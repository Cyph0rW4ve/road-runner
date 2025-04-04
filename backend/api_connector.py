import os
import googlemaps

api_key = os.environ.get("GOOGLE_API")
gmaps = googlemaps.Client(key=api_key)

# Look up an address with reverse geocoding
reverse_geocode_result = gmaps.directions((53.92831446221393, 10.298307693453467),(53.99836624481872, 10.779813054315975))
print(reverse_geocode_result)

distance = reverse_geocode_result[0]['legs'][0]['distance']['value']
duration = reverse_geocode_result[0]['legs'][0]['duration']['value']
print(distance, "meters.")
print(duration, "seconds.")