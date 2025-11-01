import json
import folium
from folium.plugins import FastMarkerCluster

def load_post_offices(filename='post_offices.json'):
    """Load post office data from JSON file."""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {filename} not found. Run fetch_post_offices.py first.")
        return []

def create_map(post_offices, output_file='post_office_map.html'):
    """
    Create an interactive map with post office locations.
    Uses marker clustering for better performance with many points.
    """
    if not post_offices:
        print("No post office data to display")
        return

    # Center the map on the US (approximate center)
    us_center = [39.8283, -98.5795]

    # Create base map with simple, light background
    m = folium.Map(
        location=us_center,
        zoom_start=4,
        tiles='CartoDB Positron'
    )

    # Prepare data for FastMarkerCluster
    callback = ('function (row) {'
                'var icon = L.divIcon({html: \'<div style="background-color:#e74c3c;width:10px;height:10px;border-radius:50%;border:2px solid white;"></div>\'});'
                'var marker = L.marker(new L.LatLng(row[0], row[1]), {icon: icon});'
                'var popup = row[2];'
                'marker.bindPopup(popup);'
                'return marker;};')

    # Build data array with coordinates and popup HTML for each post office
    data = []
    for po in post_offices:
        # Build popup content
        popup_html = f"<b>{po['name']}</b><br>"

        if po.get('housenumber') and po.get('street'):
            popup_html += f"{po['housenumber']} {po['street']}<br>"
        elif po.get('street'):
            popup_html += f"{po['street']}<br>"

        if po.get('city'):
            popup_html += f"{po['city']}, "
        if po.get('state'):
            popup_html += f"{po['state']} "
        if po.get('postcode'):
            popup_html += f"{po['postcode']}"

        if po.get('city') or po.get('state') or po.get('postcode'):
            popup_html += "<br>"

        if po.get('phone'):
            popup_html += f"Phone: {po['phone']}<br>"

        if po.get('opening_hours'):
            popup_html += f"Hours: {po['opening_hours']}<br>"

        if po.get('operator'):
            popup_html += f"Operator: {po['operator']}"

        data.append([po['lat'], po['lon'], popup_html])

    # Add fast marker cluster
    FastMarkerCluster(data, callback=callback).add_to(m)

    # Add layer control
    folium.LayerControl().add_to(m)

    # Add title
    title_html = '''
    <div style="position: fixed;
                top: 10px; left: 50px; width: 400px; height: 60px;
                background-color: white; border:2px solid grey; z-index:9999;
                font-size:16px; padding: 10px">
        <b>US Post Office Map</b><br>
        Total Post Offices: {count}
    </div>
    '''.format(count=len(post_offices))

    m.get_root().html.add_child(folium.Element(title_html))

    # Save map
    m.save(output_file)
    print(f"Map saved to {output_file}")
    print(f"Total post offices mapped: {len(post_offices)}")

if __name__ == "__main__":
    # Load data
    post_offices = load_post_offices()

    if post_offices:
        # Create map
        create_map(post_offices)
        print("\nOpen post_office_map.html in your browser to view the map!")
    else:
        print("No data available. Please run fetch_post_offices.py first.")
