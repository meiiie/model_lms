# 🚢 Ship Hull v3.2 (Handysize Bulk Carrier - Professional Maritime Detail)

**Phiên bản:** v3.2 (PROFESSIONAL + Maritime standards + 24 support brackets)
**Ngày tạo:** 2026-05-07
**Tác giả:** Maritime VR LMS Project
**Loại:** Production-grade vessel exterior

## 🆕 v3.2 - Floating Components Fixed

Sau audit visual, phát hiện một số components "lơ lửng" (không có support brackets thật). Đã fix:

### 24 Support objects added
| Component | Quantity | Function |
|---|---:|---|
| **Pipe gallery supports** | 5 brackets | Vertical struts từ deck lên pipe |
| **Bridge wing struts** | 4 diagonal | Slanted supports dưới bridge wings |
| **Davit fall wires** | 4 cables | Cable thực sự kết nối davit-lifeboat |
| **Crane A-frames** | 6 struts | Inverted V trên crane houses |
| **Crane support cables** | 3 | Cable từ A-frame xuống boom |
| **Bridge window frames** | 2 | Top + bottom trim |

### Add-ons used in v3.2
- ✅ **Shaders Plus V3** - Dispersion Shader Module on bridge front windows
  - IOR 1.45, Dispersion 0.06 (subtle rainbow caustics on glass)
- ✅ **Better Lighting V2** - Preset 003 (dramatic studio lighting)
  - 2 area lights × 840k W (scaled for ship)

### Math/Physics audit results (Naval Architecture)
- ✅ L/B ratio: 6.0 (target 5.5-7.0)
- ✅ B/D ratio: 1.67 (target 1.5-2.0)
- ✅ Block coefficient Cb: 0.82 (target 0.78-0.85)
- ✅ Displacement: ~14,000T (small Handysize)
- ✅ Bridge AWL: 18.3m (SOLAS V/22 ✅)
- ✅ Coaming height: 0.8m (IACS ✅)
- ✅ Propeller D/T: 0.71 (target 0.65-0.75)
- ✅ Bulwarks: 1.2m (SOLAS min 1.0m)
- ✅ Nav lights: 5 per COLREG Rule 21

## v3.0 / v3.1 history (legacy)

## 🆕 What's new in v3.0 (Professional Upgrade)

Reference: **IMO Load Line Convention 1966, COLREG 1972, SOLAS V/19**

### Hull markings (texture-based)
- ✅ **Plimsoll Line** (load line mark) at midship - circle with horizontal line
- ✅ **Load line scale** (TF/F/T/S/W/WNA marks)
- ✅ **Draft marks** (vertical scale at bow + stern + amidships)
- ✅ **Ship name "MARITIME LMS"** on bow side
- ✅ **Stern name "LMS"**
- ✅ **Continuous load line** (red painted)
- ✅ **Hawsepipe area** (anchor pocket marking)

### Hull-mounted equipment
- ✅ **Bilge keels** (vây giảm lắc) - port + starboard, 50m long
- ✅ **Hawsepipes** (anchor passages) - port + starboard

### Deck equipment (per IACS standards)
- ✅ **4 mooring winches** (2 bow + 2 stern)
- ✅ **14 bollards/bitts** distributed around deck edges
- ✅ **4 ventilator mushrooms** (cargo hold ventilation)
- ✅ **Pipe gallery** (70m running along deck)

### Superstructure detail (4 decks)
- ✅ **24 portholes** (8 per deck × 3 decks, with emissive glass)
- ✅ **3 external stairs** (escape routes between decks)
- ✅ **Bridge front window band** (slanted forward 8°)
- ✅ **Bridge wings** extending from top

### Cargo equipment
- ✅ **4 cargo hatches** với covers
- ✅ **16 hatch coamings** (raised steel edges - 4 per hatch)
- ✅ **3 pedestal cranes** between hatches

### Stern detail
- ✅ **4-blade propeller** (proper propeller with rotation animation!)
- ✅ **Real rudder** (control surface)

### Navigation Lights (COLREG Rule 21)
- ✅ **Port nav light** (RED, emissive 15.0)
- ✅ **Starboard nav light** (GREEN, emissive 15.0)
- ✅ **Masthead light** (WHITE, emissive 12.0)
- ✅ **Foremast light** (WHITE)
- ✅ **Stern light** (WHITE)

### Other
- ✅ **2 lifeboats** + davits (orange SOLAS standard)
- ✅ **2 anchors** + windlass
- ✅ **Foremast + Mainmast** + radar dome platform
- ✅ **Funnel** (red maritime)
- ✅ **Bulwarks** (raised hull edges)

