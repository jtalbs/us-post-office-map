# US Post Office Map

An interactive map visualization of US Post Office locations using OpenStreetMap data.

## Features

- Fetches post office data from OpenStreetMap via Overpass API
- Creates an interactive web map using Leaflet (via Folium)
- Marker clustering for better performance
- Displays post office details including address, phone, and hours

## Installation

1. Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Step 1: Fetch Post Office Data

Run the data fetching script to download post office locations from OpenStreetMap:

```bash
python fetch_post_offices.py
```

This will:
- Query OpenStreetMap's Overpass API for all post offices in the continental US
- Save the data to `post_offices.json`
- May take a few minutes to complete

### Step 2: Generate the Map

Create the interactive map:

```bash
python create_map.py
```

This will:
- Load data from `post_offices.json`
- Generate an interactive HTML map
- Save it as `post_office_map.html`

### Step 3: View the Map

Open `post_office_map.html` in your web browser to view the interactive map!

## Data Source

Post office location data comes from [OpenStreetMap](https://www.openstreetmap.org/), a collaborative project to create a free editable map of the world.

The data is queried using the [Overpass API](https://overpass-api.de/), which provides read-only access to OpenStreetMap data.

## License

This project uses OpenStreetMap data, which is © OpenStreetMap contributors and available under the [Open Database License](https://opendatacommons.org/licenses/odbl/).

## Notes

- The completeness of the data depends on OpenStreetMap contributors
- Not all post offices may be tagged in OSM
- Data freshness depends on when OSM was last updated in each area
- For official USPS data, visit [PostalPro](https://postalpro.usps.com/gis)
