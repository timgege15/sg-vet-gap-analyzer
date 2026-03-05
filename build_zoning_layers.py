import json

MASTERPLAN_FILE = "/Users/zijiaye/Downloads/MasterPlan2019LandUselayer.geojson"

print("Loading masterplan...")
with open(MASTERPLAN_FILE) as f:
    master = json.load(f)

INDUSTRIAL_ZONES = {
    "BUSINESS 1",
    "BUSINESS 1 - WHITE",
    "BUSINESS 2",
    "BUSINESS 2 - WHITE",
    "BUSINESS PARK",
    "BUSINESS PARK - WHITE",
    "WHITE"
}

# Lean restricted definition
RESTRICTED_ZONES = {
    "PORT / AIRPORT",
    "TRANSPORT FACILITIES",
    "LIGHT RAPID TRANSIT",
    "MASS RAPID TRANSIT",
    "UTILITY",
    "SPECIAL USE",
    "CEMETERY",
    "RESERVE SITE"
}

industrial_features = []
restricted_features = []

print("Filtering zoning layers...")

for feat in master["features"]:
    desc = feat["properties"].get("LU_DESC", "")
    geom = feat["geometry"]

    if geom["type"] not in ["Polygon", "MultiPolygon"]:
        continue

    if desc in INDUSTRIAL_ZONES:
        industrial_features.append(feat)

    if desc in RESTRICTED_ZONES:
        restricted_features.append(feat)

industrial_geojson = {
    "type": "FeatureCollection",
    "features": industrial_features
}

restricted_geojson = {
    "type": "FeatureCollection",
    "features": restricted_features
}

print("Saving industrial-zones.json...")
with open("industrial-zones.json", "w") as f:
    json.dump(industrial_geojson, f)

print("Saving restricted-zones.json...")
with open("restricted-zones.json", "w") as f:
    json.dump(restricted_geojson, f)

print("Done.")
