import json

INPUT = "masterplan-full.geojson"
OUTPUT = "ura-zoning-subset.geojson"

# Keywords we want to retain
KEEP_KEYWORDS = [
    "RESIDENTIAL",
    "BUSINESS",
    "WHITE",
    "INDUSTRIAL",
    "SPECIAL",
    "UTILITY",
    "TRANSPORT",
    "PORT",
    "AIRPORT",
    "MILITARY",
    "DEFENCE",
    "WATERBODY",
    "COMMERCIAL"
]

print("Loading full masterplan...")
with open(INPUT) as f:
    data = json.load(f)

filtered_features = []

for feature in data["features"]:
    lu = feature["properties"].get("LU_DESC", "").upper()
    if any(keyword in lu for keyword in KEEP_KEYWORDS):
        filtered_features.append(feature)

print("Original features:", len(data["features"]))
print("Filtered features:", len(filtered_features))

subset = {
    "type": "FeatureCollection",
    "features": filtered_features
}

with open(OUTPUT, "w") as f:
    json.dump(subset, f)

print("Saved zoning subset to", OUTPUT)
