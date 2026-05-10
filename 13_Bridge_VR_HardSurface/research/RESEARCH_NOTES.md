# RESEARCH NOTES — VR Maritime Bridge Cockpit (Hard-Surface)

Asset family: `13_Bridge_VR_HardSurface`
Target platform: Meta Quest 3 (Snapdragon XR2 Gen 2), 72 FPS minimum
Date: 2026-05-10

---

## 1. Authoritative sources used

| Tag | Source | Form | Notes |
|-----|--------|------|-------|
| SOLAS V/22 | IMO SOLAS Chapter V Regulation 22 — Navigation Bridge Visibility | Public, free | Legally binding for ship build |
| MSC/Circ.982 | IMO MSC/Circ.982 — Guidelines on ergonomic criteria for bridge equipment and layout | Public, fetched from liscr.com | 33 pages, dimensional table |
| ABS Bridge Ergo (2003) | ABS Guidance Notes on Ergonomic Design of Navigation Bridges | Public, fetched from eagle.org | 116 pages, dual mm/in, most detailed |
| MSC.232(82) | IMO Revised Performance Standards for ECDIS | Public | Display size requirement |
| Quest 3 perf | Meta Horizon OS guidelines + Unity perf studies (2026) | Public | Budget targets |
| ISO 8468:2007 | Ship's bridge layout & associated equipment — Reqs and guidelines | **PAYWALLED** | Only ToC accessible; ABS doc covers equivalent ground |

PDF caches in conversation tool-results dir. Text extracts via `pypdf` 6.4.0.

## 2. Dimensional baseline (everything in millimeters unless noted)

### 2.1 Wheelhouse envelope

| Param | Value | Source |
|-------|-------|--------|
| Clear deck-to-deckhead height | ≥ 2 250 | MSC.CIRC.982 §5.1.x |
| Deckhead equipment lower edge | ≥ 2 100 (open areas, passageways, standing stations) | MSC.CIRC.982 §5.1.x |
| Cross-wheelhouse passage width | ≥ 1 200 | MSC.CIRC.982 §5.1.3.1 / ABS §6.1 |
| Bridge wing door width | ≥ 900 | ABS §6.1 |
| Free passage between adjacent workstations | ≥ 700 | MSC.CIRC.982 §5.1.3.2 / ABS §6.3 |
| Front-bulkhead-to-console passage | preferred ≥ 1 000, min ≥ 800 | MSC.CIRC.982 §5.1.3.3 / ABS §6.4 |

### 2.2 Front windows (visibility, structural)

| Param | Value | Source |
|-------|-------|--------|
| Lower edge above deck | ≤ 1 000 (sitting view over bow) | ABS §3.1 |
| Upper edge above deck | ≥ 2 000, must show horizon for 1 800 eye, even with bow 10° below keel | ABS §3.2.iii |
| Inclination from vertical (top out) | 10° to 25° | SOLAS V/22 + MSC.CIRC.982 + ABS |
| Frame between front windows (no stiffener) | ≤ 150 | ABS §3.4 |
| Stiffener cover frame max | 100 W × 120 D | ABS §3.4 |
| Horizontal sliding windows | NOT allowed | ABS §3.4 |
| Single blind sector | ≤ 10° | SOLAS V/22 |
| Total blind sectors | ≤ 20° | SOLAS V/22 |
| Clear sector between blinds | ≥ 5° | SOLAS V/22 |
| Forward-of-bow blind in ±10° arc | ≤ 5° per sector | MSC.CIRC.982 §5.1.1.1.5 |

### 2.3 Eye height + reference person (DRIVES VR HMD spawn)

| Param | Value | Source |
|-------|-------|--------|
| Standing eye height (preferred) | **1 800** | SOLAS V/22 + MSC.CIRC.982 + ABS |
| Standing eye height (min allowed) | 1 600 | SOLAS V/22 |
| Reference person stature | 1 900 | ABS §3.2.iii |
| Distance from bulkhead to reference standing pos | 750 | ABS §3.2.iii |
| 95th %ile NE/NA male standing eye | ≈ 1 750 | ABS §3.2 |
| 95th %ile NE/NA male seated eye | 850–853 | ABS §1.5 |

### 2.4 Console (single-operator, the dominant unit)

| Param | Value | Source |
|-------|-------|--------|
| Console top max height (standing op) | **1 200** | MSC.CIRC.982 §5.3.1.4 / ABS §3.5 |
| Console top height for sitting-only | 1 200 − 200 = **1 000** | ABS Fig. 1 note 3 |
| Console max width (single person) | ≤ 1 600 | ABS §3.2 |
| Upper leg-room depth (under top) | ≥ 450 | MSC.CIRC.982 §5.3.1.5 / ABS §3.6 |
| Lower leg-room depth (foot well) | ≥ 600 | MSC.CIRC.982 §5.3.1.5 / ABS §3.6 |
| Knee-well width | preferred 600, min 500 | ABS Fig. 1 note 2 |
| Forward control reach (frequent/precise) | ≤ 675 from console front edge | MSC.CIRC.982 §5.3.x / ABS §7.1 |

### 2.5 Chart table (planning/documentation workstation)

| Param | Value | Source |
|-------|-------|--------|
| Width | ≥ 1 200 | ABS §3.7 |
| Depth | ≥ 850 | ABS §3.7 |
| Height | 900–1 000 | ABS §3.7 |
| Chart-overhang slit | 100 along front + back | ABS §3.7 |

