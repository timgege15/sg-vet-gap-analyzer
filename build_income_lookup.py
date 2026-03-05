import csv
import json

INPUT_FILE = "income.csv"
OUTPUT_FILE = "income-by-planning-area.json"

BANDS = [
    "Below_1_000",
    "1_000_1_999",
    "2_000_2_999",
    "3_000_3_999",
    "4_000_4_999",
    "5_000_5_999",
    "6_000_6_999",
    "7_000_7_999",
    "8_000_8_999",
    "9_000_9_999",
    "10_000_10_999",
    "11_000_11_999",
    "12_000_12_999",
    "13_000_13_999",
    "14_000_14_999",
    "15_000_17_499",
    "17_500_19_999",
    "20_000andOver"
]

def band_midpoint(band):
    if band == "Below_1_000":
        return 500
    if band == "20_000andOver":
        return 20000

    # Remove commas
    clean = band.replace(",", "")

    # Split exactly into two income numbers
    parts = clean.split("_")

    # Combine first two parts for lower bound
    low = int(parts[0] + parts[1])

    # Combine last two parts for upper bound
    high = int(parts[2] + parts[3])

    return (low + high) / 2

income_lookup = {}

with open(INPUT_FILE, newline='') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        area = row["Number"]

        if area == "Total":
            continue

        total_households = int(row["Total"])
        midpoint_target = total_households / 2
        cumulative = 0

        for band in BANDS:
            count = int(row[band])
            cumulative += count

            if cumulative >= midpoint_target:
                income_lookup[area.upper()] = band_midpoint(band)
                break

with open(OUTPUT_FILE, "w") as f:
    json.dump(income_lookup, f, indent=2)

print("Income lookup created:", OUTPUT_FILE)