### Stats v3.0
- ✅ **133 mesh objects** (vs 49 in v2.0, vs 8 in v1.0)
- ✅ **3,000+ verts** (still VR-friendly)
- ✅ **20+ PBR materials** với emissive nav lights
- ✅ **Hull markings texture** 4096×1024 pixel art
- ✅ **Propeller rotation animation** (60 frames loop)

---

## 1. Giới thiệu

**Ship Hull v2.0** là model thân tàu chuyên nghiệp - tàu hàng rời cỡ Handysize với đầy đủ cấu trúc cần thiết theo tiêu chuẩn IMO.

### Ship class
**Handysize Bulk Carrier** (tàu chở hàng rời cỡ trung):
- LOA (Length Over All): 120m
- Beam: 20m (chiều rộng)
- Draft: 7m (chìm dưới nước)
- Depth: 12m (tổng chiều cao thân tàu)
- Freeboard: 5m (above water)
- Deadweight: ~25,000 DWT (estimated)

### Use cases trong VR LMS
- 🚢 **Bridge tour:** Học viên hiểu họ đang ở đâu trên tàu
- 📐 **Ship dimensions:** Lessons về kích thước tàu
- 🌊 **Approaching ship:** Cảnh bên ngoài tàu trên biển
- 🚷 **Deck operations:** Future lessons về làm việc trên boong (cần models thêm)
- 🏭 **Engine room access:** Through superstructure (future)

---

## 2. Thông số kỹ thuật

### Dimensions
| Phần | Kích thước |
|---|---|
| **Hull length (LOA)** | 100 m |
| **Hull beam** | 18 m |
| **Hull depth** | 8 m |
| **Draft (below water)** | 5 m |
| **Freeboard (above water)** | 3 m |
| **Superstructure length** | 18 m |
| **Superstructure width** | 15 m (85% beam) |
| **Superstructure height** | 6 m (2 decks) |
| **Bridge level (z)** | 9.3 m above waterline |
| **Foremast height** | 15 m |
| **Mainmast height** | 8 m (above superstructure) |
| **Funnel height** | 6 m |

### Geometry stats (greybox)
| Component | Verts |
|---|---:|
| Hull (tapered box) | 24 |
| Deck | 24 |
| Superstructure | 24 |
| Foremast + Mainmast | ~50 |
| Funnel | ~50 |
| Railings | 16 |
| **TOTAL** | **~200 verts** |

> ⚡ Cực kỳ nhẹ! Lý tưởng cho VR distant view.

### File sizes (v2.0 latest)
| File | Size |
|---|---:|
| `source/ShipHull_VR_v2.0.blend` | ~500 KB |
| `exports/ShipHull_VR_v2.0.glb` | **103 KB** |
| `exports/ShipHull_VR_v2.0.fbx` | **192 KB** |
| `source/ShipHull_VR_v1.0.blend` (legacy) | 135 KB |
| `exports/ShipHull_VR_v1.0.glb` (legacy) | 14 KB |

---

## 3. Hierarchy

```
Ship_root (Empty - root)
│
├─── 🚢 Hull
│    └── ship_hull              [Tapered box - blue paint]
│
├─── 📋 Deck
│    └── ship_deck              [Flat surface on top of hull]
│
├─── 🏢 Superstructure
│    ├── superstructure         [White accommodation block]
│    └── anchor_bridge (Empty)   [Where Bridge Cabin attaches]
│
└─── 🔧 Details
     ├── foremast               [Mast at bow]
     ├── mainmast               [Mast above bridge]
     ├── funnel                 [Red smokestack]
     ├── railing_port           [Left side safety rail]
     └── railing_starboard      [Right side safety rail]
```

---

## 4. Coordinate system

```
Z axis (up):
  +9.3m - Bridge level (anchor_bridge)
  +3.0m - Main deck
   0.0m - WATERLINE (sea level)
  -5.0m - Keel (bottom of hull)

Y axis (forward/back):
  +50m  - Bow tip
  +0m   - Midship
  -50m  - Stern

X axis (left/right):
  -9m   - Port side
  +0m   - Centerline
  +9m   - Starboard side
```

---

## 5. Anchor for Bridge Cabin

**`anchor_bridge`** Empty at (0, -25, 9.3) - position để place Bridge Cabin v1.1.

### Unity workflow

