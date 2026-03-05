import csv
import json
from shapely.geometry import shape
from shapely.ops import transform
from pyproj import Transformer

POP_FILE = "/Users/zijiaye/Downloads/ResidentPopulationbyPlanningAreaSubzoneofResidenceEthnicGroupandSexCensusofPopulation2020.csv"
GEO_FILE = "planning-areas.geojson"
OUTPUT_FILE = "population-density-by-planning-area.json"


# -----------------------------
# 1️⃣ Extract planning area totals
# -----------------------------
population_totals = {}

with open(POP_FILE, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:
        name = row["Number"].strip()

        if name.endswith(" - Total"):
            raw_value = row["Total_Total"].strip()

            # Skip invalid values like "-"
            if raw_value == "-" or raw_value == "":
                continue

            area = name.replace(" - Total", "").strip().upper()
            population = int(raw_value.replace(",", ""))

            population_totals[area] = population


# -----------------------------
# 2️⃣ Compute land area (SVY21 projection)
# -----------------------------
transformer = Transformer.from_crs("EPSG:4326", "EPSG:3414", always_xy=True)

area_lookup = {}

with open(GEO_FILE, encoding="utf-8") as f:
    geo = json.load(f)

for feature in geo["features"]:
    area_name = feature["properties"]["PLN_AREA_N"].upper()
    geom = shape(feature["geometry"])

    projected = transform(transformer.transform, geom)
    area_sqm = projected.area
    area_km2 = area_sqm / 1_000_000

    area_lookup[area_name] = area_km2


# -----------------------------
# 3️⃣ Compute density
# -----------------------------
output = {}

for area, population in population_totals.items():
    if area in area_lookup:
        area_km2 = area_lookup[area]
        density = population / area_km2 if area_km2 > 0 else 0

        output[area] = {
            "population": population,
            "area_km2": round(area_km2, 3),
            "density_per_km2": round(density)
        }


# -----------------------------
# 4️⃣ Save JSON
# -----------------------------
with open(OUTPUT_FILE, "w") as f:
    json.dump(output, f, indent=2)

print("✅ population-density-by-planning-area.json created.")
