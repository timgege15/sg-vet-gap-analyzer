# 🇸🇬 SG Vet Strategic Gap Analyzer

A spatial analytics tool to identify underserved residential zones in Singapore for potential veterinary clinic expansion.

This project combines:
- Existing veterinary clinic locations
- 1km competition buffers
- URA Master Plan zoning exclusions
- Precomputed spatial grid classification

The result is a fast, production-ready strategic map highlighting residential opportunity zones while excluding industrial and restricted land.

---

## 🎯 Objective

To identify high-potential locations for new veterinary clinics by:

1. Excluding areas within 1km of existing clinics
2. Excluding industrial, defence, transport, and non-residential zones
3. Highlighting underserved residential zones

Designed for flagship site strategy, white-space analysis, and expansion planning.

---

## 📏 Spatial Grid Model

Singapore is divided into fixed grid cells.

Grid resolution:
- 0.0035° latitude/longitude
- ≈ 390m × 390m per cell
- ≈ 0.15 km² per grid cell

Total classified cells: ~1,987

Each cell is classified as:

- 🟢 Residential Opportunity
- 🟠 Industrial / Business (Excluded)
- ⚫ Restricted / Defence (Excluded)

This grid is fully precomputed offline for performance.

---

## 🧠 Methodology

### 1️⃣ Clinic Locations

- Source: AVS registered vet centres list
- Extracted into `locations.js`
- Includes geocoded coordinates

---

### 2️⃣ Zoning Exclusions (URA Master Plan)

Using Master Plan 2019 Land Use layer:

Excluded:
- Industrial / Business zones
- Military / Defence zones
- Special Use
- Utility infrastructure
- Port / Airport areas

Retained:
- Residential
- Residential with Commercial
- Residential / Institution

Zoning is processed offline and NOT loaded in browser.

---

### 3️⃣ Competition Buffer Logic

For each grid cell:

- Compute distance to nearest clinic (Haversine formula)
- If distance ≤ 1,000m → excluded
- If distance > 1,000m → eligible

This creates a clean 1km competition exclusion radius.

---

### 4️⃣ Precomputed Architecture

All heavy GIS logic is processed offline in Python.

Output file:
grid-precomputed.json (~150KB)

The browser only renders:
- Clinic markers
- 1km buffers
- Preclassified grid cells

Load time: ~1–2 seconds.

---

## ⚙️ Architecture

### Offline (Heavy Computation)

`build_precomputed_grid.py`

- Loads URA zoning
- Applies zoning classification
- Applies 1km clinic exclusion
- Generates final grid dataset

---

### Frontend (Lightweight Rendering)

`index.html`

- Loads clinic markers
- Loads precomputed grid
- Renders rectangles via Leaflet
- No heavy GIS parsing in browser

---

## 📁 Project Structure

index.html  
locations.js  
grid-precomputed.json  
generate_clinics.py  
build_precomputed_grid.py  
README.md  

---

## 🔄 How To Regenerate Grid

If clinic data changes:

1. Update `locations.js`
2. Run:
   python3 build_precomputed_grid.py
3. Commit updated `grid-precomputed.json`

---

## 📈 Strategic Use Cases

- Flagship clinic site selection
- White-space analysis
- Competition density mapping
- Urban expansion strategy
- Market prioritisation

---

## ⚠️ Limitations

- Grid approximation (not parcel-level precision)
- Assumes 1km competition radius
- No demographic weighting yet
- Demand proxies not integrated

Future enhancements:
- Pet ownership proxy modeling
- MRT accessibility scoring
- Population weighting
- Ranked candidate shortlist output

---

## 🚀 Live Map

https://timgege15.github.io/sg-vet-gap-analyzer/

---

## 👤 Author

Tim  
Spatial strategy for veterinary expansion planning.

