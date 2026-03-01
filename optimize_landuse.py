import json

INPUT = "/Users/zijiaye/Downloads/MasterPlan2019LandUselayer.geojson"
OUTPUT = "ura-landuse-optimized.geojson"

KEEP = ["RESIDENTIAL", "INDUSTRIAL", "MILITARY", "WATERBODY"]

print("Loading URA GeoJSON...")

with open(INPUT) as f:
    data = json.load(f)

optimized_features = []

for feature in data["features"]:
    lu_desc = feature["properties"].get("LU_DESC", "").upper()

    if any(k in lu_desc for k in KEEP):

        # Reduce properties
        new_feature = {
            "type": "Feature",
            "properties": {
                "LU_DESC": lu_desc
            },
            "geometry": feature["geometry"]
        }

        optimized_features.append(new_feature)

print("Filtered features:", len(optimized_features))

optimized_geojson = {
    "type": "FeatureCollection",
    "features": optimized_features
}

with open(OUTPUT, "w") as f:
    json.dump(optimized_geojson, f)

print("Saved:", OUTPUT)
