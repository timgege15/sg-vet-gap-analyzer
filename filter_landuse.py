import json

INPUT = "/Users/zijiaye/Downloads/MasterPlan2019LandUselayer.geojson"
OUTPUT = "ura-landuse-filtered.geojson"

KEEP_CATEGORIES = [
    "RESIDENTIAL",
    "BUSINESS PARK",
    "BUSINESS 1",
    "BUSINESS 2",
    "INDUSTRIAL",
    "MILITARY",
    "WATERBODY"
]

print("Loading URA GeoJSON...")

with open(INPUT) as f:
    data = json.load(f)

filtered_features = []

for feature in data["features"]:
    lu_desc = feature["properties"].get("LU_DESC", "")

    for category in KEEP_CATEGORIES:
        if category in lu_desc.upper():
            filtered_features.append(feature)
            break

print("Filtered features:", len(filtered_features))

filtered_geojson = {
    "type": "FeatureCollection",
    "features": filtered_features
}

with open(OUTPUT, "w") as f:
    json.dump(filtered_geojson, f)

print("Saved:", OUTPUT)
