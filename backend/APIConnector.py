import os
import googlemaps

api_key = os.environ.get("GOOGLE_API")

gmaps = googlemaps.Client(key=api_key)

route = gmaps.directions("Hamburg,Germany" , "Berlin, Germany")
print(route)