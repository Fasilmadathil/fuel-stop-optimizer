from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .services.route_service import get_route
from .services.fuel_service import get_fuel_plan, calculate_cost


@api_view(['POST'])
def optimize_route(request):
    start = request.data.get("start")
    end = request.data.get("end")

    if not start or not end:
        return Response(
        {"error": "start and end are required"},
        status=status.HTTP_400_BAD_REQUEST
        )

    if isinstance(start, list) and len(start) != 2:
        return Response(
        {"error": "start must be [lng, lat]"},
        status=status.HTTP_400_BAD_REQUEST
        )

    if isinstance(end, list) and len(end) != 2:
        return Response(
        {"error": "end must be [lng, lat]"},
        status=status.HTTP_400_BAD_REQUEST
        )

    try:
        route = get_route(start, end)

        fuel_stops = get_fuel_plan(
            route["coordinates"],
            route["distance_km"]
        )

        total_cost = calculate_cost(fuel_stops)

        return Response({
            "distance_km": round(route["distance_km"], 2),
            "fuel_stops": fuel_stops,
            "total_cost": total_cost,
            "route_polyline": route["polyline"]
        })

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )