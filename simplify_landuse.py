import json
from shapely.geometry import shape, mapping
from shapely.ops import unary_union

INPUT = "ura-landuse-optimized.geojson"
OUTPUT = "ura-landuse-simplified.geojson"

SIMPLIFY_TOLERANCE = 0.0005  # ~50m simplification

print("Loading optimized GeoJSON...")

with open(INPUT) as f:
    data = json.load(f)

simplified_features = []

for feature in data["features"]:
    geom = shape(feature["geometry"])
    simplified_geom = geom.simplify(SIMPLIFY_TOLERANCE, preserve_topology=True)

    simplified_features.append({
        "type": "Feature",
        "properties": feature["properties"],
        "geometry": mapping(simplified_geom)
    })

print("Simplified features:", len(simplified_features))

simplified_geojson = {
    "type": "FeatureCollection",
    "features": simplified_features
}

with open(OUTPUT, "w") as f:
    json.dump(simplified_geojson, f)

print("Saved:", OUTPUT)