### 2.6 Display reading distances (drives screen sizing)

| Display class | Min reading distance | Char height rule | Source |
|---|---|---|---|
| Instruments tied to controls | ≥ 1 000 | char ≥ 3.5 × visual angle | ABS §8.10.2 |
| Other instruments | ≥ 2 000 | same | ABS §8.10.2 |

### 2.7 ECDIS-specific (MSC.232(82))

| Param | Value | Source |
|-------|-------|--------|
| Effective chart presentation area | ≥ **270 × 270 mm** (square) | MSC.232(82) Mod. B |
| Color + resolution | per IHO S-52 | MSC.232(82) |

### 2.8 Field of vision per workstation

| Workstation | Horizontal FoV | Source |
|---|---|---|
| Navigating & manoeuvring | ≥ 225° (right ahead → 22.5° abaft beam each side) | MSC.CIRC.982 §5.1.1.1.3 |
| Monitoring | from 90° port bow → 22.5° abaft starboard | MSC.CIRC.982 §5.1.1.1.4 |
| Bridge wing | ≥ 225° (45° opposite bow → astern same side) | SOLAS V/22 |
| Manual steering (helm) | from right ahead to ≥ 60° each side | SOLAS V/22 + MSC.CIRC.982 |

### 2.9 Workstation positioning convention

- **Navigating & manoeuvring**: starboard side
- **Manual steering (helm)**: ship centre-line preferred (small offset to starboard if obstructed)
- **Monitoring**: port side
- **Docking**: bridge wings (port + starboard)
- **Planning / documentation (chart table)**: separated from primary nav stations
- **Communications**: separated, no alarm bleed into navigating station

### 2.10 Environment (informational, low priority for VR visual)

- Air temp: 21–27°C summer, 18–24°C winter
- Humidity: ~45% @ 21°C
- Vertical temp gradient: ≤ 5°C floor-to-head

## 3. Quest 3 VR performance budget (target rig)

| Resource | Comfortable | Stretch ceiling |
|---|---|---|
| Draw calls / frame | 200–400 | 500–800 |
| Triangles / frame total | 500 K – 750 K | (LOD mandatory) |
| Triangles per single mesh | 100 K – 200 K (max for hero) | |
| Texture: hero size | 2048 × 2048 ASTC | |
| App RAM (of 8 GB) | 4 – 6 GB usable | |
| Frame rate | **72 FPS minimum**, 90 FPS goal | |
| Foveated rendering gain | -15% to -25% GPU @ L2 | -30%+ @ L4 |

## 4. Per-asset budget plan (derived from §3 and bridge module list)

Total scene target: 5 consoles + structure + glass + lighting + props ≈ **≤ 500 K tris** in primary view.

| Module | Tri target | Material count | Texture sets |
|---|---|---|---|
| BR_Structure (bulkhead/deck/ceiling) | ~ 30 K | 2 | 1 atlas 2K |
| BR_Glass (windows + mullions) | ~ 15 K | 2 (glass + frame) | 1 atlas 2K |
| BR_Console_Helm | ~ 80 K | 1 (atlas) | 1 atlas 2K |
| BR_Console_ECDIS (×2) | ~ 60 K each | 1 (shared atlas) | shared 2K + 1 emissive screen 1K |
| BR_Console_Radar (×2) | ~ 60 K each | 1 (shared atlas) | shared 2K + 1 emissive screen 1K |
| BR_Console_Engine (telegraph) | ~ 50 K | 2 (existing asset) | from `04_Engine_Telegraph` |
| BR_Compass_Binnacle | ~ 30 K | 2 | from `03_Magnetic_Compass` |
| BR_Lighting (lights are runtime) | n/a | n/a | n/a |
| **Total** | **≈ 445 K** | **~10 unique materials** | **~5 atlases** |

Headroom ~55 K tris for misc (railings, switches, name plates).

## 5. Reuse from existing model_lms slots

Re-use, do NOT remodel:
- `02_Ship_Wheel` → import as helm wheel mesh
- `03_Magnetic_Compass` → binnacle + card
- `04_Engine_Telegraph` → engine telegraph station
- `07_VHF_Radio` → comms console face
- `08_ECDIS` → ECDIS panel reference (texture or mesh)
- `09_Marine_Radar` → radar panel reference
- `11_Bridge_Alarm_Panel` → alarm panel inset

New work in `13_Bridge_VR_HardSurface`:
- Wheelhouse envelope (bulkhead, deck, ceiling)
- Front windows + mullions
- Console housings (the steel boxes that hold the existing equipment)
- Console kit pieces (panel base, screen bezel, switch cluster)
- Bridge wing extensions (optional V2)

## 6. Open questions (for next research pass if needed)

- ISO 8468:2007 numerical specs that ABS may not cover (ABS is largely a US restatement of IMO + ISO)
- IHO S-52 color presentation specifics (drive ECDIS screen content textures)
- IEC 62288:2022 specific symbol/font sizing (drive UI texture work)
- Quest 3 specific ASTC block size recommendations (4×4 vs 6×6 vs 8×8 trade-off)

## 7. Deliverable status

- [x] Phase 0: scene clean, units METRIC/m, 11 collections, AgX color
- [x] Phase 1: this dossier
- [ ] Phase 2: blueprint plane in REFERENCE collection, modular asset list locked
- [ ] Phase 3: kit core (panel base, bezel x3, switch cluster)
- [ ] Phase 4: PBR materials + HDRI + glass
- [ ] Phase 5: VR validation + Unity export
