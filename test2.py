import pyairbnb
import json
import pyairbnb.utils as utils

check_in = "2025-08-01"
check_out = "2025-08-17"
currency = "EUR"
user_input_text = "Somo"
locale = "pt"
proxy_url = ""  # Proxy URL (if needed)
zoom_value=10
api_key = pyairbnb.get_api_key("")
markets_data = pyairbnb.get_markets(currency,locale,api_key,proxy_url)
markets = pyairbnb.get_nested_value(markets_data,"user_markets", [])
if len(markets)==0:
    raise Exception("markets are empty")
config_token = pyairbnb.get_nested_value(markets[0],"satori_parameters", "")
country_code = pyairbnb.get_nested_value(markets[0],"country_code", "")
if config_token=="" or country_code=="":
    raise Exception("config_token or country_code are empty")
place_ids_results = pyairbnb.get_places_ids(country_code, user_input_text, currency, locale, config_token, api_key, proxy_url)
if len(place_ids_results)==0:
    raise Exception("empty places ids")
place_id = pyairbnb.get_nested_value(place_ids_results[0],"location.google_place_id", "")
location_name = pyairbnb.get_nested_value(place_ids_results[0],"location.location_name", "")
print("place_id: ",place_id)
print("location_name: ",location_name)
bb=place_ids_results[0]["location"]["bounding_box"]
ne_lat = bb["ne_lat"]
ne_long = bb["ne_lng"]
sw_lat = bb["sw_lat"]
sw_long = bb["sw_lng"]
price_min = 0
price_max = 0
place_type = ""
amenities = []
currency = currency
language = "en"
proxy_url = ""

search_results = pyairbnb.search_all(
    check_in=check_in,
    check_out=check_out,
    ne_lat=ne_lat,
    ne_long=ne_long,
    sw_lat=sw_lat,
    sw_long=sw_long,
    zoom_value=zoom_value,
    price_min=price_min,
    price_max=price_max,
    place_type=place_type,
    amenities=amenities,
    currency=currency,
    language=language,
    proxy_url=proxy_url
)

# Save the search results as a CSV file
csv_path = utils.json_to_csv(search_results, 'search_results1.csv')
print(f"Search results saved to: {csv_path}")

room_url = "https://www.airbnb.com/rooms/51752186"  # Listing URL
currency = "USD"  # Currency for the listing details
check_in = "2026-05-15"
check_out = "2026-05-17"
# Retrieve listing details without including the price information (no check-in/check-out dates)
data = pyairbnb.get_details(room_url=room_url, currency=currency,adults=4,check_in=check_in,check_out=check_out)

# Save the retrieved details to a CSV file
csv_path = utils.json_to_csv(data, 'details_data.csv')
print(f"Details data saved to: {csv_path}")

# Test search_all_from_url using a sample Airbnb URL with various filters
results = pyairbnb.search_all_from_url("https://www.airbnb.es/s/Somo/homes?refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2025-07-01&monthly_length=3&monthly_end_date=2025-10-01&price_filter_input_type=0&channel=EXPLORE&date_picker_type=calendar&checkin=2025-06-28&checkout=2025-07-31&source=structured_search_input_header&search_type=user_map_move&place_id=ChIJ99XqptRKSQ0RBOWNO2Mpae4&acp_id=ef7cd257-720e-4946-963b-22b4eade22cf&query=Somo&search_mode=regular_search&price_filter_num_nights=33&ne_lat=43.45945813069151&ne_lng=-3.726544351373718&sw_lat=43.44540119740168&sw_lng=-3.7409395081610626&zoom=15.464059110494395&zoom_level=15.464059110494395&search_by_map=true", currency="USD", proxy_url="")
# Save URL search results to CSV
csv_path = utils.json_to_csv(results, 'search_results_from_url.csv')

print(f"URL search results saved to: {csv_path}")

print(f"Retrieved {len(results)} listings from URL search.")