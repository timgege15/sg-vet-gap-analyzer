import json
import math
from shapely.geometry import shape, box
from shapely.strtree import STRtree

# ---------------- CONFIG ---------------- #

GRID_SIZE = 0.0035
BOUNDING_BOX = (1.20, 103.60, 1.48, 104.05)

ZONING_FILE = "/Users/zijiaye/Downloads/MasterPlan2019LandUselayer.geojson"
INDUSTRIAL_FILE = "industrial-zones.json"
RESTRICTED_FILE = "restricted-zones.json"
CLINICS_FILE = "locations.js"

RADII = [1, 2, 3]

# ---------------------------------------- #

print("Loading zoning...")
with open(ZONING_FILE) as f:
    zoning = json.load(f)

print("Loading industrial...")
with open(INDUSTRIAL_FILE) as f:
    industrial = json.load(f)

print("Loading restricted...")
with open(RESTRICTED_FILE) as f:
    restricted = json.load(f)

print("Loading clinics...")
with open(CLINICS_FILE) as f:
    text = f.read()

start = text.find("[")
end = text.rfind("]") + 1
clinics = json.loads(text[start:end])
clinic_points = [(c["lat"], c["lng"]) for c in clinics]

# ---------------- PREPARE GEOMETRIES ---------------- #

print("Preparing residential polygons...")

def safe_shape(geom):
    g = shape(geom)
    if not g.is_valid:
        g = g.buffer(0)
    return g

residential_polys = []
for feat in zoning["features"]:
    desc = feat["properties"].get("LU_DESC","")
    if desc in [
        "RESIDENTIAL",
        "RESIDENTIAL / INSTITUTION",
        "RESIDENTIAL WITH COMMERCIAL AT 1ST STOREY"
    ]:
        residential_polys.append(safe_shape(feat["geometry"]))

industrial_polys = [safe_shape(f["geometry"]) for f in industrial["features"]]
restricted_polys = [safe_shape(f["geometry"]) for f in restricted["features"]]

# Build spatial index
res_index = STRtree(residential_polys)
ind_index = STRtree(industrial_polys)
resr_index = STRtree(restricted_polys)

# ---------------- DISTANCE FUNCTION ---------------- #

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    toRad = lambda x: x * math.pi / 180
    dLat = toRad(lat2 - lat1)
    dLon = toRad(lon2 - lon1)
    a = math.sin(dLat/2)**2 + \
        math.cos(toRad(lat1)) * math.cos(toRad(lat2)) * \
        math.sin(dLon/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

# ---------------- GRID BUILD ---------------- #

min_lat, min_lng, max_lat, max_lng = BOUNDING_BOX

for radius in RADII:

    print(f"\nBuilding grid for {radius}km...")
    cells = []

    lat = min_lat
    while lat <= max_lat:
        lng = min_lng
        while lng <= max_lng:

            cell_poly = box(lng, lat, lng+GRID_SIZE, lat+GRID_SIZE)
            cell_area = cell_poly.area

            residential_area = 0
            industrial_area = 0
            restricted_area = 0

            for idx in res_index.query(cell_poly):
                poly = residential_polys[idx]
                try:
                    if poly.intersects(cell_poly):
                        residential_area += poly.intersection(cell_poly).area
                except:
                    continue

            for idx in ind_index.query(cell_poly):
                poly = industrial_polys[idx]
                try:
                    if poly.intersects(cell_poly):
                        industrial_area += poly.intersection(cell_poly).area
                except:
                    continue

            for idx in resr_index.query(cell_poly):
                poly = restricted_polys[idx]
                try:
                    if poly.intersects(cell_poly):
                        restricted_area += poly.intersection(cell_poly).area
                except:
                    continue

            if residential_area == 0 and industrial_area == 0 and restricted_area == 0:
                lng += GRID_SIZE
                continue

            residential_pct = residential_area / cell_area
            industrial_pct = industrial_area / cell_area
            restricted_pct = restricted_area / cell_area

            dominant = max(
                [("residential", residential_pct),
                 ("industrial", industrial_pct),
                 ("restricted", restricted_pct)],
                key=lambda x: x[1]
            )[0]

            center_lat = lat + GRID_SIZE/2
            center_lng = lng + GRID_SIZE/2

            clinic_count = 0
            for cl_lat, cl_lng in clinic_points:
                if haversine(center_lat, center_lng, cl_lat, cl_lng) <= radius * 1000:
                    clinic_count += 1

            cells.append({
                "lat": lat,
                "lng": lng,
                "clinic_count": clinic_count,
                "residential_pct": round(residential_pct,4),
                "industrial_pct": round(industrial_pct,4),
                "restricted_pct": round(restricted_pct,4),
                "dominant_type": dominant
            })

            lng += GRID_SIZE
        lat += GRID_SIZE

    outfile = f"grid-{radius}km.json"
    print(f"Saving {outfile} ({len(cells)} cells)...")

    with open(outfile, "w") as f:
        json.dump(cells, f)

print("\nDone.")
