import requests
import time
import json
import csv
from collections import defaultdict

CSV_FILE = "List of clinics 010326 - Sheet1.csv"
OUTPUT_FILE = "locations.js"

def extract_clinics(csv_file):
    clinics = []

    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            clinics.append({
                "name": row["Vet Centre"].strip(),
                "postal": row["Postal Code"].strip(),
                "phone": row["Contact Number"].strip()
            })

    return clinics


def geocode(postal_code):
    url = "https://www.onemap.gov.sg/api/common/elastic/search"
    params = {
        "searchVal": postal_code,
        "returnGeom": "Y",
        "getAddrDetails": "Y",
        "pageNum": 1
    }

    r = requests.get(url, params=params)
    data = r.json()

    if data["found"] == 0:
        return None

    result = data["results"][0]

    return {
        "address": result["ADDRESS"],
        "lat": float(result["LATITUDE"]),
        "lng": float(result["LONGITUDE"])
    }


def main():
    print("Extracting clinics from CSV...")
    clinics = extract_clinics(CSV_FILE)
    print(f"Extracted {len(clinics)} clinic entries.")

    grouped = defaultdict(list)

    for clinic in clinics:
        grouped[clinic["postal"]].append({
            "name": clinic["name"],
            "phone": clinic["phone"]
        })

    locations = []

    print("Geocoding unique postal codes...")
    for i, postal in enumerate(grouped.keys()):
        print(f"[{i+1}/{len(grouped)}] Geocoding {postal}")
        geo = geocode(postal)

        if geo:
            locations.append({
                "postal": postal,
                "address": geo["ADDRESS"] if "ADDRESS" in geo else geo["address"],
                "lat": geo["lat"],
                "lng": geo["lng"],
                "clinics": grouped[postal]
            })

        time.sleep(0.3)

    print(f"Created {len(locations)} physical locations.")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("const locations = ")
        json.dump(locations, f, indent=2)
        f.write(";")

    print("Done. locations.js created.")


if __name__ == "__main__":
    main()
