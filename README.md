# 🇸🇬 SG Vet Strategic Gap Analyzer

A spatial analytics tool to identify underserved residential zones in Singapore for potential veterinary clinic expansion.

---

## 🎯 Definition: Residential Opportunity

A **Residential Opportunity** grid cell is defined as:

1. Classified as *Residential* under the URA Master Plan land use layer  
2. NOT located within 1km of any existing registered veterinary clinic  

In other words:

Residential zoning  
+ No nearby competition (1km buffer)  
= Underserved residential catchment  

This provides a structured white-space detection framework for expansion planning.

---

## 📏 Spatial Grid Model

Singapore is divided into fixed grid cells:

- 0.0035° resolution
- ≈ 390m × 390m per cell
- ≈ 0.15 km² per grid cell
- ~1,987 classified cells

Each cell is categorized as:

- 🟢 Residential Opportunity
- 🟠 Industrial / Business (Excluded)
- ⚫ Restricted / Defence (Excluded)

---

## 🧠 Methodology Summary

1. Geocode all registered veterinary clinics  
2. Apply 1km competition exclusion radius  
3. Exclude industrial and restricted zoning  
4. Precompute classification offline  
5. Render lightweight strategic grid in browser  

---

## ⚙️ Architecture

Heavy computation is done offline using:

build_precomputed_grid.py

Frontend only renders precomputed grid:

grid-precomputed.json (~150KB)

Load time: ~1–2 seconds

---

## 📁 Project Structure

index.html  
locations.js  
grid-precomputed.json  
generate_clinics.py  
build_precomputed_grid.py  
README.md  

---

## 🚀 Live Map

https://timgege15.github.io/sg-vet-gap-analyzer/

---

## 👤 Author

Tim  
Spatial strategy for veterinary expansion planning.

