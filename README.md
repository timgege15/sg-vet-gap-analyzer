# SG Vet Gap Analyzer

A strategic spatial decision tool to identify low-competition residential catchments for veterinary clinic expansion in Singapore.

---

## Objective

Identify high-quality residential white-space areas with minimal existing clinic coverage, while excluding industrial and restricted land uses.

This tool supports strategic site screening before detailed feasibility analysis.

---

## Core Concepts

### 1. Competition Radius

Defines the catchment radius used to measure competition intensity.

Available options:
- 1km
- 2km
- 3km

Used to count the number of existing clinics within the selected radius.

Default: **1km**

---

### 2. Max Clinics Within Radius

Defines the maximum allowable number of clinics within the selected competition radius.

Default: **0 clinics**

Interpretation:
- 0 → True white space
- 1 → Very low competition
- 2–3 → Moderate competition
- 4+ → High competition

---

### 3. Min Residential %

Defines the minimum proportion of residential land use within each grid cell.

Default: **70%**

Residential includes:
- Residential
- Residential with Commercial at 1st Storey
- Residential / Institution
- Commercial & Residential (where applicable)

Purpose:
Ensure that opportunity zones represent real population catchment, not mixed-use or marginal zones.

---

## Opportunity Logic

A grid cell is classified as Opportunity if:

- Dominant land use = Residential
- Residential % ≥ threshold
- Clinic count within selected radius ≤ max clinics

Industrial and Restricted zones are excluded from opportunity classification.

---

## Zoning Layers

### Industrial
Includes:
- Business 1
- Business 2
- Business Park
- Port / Airport
- Utility
- Transport Facilities

These are considered non-residential demand zones.

### Restricted
Includes:
- Special Use
- Military areas
- Reserve Site
- Infrastructure zones

These are considered non-deployable.

---

## Grid System

Grid size: ~0.0035 degrees (~350m x 350m)

Each grid cell contains:
- residential_pct
- clinic_count (for 1km, 2km, 3km)
- dominant_type
- zoning overlap metrics

Grids are precomputed for performance.

---

## Site Evaluation Tool

Users can enter a Singapore postal code to:

- Plot location
- Calculate nearest 3 clinics
- Compute competition intensity for:
  - 1km
  - 2km
  - 3km
- Draw visual connection lines

This allows quick tactical site screening.

---

## Architecture

Frontend:
- Leaflet
- Marker clustering
- Preloaded grid JSON

Backend:
- Python precomputation
- Shapely spatial intersection
- Land use classification
- Competition counting

All heavy spatial calculations are done offline for performance.

---

## What This Tool Is

✔ Strategic screening tool  
✔ Competition intensity visualiser  
✔ Residential white-space detector  
✔ Executive decision dashboard  

---

## What This Tool Is Not

✘ Population-weighted demand model  
✘ Revenue forecast engine  
✘ Lease feasibility model  
✘ Pet ownership density model  

Future upgrades may include:
- HDB vs Private differentiation
- Population data integration
- Pet registration proxies
- Income segmentation
- Traffic flow modelling

---

## Recommended Use Flow

1. Start with default strict white-space settings.
2. Relax max clinics if too restrictive.
3. Expand radius to 2km or 3km to test saturation depth.
4. Use site evaluation for shortlisted addresses.
5. Conduct on-ground validation.

---

## Strategic Philosophy

This model prioritises structural coverage gaps over incremental competitive entry.

It is designed for disciplined expansion, not reactive positioning.

---

Author: Internal Strategic Tool  
Version: Enterprise White-Space Mode
