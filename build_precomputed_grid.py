import json
import math
import re

ZONING_FILE = "ura-zoning-subset.geojson"
CLINIC_FILE = "locations.js"
OUTPUT_FILE = "grid-precomputed.json"

CELL_SIZE = 0.0035
BOUNDS = [
    [1.20, 103.60],
    [1.48, 104.05]
]

print("Loading zoning...")
with open(ZONING_FILE) as f:
    zoning = json.load(f)

print("Loading clinics...")

# Extract JSON array safely from JS file
with open(CLINIC_FILE) as f:
    text = f.read()

match = re.search(r'\[\s*{.*}\s*\]', text, re.DOTALL)
if not match:
    raise Exception("Could not extract clinic JSON from locations.js")

clinics = json.loads(match.group())

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = (math.sin(dLat/2)**2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(dLon/2)**2)
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

def point_in_poly(lat, lng, poly):
    inside = False
    x, y = lng, lat
    for i in range(len(poly)):
        j = (i - 1) % len(poly)
        xi, yi = poly[i]
        xj, yj = poly[j]
        if ((yi > y) != (yj > y)) and \
           (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
            inside = not inside
    return inside

print("Precomputing zoning bounding boxes...")

features = []
for f in zoning["features"]:
    geom = f["geometry"]
    lu = f["properties"]["LU_DESC"].upper()

    if geom["type"] == "Polygon":
        coords = geom["coordinates"][0]
    elif geom["type"] == "MultiPolygon":
        coords = geom["coordinates"][0][0]
    else:
        continue

    lngs = [c[0] for c in coords]
    lats = [c[1] for c in coords]

    features.append({
        "coords": coords,
        "bbox": {
            "minLat": min(lats),
            "maxLat": max(lats),
            "minLng": min(lngs),
            "maxLng": max(lngs)
        },
        "lu": lu
    })

grid = []

print("Building grid...")

lat = BOUNDS[0][0]
while lat <= BOUNDS[1][0]:
    lng = BOUNDS[0][1]
    while lng <= BOUNDS[1][1]:

        centerLat = lat + CELL_SIZE/2
        centerLng = lng + CELL_SIZE/2

        zone = None

        for f in features:
            b = f["bbox"]
            if centerLat < b["minLat"] or centerLat > b["maxLat"] \
               or centerLng < b["minLng"] or centerLng > b["maxLng"]:
                continue

            if point_in_poly(centerLat, centerLng, f["coords"]):
                zone = f["lu"]
                break

        if not zone:
            lng += CELL_SIZE
            continue

        # INDUSTRIAL
        if any(k in zone for k in ["INDUSTRIAL","BUSINESS","WHITE"]):
            grid.append({"lat": lat, "lng": lng, "type": "industrial"})

        # RESTRICTED
        elif any(k in zone for k in
            ["MILITARY","DEFENCE","SPECIAL","UTILITY","TRANSPORT","PORT","AIRPORT"]):
            grid.append({"lat": lat, "lng": lng, "type": "restricted"})

        # RESIDENTIAL
        elif "RESIDENTIAL" in zone:

            minDist = float("inf")
            for c in clinics:
                d = haversine(centerLat, centerLng, c["lat"], c["lng"])
                if d < minDist:
                    minDist = d

            if minDist > 1000:
                grid.append({"lat": lat, "lng": lng, "type": "opportunity"})

        lng += CELL_SIZE
    lat += CELL_SIZE

print("Saving grid...")
with open(OUTPUT_FILE, "w") as f:
    json.dump(grid, f)

print("Done. Cells:", len(grid))
