import csv
import time
import requests

from django.core.management.base import BaseCommand
from routing.models import FuelStation


class Command(BaseCommand):
    help = "Import fuel data with optimized geocoding"

    def get_lat_lng(self, city, state):
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "city": city,
            "state": state,
            "country": "USA",
            "format": "json",
            "limit": 1
        }

        try:
            response = requests.get(
                url,
                params=params,
                headers={"User-Agent": "fuel-optimizer-app"}
            )

            if response.status_code != 200:
                return None, None

            data = response.json()

            if data:
                return float(data[0]["lat"]), float(data[0]["lon"])

        except Exception as e:
            print(f"Error: {city}, {state} → {e}")

        return None, None

    def handle(self, *args, **kwargs):
        file_path = r"fuel_optimizer\fuel-prices-for-be-assessment.csv"

        stations_to_create = []
        seen_stations = set()
        city_cache = {} 

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for idx, row in enumerate(reader):
                name = row.get("Truckstop Name", "").strip()
                city = row.get("City", "").strip()
                state = row.get("State", "").strip()
                price = row.get("Retail Price", "").strip()

                if not (name and city and state and price):
                    continue

                key = (name, city, state)
                if key in seen_stations:
                    continue
                seen_stations.add(key)

                try:
                    price = float(price)
                except:
                    continue

                city_key = (city, state)

                if city_key in city_cache:
                    lat, lng = city_cache[city_key]

                else:
                    lat, lng = self.get_lat_lng(city, state)

                    if lat is None or lng is None:
                        print(f"Skipping: {city}, {state}")
                        continue

                    city_cache[city_key] = (lat, lng)

                    print(f"Geocoded: {city}, {state} → {lat}, {lng}")

                    time.sleep(1)

                station = FuelStation(
                    name=name,
                    city=city,
                    state=state,
                    latitude=lat,
                    longitude=lng,
                    price=price
                )

                stations_to_create.append(station)

                if idx % 500 == 0:
                    print(f"Processed {idx} rows...")

        FuelStation.objects.bulk_create(stations_to_create, batch_size=500)

        self.stdout.write(
            self.style.SUCCESS(f"Imported {len(stations_to_create)} stations")
        )