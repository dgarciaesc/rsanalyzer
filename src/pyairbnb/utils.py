import re
from urllib.parse import quote
from datetime import datetime
import csv


regex_space = re.compile(r'[\s ]+')
regx_price = re.compile(r'\d+')

def remove_space(value:str):
    return regex_space.sub(' ', value.strip())

def get_nested_value(dic, key_path, default=None):
    keys = key_path.split(".")
    current = dic
    for key in keys:
        current = current.get(key, {})
        if current == {} or current is None:
            return default
    return current

def parse_price_symbol(price_raw: str):
    price_raw = price_raw.replace(",", "")

    
    price_number_match = regx_price.search(price_raw)
    
    if price_number_match is None:
        return 0,""
    
    price_number = price_number_match.group(0)
    
    price_currency = price_raw.replace(price_number, "").replace(" ", "").replace("-", "")
    
    price_converted = float(price_number)
    if price_raw.startswith("-"):
        price_converted *= -1
    
    return price_converted, price_currency

def parse_proxy(ip_or_domain: str,port: str, username: str, password: str) -> (str):
    encoded_username = quote(username)
    encoded_password = quote(password)
    proxy_url = f"http://{encoded_username}:{encoded_password}@{ip_or_domain}:{port}"
    return proxy_url
    
def json_to_csv(json_data, output_path=None):
    """
    Convert JSON data directly to CSV format.
    
    Args:
        json_data (dict or list): The JSON data to convert
        output_path (str, optional): Path for the output CSV file. If not provided, will use timestamp.
    
    Returns:
        str: Path to the created CSV file
    """
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"airbnb_data_{timestamp}.csv"
    
    # Extract the relevant data from the JSON structure
    data_to_write = []
    
    # Handle both single item and list of items
    items = json_data if isinstance(json_data, list) else [json_data]
    
    for item in items:
        # Extract basic information
        room_data = {
            'room_id': item.get('room_id', ''),
            'category': item.get('category', ''),
            'kind': item.get('kind', ''),
            'name': item.get('name', ''),
            'title': item.get('title', ''),
            'type': item.get('type', ''),
            'price_unit_amount': item.get('price', {}).get('unit', {}).get('amount', ''),
            'price_unit_currency': item.get('price', {}).get('unit', {}).get('curency_symbol', ''),
            'price_unit_qualifier': item.get('price', {}).get('unit', {}).get('qualifier', ''),
            'price_total_amount': item.get('price', {}).get('total', {}).get('amount', ''),
            'price_total_currency': item.get('price', {}).get('total', {}).get('currency_symbol', ''),
            'airbnb_fee_amount': item.get('fee', {}).get('airbnb', {}).get('amount', ''),
            'airbnb_fee_currency': item.get('fee', {}).get('airbnb', {}).get('currency_symbol', ''),
            'cleaning_fee_amount': item.get('fee', {}).get('cleaning', {}).get('amount', ''),
            'cleaning_fee_currency': item.get('fee', {}).get('cleaning', {}).get('currency_symbol', ''),
            'rating_value': item.get('rating', {}).get('value', ''),
            'rating_count': item.get('rating', {}).get('reviewCount', ''),
            'latitude': item.get('coordinates', {}).get('latitude', ''),
            'longitude': item.get('coordinates', {}).get('longitud', ''),
            'badges': ','.join(item.get('badges', [])),
            'image_urls': ','.join([img.get('url', '') for img in item.get('images', [])])
        }
        data_to_write.append(room_data)
    
    # Write to CSV
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        if data_to_write:
            fieldnames = data_to_write[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data_to_write)
    
    return output_path