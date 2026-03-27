import requests
import json
import sys
from Polygon import Polygon

api_url = "https://nominatim.openstreetmap.org/search?"
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
}

def get_coords(query):
    results = requests.get(
        api_url + "q=" + query + "&format=json",
        headers=headers
    ).json()
    if not results:
        print(f"Could not find location: '{query}'")
        sys.exit(1)
    result = results[0]
    return [float(result['lat']), float(result['lon'])], result.get('display_name', query)

def find_tz(wanted_coord):
    try:
        with open('combined-now.json', 'r') as f:
            tz_map = json.load(f)
    except FileNotFoundError:
        print("Error: 'combined-now.json' not found. Make sure it's in the same directory.")
        sys.exit(1)

    for tz in tz_map['features']:
        geom_type = tz["geometry"]["type"]
        coords = tz["geometry"]["coordinates"]
        tzid = tz['properties']['tzid']

        if geom_type == "Polygon":
            for ring in coords:
                if Polygon(ring).is_in_polygon(wanted_coord):
                    return tzid

        elif geom_type == "MultiPolygon":
            for poly in coords:
                for ring in poly:
                    if Polygon(ring).is_in_polygon(wanted_coord):
                        return tzid

    return None

def main():
    if len(sys.argv) > 1:
        # Accept place name as a command line argument: python main.py "Paris, France"
        query = "".join(sys.argv[1:])
    else:
        # Interactive mode: prompt the user
        query = input("Enter a place name: ").strip()
        if not query:
            print("No place entered. Exiting.")
            sys.exit(0)

    print(f"Looking up '{query}'...")
    coord, display_name = get_coords(query)
    print(f"Found: {display_name}")
    print(f"Coordinates: {coord[0]:.4f}, {coord[1]:.4f}")
    print("Searching timezone data...")

    tz = find_tz(coord)
    if tz:
        print(f"Timezone: {tz}")
    else:
        print("Timezone not found for this location.")

if __name__ == "__main__":
    main()