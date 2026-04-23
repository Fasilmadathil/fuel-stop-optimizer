import requests
import polyline
from django.conf import settings


def get_route(start, end):
    if isinstance(start, str):
        start = geocode_location(start)

    if isinstance(end, str):
        end = geocode_location(end)

    url = "https://api.openrouteservice.org/v2/directions/driving-car"

    headers = {
        "Authorization": settings.OPENROUTESERVICE_API_KEY,
        "Content-Type": "application/json"
    }

    body = {
        "coordinates": [start, end]
    }

    response = requests.post(url, json=body, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Route API failed: {response.text}")

    data = response.json()

    if "routes" not in data:
        raise Exception(f"Invalid response: {data}")

    route = data["routes"][0]


    coords = polyline.decode(route["geometry"])


    coords = [[lng, lat] for lat, lng in coords]

    return {
        "distance_km": route["summary"]["distance"] / 1000,
        "coordinates": coords,
        "polyline": route["geometry"]
    }

def geocode_location(location):
    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": location,
        "format": "json",
        "limit": 1
    }

    response = requests.get(
        url,
        params=params,
        headers={"User-Agent": "fuel-app"}
    )

    data = response.json()

    if not data:
        raise Exception(f"Could not geocode location: {location}")

    lat = float(data[0]["lat"])
    lng = float(data[0]["lon"])

    return [lng, lat]