from flask import Flask, request, jsonify
from flask_cors import CORS
import pyairbnb
import json
import pyairbnb.utils as utils
from datetime import datetime
from models import db, SearchResult
from config import Config
import logging
import os
import sys
import csv
import pandas as pd

# Configure logging
def setup_logger():
    logger = logging.getLogger('airbnb_search')
    logger.setLevel(logging.DEBUG if os.getenv('ENABLE_LOGS', 'true').lower() == 'true' else logging.WARNING)
    
    # Create console handler with formatting
    console_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logger()

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Initialize database
db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()
    logger.info("Database initialized and tables created")

def extract_price(price_data):
    """Extract price from Airbnb's complex price structure"""
    try:
        if not price_data:
            return 0.0
            
        # Try to get the unit price first (monthly rate)
        if isinstance(price_data, dict):
            # Check for unit price (monthly rate)
            if 'unit' in price_data and 'amount' in price_data['unit']:
                return float(price_data['unit']['amount'])
            
            # Check for total price
            if 'total' in price_data and 'amount' in price_data['total']:
                return float(price_data['total']['amount'])
            
            # Check for break_down (last item is usually the final price)
            if 'break_down' in price_data and price_data['break_down']:
                last_breakdown = price_data['break_down'][-1]
                if 'amount' in last_breakdown:
                    return float(last_breakdown['amount'])
        
        # If it's a direct number
        return float(price_data)
    except (ValueError, TypeError, KeyError) as e:
        logger.warning(f"Could not parse price: {str(e)}")
        return 0.0

def save_to_csv(results, filename):
    """Save search results to a CSV file"""
    try:
        # Create a list to store the flattened data
        flattened_data = []
        
        for result in results:
            # Extract price safely
            price = extract_price(result.get('price', {}))
            
            # Create a flattened record
            record = {
                'listing_id': str(result.get('room_id', result.get('id', ''))),
                'title': result.get('name', ''),
                'description': result.get('title', ''),
                'price': price,
                'currency': 'EUR',  # Default to EUR as it's in the price structure
                'location': result.get('location', ''),
                'latitude': result.get('coordinates', {}).get('latitude'),
                'longitude': result.get('coordinates', {}).get('longitud'),
                'room_type': result.get('category', ''),
                'room_kind': result.get('kind', ''),
                'url': result.get('url', ''),
                'rating': result.get('rating', {}).get('value', 0),
                'reviews_count': result.get('rating', {}).get('reviewCount', 0),
                'images': [img.get('url', '') for img in result.get('images', [])]
            }
            flattened_data.append(record)

        # Convert to DataFrame and save to CSV
        df = pd.DataFrame(flattened_data)
        df.to_csv(filename, index=False)
        logger.info(f"Results saved to CSV file: {filename}")
        return True
    except Exception as e:
        logger.error(f"Error saving to CSV: {str(e)}")
        return False

@app.route('/health', methods=['GET'])
def health_check():
    logger.debug("Health check endpoint called")
    return jsonify({"status": "healthy"}), 200

@app.route('/api/search', methods=['POST'])
def search():
    logger.info(f"Search request received: {request.json}")
    try:
        data = request.json
        check_in = data.get('check_in')
        check_out = data.get('check_out')
        location = data.get('location', 'Luxembourg')
        currency = data.get('currency', 'EUR')
        locale = data.get('locale', 'en')
        
        logger.debug(f"Search parameters - Location: {location}, Check-in: {check_in}, Check-out: {check_out}")
        
        # Get markets data
        logger.debug("Fetching markets data")
        api_key = pyairbnb.get_api_key("")
        markets_data = pyairbnb.get_markets(currency, locale, api_key, "")
        markets = pyairbnb.get_nested_value(markets_data, "user_markets", [])
        
        if len(markets) == 0:
            logger.error("No markets found")
            return jsonify({"error": "No markets found"}), 400
            
        config_token = pyairbnb.get_nested_value(markets[0], "satori_parameters", "")
        country_code = pyairbnb.get_nested_value(markets[0], "country_code", "")
        
        if config_token == "" or country_code == "":
            logger.error("Invalid market configuration")
            return jsonify({"error": "Invalid market configuration"}), 400
            
        # Get place IDs
        logger.debug(f"Fetching place IDs for location: {location}")
        place_ids_results = pyairbnb.get_places_ids(
            country_code, location, currency, locale, config_token, api_key, ""
        )
        
        if len(place_ids_results) == 0:
            logger.error(f"No locations found for: {location}")
            return jsonify({"error": "No locations found"}), 400
            
        # Get bounding box
        bb = place_ids_results[0]["location"]["bounding_box"]
        ne_lat = bb["ne_lat"]
        ne_long = bb["ne_lng"]
        sw_lat = bb["sw_lat"]
        sw_long = bb["sw_lng"]
        
        logger.debug(f"Bounding box - NE: ({ne_lat}, {ne_long}), SW: ({sw_lat}, {sw_long})")
        
        # Perform search
        logger.info("Starting Airbnb search")
        search_results = pyairbnb.search_all(
            check_in=check_in,
            check_out=check_out,
            ne_lat=ne_lat,
            ne_long=ne_long,
            sw_lat=sw_lat,
            sw_long=sw_long,
            zoom_value=2,
            price_min=0,
            price_max=0,
            place_type="",
            amenities=[],
            currency=currency,
            language=locale,
            proxy_url=""
        )
        
        logger.info(f"Found {len(search_results)} search results")
        
        # Store results in database
        logger.debug("Storing results in database")
        for result in search_results:
            # Extract price safely
            price = extract_price(result.get('price', {}))
            
            search_result = SearchResult(
                listing_id=str(result.get('room_id', result.get('id', ''))),
                title=result.get('name', ''),
                description=result.get('title', ''),
                price=price,
                currency=currency,
                location=location,
                latitude=result.get('coordinates', {}).get('latitude'),
                longitude=result.get('coordinates', {}).get('longitud'),
                check_in=datetime.strptime(check_in, '%Y-%m-%d').date(),
                check_out=datetime.strptime(check_out, '%Y-%m-%d').date(),
                raw_data=result
            )
            db.session.add(search_result)
        
        db.session.commit()
        logger.info("Search results stored in database successfully")

        # Save to CSV
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        csv_filename = f'search_results_{location}_{timestamp}.csv'
        save_to_csv(search_results, csv_filename)
        
        return jsonify(search_results)
        
    except Exception as e:
        logger.error(f"Error during search: {str(e)}", exc_info=True)
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    logger.info("Starting Flask application")
    app.run(debug=True, host='0.0.0.0', port=5000) 