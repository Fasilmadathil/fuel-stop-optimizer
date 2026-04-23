from routing.models import FuelStation
import math

MAX_RANGE_KM = 800  
DISTANCE_WEIGHT = 0.01  


def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km

    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)

    a = (
        math.sin(d_lat / 2) ** 2 +
        math.cos(math.radians(lat1)) *
        math.cos(math.radians(lat2)) *
        math.sin(d_lon / 2) ** 2
    )

    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def get_stops(route_coords):
    if not route_coords:
        return []

    stops = []
    distance_accum = 0

    prev_lng, prev_lat = route_coords[0]

    for lng, lat in route_coords[1:]:
        segment = haversine(prev_lat, prev_lng, lat, lng)
        distance_accum += segment

        if distance_accum >= MAX_RANGE_KM:
            stops.append((lng, lat))
            distance_accum -= MAX_RANGE_KM  

        prev_lng, prev_lat = lng, lat

    return stops


def find_best_station(lat, lng):
    candidates = FuelStation.objects.filter(
        latitude__range=(lat - 1.5, lat + 1.5),
        longitude__range=(lng - 1.5, lng + 1.5)
    )

    best_station = None
    best_score = float("inf")

    for station in candidates:
        distance = haversine(lat, lng, station.latitude, station.longitude)


        score = station.price + (distance * DISTANCE_WEIGHT)

        if score < best_score:
            best_score = score
            best_station = station


    if not best_station:
        best_station = FuelStation.objects.order_by('price').first()

    return best_station


def get_fuel_plan(route_coords, total_distance_km):
    stops = get_stops(route_coords)

    result = []

    for lng, lat in stops:
        station = find_best_station(lat, lng)

        if station:
            result.append({
                "lat": lat,
                "lng": lng,
                "station": station.name,
                "price": float(station.price)
            })

    return result


def calculate_cost(stops):
    total = 0

    for stop in stops:
        total += 50 * stop["price"]  # 50 gallons per full tank

    return round(total, 2)