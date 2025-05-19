import requests
import math
import time

def calculate_distance_to_center(address):
    """Calculate the real distance from an address to Riga center (Origo)"""
    # Center coordinates (Origo/Station square)
    center_lat, center_lng = 56.949653, 24.118738
    
    # If address is empty or None, use default value
    if not address or address.strip() == "":
        return 5.0, 15
    
    try:
        # Use Nominatim (OpenStreetMap) geocoding
        # In a real project, could use Google Maps API or similar
        search_address = f"{address}, Riga, Latvia"
        url = f"https://nominatim.openstreetmap.org/search?q={search_address}&format=json&limit=1"
        
        response = requests.get(url, headers={'User-Agent': 'PropertySearchProject'})
        data = response.json()
        
        if data and len(data) > 0:
            # Get coordinates
            lat = float(data[0]['lat'])
            lng = float(data[0]['lon'])
            
            # Calculate distance (Haversine formula km)
            R = 6371  # Earth radius in km
            dlat = math.radians(lat - center_lat)
            dlng = math.radians(lng - center_lng)
            
            a = math.sin(dlat/2)**2 + math.cos(math.radians(center_lat)) * math.cos(math.radians(lat)) * math.sin(dlng/2)**2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
            distance = R * c
            
            # Calculate driving time in minutes (assume average speed 30 km/h in city)
            time_minutes = math.ceil(distance / 30 * 60)
            
            return round(distance, 2), time_minutes
    
    except Exception as e:
        print(f"Error calculating distance: {e}")
    
    # If calculation failed, use approximate value based on district name
    districts = {
        "center": 0.5,
        "oldtown": 0.3,
        "downtown": 0.5,
        "pardaugava": 3.0,
        "kengarags": 7.0,
        "purvciems": 5.0,
        "teika": 4.5,
        "imanta": 9.0,
        "zolitude": 10.0,
        "ziepniekkalns": 7.5,
        "agenskalns": 3.5,
        "jugla": 9.0,
        "mezciems": 7.0,
        "bolderaja": 12.0,
        "sarkandaugava": 5.0,
        "kipsala": 2.5,
        "maskava": 3.0,
        "tornkalns": 4.0,
        # Streets in central areas
        "brivibas": 2.0,
        "terbatas": 1.0,
        "caka": 1.5,
        "chaka": 1.5,
        "valdemara": 2.0,
        "dzirnavu": 1.0,
        "barona": 1.2,
        "gertrudes": 1.8,
        "stabu": 1.5,
        "matisa": 2.5,
        "avotu": 2.5,
        "tallinas": 3.0,
        "marijas": 0.8,
        "elizabetes": 1.0,
        "alberta": 2.0
    }
    
    address_lower = address.lower()
    
    # Try to find district or street in address
    for district, distance in districts.items():
        if district in address_lower:
            # Calculate approximate time (minutes) by car (average speed 30 km/h)
            time_minutes = math.ceil(distance / 30 * 60)
            return round(distance, 2), time_minutes
    
    # If district not found, return default value (5 km, 15 min)
    return 5.0, 15


def measure_time_complexity(func, *args, **kwargs):
    """Measure function execution time for time complexity analysis"""
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    execution_time = end_time - start_time
    
    print(f"Function {func.__name__} executed in {execution_time:.6f} seconds")
    return result, execution_time