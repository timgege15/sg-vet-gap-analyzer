import json

INPUT_FILES = [
    "industrial-zones.json",
    "restricted-zones.json"
]

def round_coords(coords, precision=5):
    if isinstance(coords[0], list):
        return [round_coords(c, precision) for c in coords]
    else:
        return [round(coords[0], precision), round(coords[1], precision)]

for filename in INPUT_FILES:
    print(f"Optimising {filename}...")
    with open(filename) as f:
        data = json.load(f)

    for feature in data["features"]:
        geom = feature["geometry"]

        if geom["type"] == "Polygon":
            geom["coordinates"] = [
                round_coords(ring) for ring in geom["coordinates"]
            ]

        elif geom["type"] == "MultiPolygon":
            geom["coordinates"] = [
                [round_coords(ring) for ring in poly]
                for poly in geom["coordinates"]
            ]

    output_file = filename.replace(".json", "-optimized.json")

    with open(output_file, "w") as f:
        json.dump(data, f, separators=(',', ':'))

    print(f"Saved {output_file}")

print("Done.")
