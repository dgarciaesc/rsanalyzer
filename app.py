from flask import Flask, request, jsonify
from flask_cors import CORS
import pyairbnb
import json
import pyairbnb.utils as utils

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/search', methods=['POST'])
def search():
    try:
        data = request.json
        check_in = data.get('check_in')
        check_out = data.get('check_out')
        location = data.get('location', 'Luxembourg')
        currency = data.get('currency', 'EUR')
        locale = data.get('locale', 'en')
        
        # Get markets data
        api_key = pyairbnb.get_api_key("")
        markets_data = pyairbnb.get_markets(currency, locale, api_key, "")
        markets = pyairbnb.get_nested_value(markets_data, "user_markets", [])
        
        if len(markets) == 0:
            return jsonify({"error": "No markets found"}), 400
            
        config_token = pyairbnb.get_nested_value(markets[0], "satori_parameters", "")
        country_code = pyairbnb.get_nested_value(markets[0], "country_code", "")
        
        if config_token == "" or country_code == "":
            return jsonify({"error": "Invalid market configuration"}), 400
            
        # Get place IDs
        place_ids_results = pyairbnb.get_places_ids(
            country_code, location, currency, locale, config_token, api_key, ""
        )
        
        if len(place_ids_results) == 0:
            return jsonify({"error": "No locations found"}), 400
            
        # Get bounding box
        bb = place_ids_results[0]["location"]["bounding_box"]
        ne_lat = bb["ne_lat"]
        ne_long = bb["ne_lng"]
        sw_lat = bb["sw_lat"]
        sw_long = bb["sw_lng"]
        
        # Perform search
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
        
        # Save the search results as a CSV file
        csv_path = utils.json_to_csv(search_results, 'search_results.csv')
        print(f"Search results saved to: {csv_path}")
        return jsonify(search_results)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) 