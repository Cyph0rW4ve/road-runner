import os
import googlemaps

api_key = os.environ.get("GOOGLE_API")
gmaps = googlemaps.Client(key=api_key)

# Look up an address with reverse geocoding
reverse_geocode_result = gmaps.directions("Hamburg", "Berlin")
#print(reverse_geocode_result)

distance = reverse_geocode_result[0]['legs'][0]['distance']['text']
duration = reverse_geocode_result[0]['legs'][0]['duration']['value']
print(distance, "meters.")
print(duration, "seconds.")