import requests
import json
import time

def fetch_post_offices_by_state(state_name):
    """
    Fetch post office locations from OpenStreetMap for a given state.
    Uses the Overpass API to query OSM data.
    """
    overpass_url = "https://overpass-api.de/api/interpreter"

    # Overpass QL query to find all post offices in the state
    overpass_query = f"""
    [out:json][timeout:180];
    area["name"="{state_name}"]["admin_level"="4"]["boundary"="administrative"]->.searchArea;
    (
      node["amenity"="post_office"](area.searchArea);
      way["amenity"="post_office"](area.searchArea);
      relation["amenity"="post_office"](area.searchArea);
    );
    out center;
    """

    print(f"Fetching post offices for {state_name}...")
    response = requests.post(overpass_url, data={"data": overpass_query})

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data for {state_name}: {response.status_code}")
        return None

def fetch_all_us_post_offices():
    """
    Fetch all post offices in the continental United States.
    Note: This uses a bounding box for the entire US.
    """
    overpass_url = "https://overpass-api.de/api/interpreter"

    # Bounding box for continental US: (south, west, north, east)
    # Approximate: 24.5°N to 49°N latitude, -125°W to -66°W longitude
    overpass_query = """
    [out:json][timeout:300];
    (
      node["amenity"="post_office"](24.5,-125.0,49.0,-66.0);
      way["amenity"="post_office"](24.5,-125.0,49.0,-66.0);
    );
    out center;
    """

    print("Fetching all post offices in the continental US...")
    print("This may take a few minutes...")

    response = requests.post(overpass_url, data={"data": overpass_query})

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

def parse_post_office_data(osm_data):
    """
    Parse OSM data and extract post office information.
    Returns a list of post offices with name, lat, lon, address info.
    """
    post_offices = []

    if not osm_data or 'elements' not in osm_data:
        return post_offices

    for element in osm_data['elements']:
        post_office = {}

        # Get coordinates
        if element['type'] == 'node':
            post_office['lat'] = element['lat']
            post_office['lon'] = element['lon']
        elif 'center' in element:
            post_office['lat'] = element['center']['lat']
            post_office['lon'] = element['center']['lon']
        else:
            continue  # Skip if no coordinates available

        # Get tags (name, address, etc.)
        tags = element.get('tags', {})
        post_office['name'] = tags.get('name', 'Post Office')
        post_office['operator'] = tags.get('operator', '')
        post_office['street'] = tags.get('addr:street', '')
        post_office['housenumber'] = tags.get('addr:housenumber', '')
        post_office['city'] = tags.get('addr:city', '')
        post_office['state'] = tags.get('addr:state', '')
        post_office['postcode'] = tags.get('addr:postcode', '')
        post_office['phone'] = tags.get('phone', '')
        post_office['opening_hours'] = tags.get('opening_hours', '')

        post_offices.append(post_office)

    return post_offices

def save_to_json(data, filename='post_offices.json'):
    """Save post office data to JSON file."""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Saved {len(data)} post offices to {filename}")

if __name__ == "__main__":
    # Fetch post office data
    osm_data = fetch_all_us_post_offices()

    if osm_data:
        # Parse the data
        post_offices = parse_post_office_data(osm_data)

        print(f"\nFound {len(post_offices)} post offices")

        # Save to JSON file
        save_to_json(post_offices)

        # Print a sample
        if post_offices:
            print("\nSample post office:")
            print(json.dumps(post_offices[0], indent=2))
    else:
        print("Failed to fetch post office data")