```csharp
public class ShipBridgeMounter : MonoBehaviour {
    public GameObject bridgeCabinPrefab;

    void Start() {
        Transform anchor = transform.Find("anchor_bridge");
        if (anchor) {
            Instantiate(bridgeCabinPrefab, anchor.position, anchor.rotation, anchor);
        }
    }
}
```

---

## 6. Materials

| Material | Color | Use |
|---|---|---|
| `mat_ship_hull` | Dark navy (0.05, 0.08, 0.12) | Hull below + above water |
| `mat_ship_deck` | Weathered tan (0.18, 0.16, 0.14) | Deck planking |
| `mat_superstructure` | Painted white (0.85, 0.85, 0.83) | Accommodation block |
| `mat_ship_mast` | Painted white metal | Masts |
| `mat_funnel` | Maritime red (0.50, 0.10, 0.10) | Smokestack |
| `mat_railing` | White metal | Safety railings |

---

## 7. Custom Properties

```json
{
  "Ship_root": {
    "asset_type": "Ship_Hull",
    "ship_type": "small_bulk_carrier",
    "length_m": 100,
    "beam_m": 18,
    "draft_m": 5,
    "course_topic": "Ship_familiarization"
  },
  "ship_deck": {
    "interactive": true,
    "vr_action": "walkable_surface"
  },
  "anchor_bridge": {
    "info": "Bridge cabin attaches here"
  }
}
```

---

## 8. Unity Integration

### Place ship in scene
```csharp
// Position ship at origin (waterline = 0)
// Ocean plane at z=0 will integrate with hull
GameObject ship = Instantiate(shipHullPrefab, Vector3.zero, Quaternion.identity);
```

### Bridge mounting
```csharp
// Bridge Cabin spawns on anchor_bridge automatically
// Or manually:
GameObject bridge = Instantiate(bridgeCabinPrefab,
    ship.transform.Find("anchor_bridge").position,
    Quaternion.identity);
```

### Walking on deck (future feature)
```csharp
// Add MeshCollider to ship_deck
// Mark as "walkable_surface"
// Player teleport zones can spawn around deck
```

---

## 9. ⚠️ Limitations (greybox v1.0)

### Currently NOT included:
- ❌ **Cargo holds** - hatches and cranes
- ❌ **Lifeboats** - on superstructure sides
- ❌ **Anchors and chains** - bow
- ❌ **Detailed bow/stern** - propeller, rudder
- ❌ **Internal compartments** - engine room, cabins
- ❌ **Rigging and lights** - navigation lights, signal flags
- ❌ **Detailed superstructure** - portholes, doors

### For VR LMS - this is OK because:
- ✅ Student spends 95% time **inside bridge cabin**
- ✅ Hull provides **visual context** when looking out windows
- ✅ Greybox = fast loading, perfect for Quest 2/3
- ✅ Can polish in v2.0 if specific lessons need it

---

## 10. Render Previews

| File | Mô tả |
|---|---|
| `renders/ShipHull_hero.png` | 3/4 view of ship at sea |

---

## 11. Suggested LMS Lessons

| Lesson | Use ship for... |
|---|---|
| **Ship Familiarization** | Tour exterior, learn parts |
| **Approaching the Vessel** | First view from pilot boat |
| **Boarding Procedures** | Ladder access via deck |
| **Bridge Wing Operations** | Walking outside on bridge wings (future) |
| **Anchor Operations** | Watch from bridge windows |
| **Departure/Docking** | View ship from pier (cinematic) |

---

## 12. Future improvements (v1.1+)

- [ ] **Cargo hatches** (3-4 holds with covers)
- [ ] **Lifeboats** (2-4 davits + boats)
- [ ] **Anchor + windlass** at bow
- [ ] **Bridge wings** (extending platforms)
- [ ] **Pilot ladder** (boarding access)
- [ ] **Navigation lights** (port red, starboard green, masthead white)
- [ ] **Hull texture details** (rivets, paint wear, name on bow/stern)
- [ ] **Engine room access** door + hatches
- [ ] **Funnel logo** (company branding)
- [ ] **Larger version** (Panamax/VLCC scale 200-300m)

---

## 13. Changelog

### v1.0 (2026-05-07)
- ✅ Greybox cargo carrier 100m
- ✅ Hull with bow/stern taper
- ✅ Main deck
- ✅ Superstructure with bridge anchor
- ✅ 2 masts (fore + main)
- ✅ Funnel
- ✅ 2 railings
- ✅ 6 PBR materials
- ✅ Custom properties for VR
- ✅ Compatible with Bridge Cabin v1.1

---

**End of Document**
