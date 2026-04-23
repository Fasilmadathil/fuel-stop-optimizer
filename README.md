# :fuelpump: Fuel Optimization API

A Django REST API that calculates the most cost-effective fuel stops along a route within the USA. It is designed for vehicles with range and fuel efficiency constraints, ensuring minimal fuel cost across long-distance trips.

---

## :rocket: Features

* **Intelligent Routing**
  Accepts city names or coordinates and computes routes using OpenRouteService.

* **Cost-Effective Refueling**
  Uses a greedy algorithm to determine the cheapest fuel stations along the route.

* **Constraint-Aware Calculation**

  * Maximum vehicle range: **500 miles**
  * Fuel efficiency: **10 miles per gallon (MPG)**

* **Optimized Performance**
  Only one routing API call is made; all fuel calculations are handled locally.

---

## :hammer_and_wrench: Tech Stack

* **Backend Framework**: Django 5.x
* **API Framework**: Django REST Framework (DRF)
* **Geospatial Services**:

  * OpenRouteService (Routing)
  * Nominatim (Geocoding)
* **Core Logic**: Python (Haversine formula for proximity calculations)

---

## :satellite_antenna: API Endpoint

### `POST /api/optimize-route/`

#### Request Body

```json
{
  "start": "New York",
  "end": "Los Angeles"
}
```

#### Response Body

```json
{
  "distance_miles": 2793.5,
  "route_polyline": "...",
  "fuel_stops": [
    {
      "station": "Circle K",
      "address": "123 Main St, Example, OH",
      "price": 3.06,
      "coordinates": [41.32, -82.48]
    }
  ],
  "total_cost": 854.21
}
```

---

## :gear: Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Fasilmadathil/fuel-optimization-api.git
cd fuel-optimization-api
```

---

### 2. Create Virtual Environment

```bash
python -m venv venv
```

#### Activate Environment

**Windows**

```bash
venv\Scripts\activate
```

**Mac/Linux**

```bash
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Setup Environment Variables

Create a `.env` file in the root directory:

```env
OPENROUTESERVICE_API_KEY=your_api_key_here
```

---

### 5. Run the Server

```bash
python manage.py migrate
python manage.py runserver
```

Server will be available at:

```
http://127.0.0.1:8000/
```

---

## :zap: Design Notes

* **Efficiency First**
  The API fetches the full route once and performs all fuel optimization locally.

* **Greedy Algorithm**
  Always selects the cheapest reachable fuel station within the current fuel range.

* **Safety Buffer**
  Ensures the vehicle never exceeds the 500-mile limit without refueling.

* **Lightweight Architecture**
  Avoids heavy GIS tools like PostGIS for faster setup and deployment.

---

## :pushpin: Example Use Case

Plan a cost-efficient road trip from **New York to Los Angeles** by automatically selecting optimal fuel stops based on real-time pricing and route constraints.

---


## :bust_in_silhouette: Author

**Fasil Madathil**

GitHub: https://github.com/Fasilmadathil

---