# Cabin Lái Tàu VR — Bridge Cabin Complete v1.0

**Codename:** `bridge-cabin-v1.0`
**Release date:** 2026-05-11
**Asset family:** `13_Bridge_VR_HardSurface/`

---

## 🎯 Đây là model gì?

Một **buồng lái tàu (wheelhouse) hoàn chỉnh** dùng cho VR — không phải một component đơn lẻ mà là **toàn bộ không gian buồng lái** với tất cả thiết bị hàng hải đã đặt vào đúng vị trí, materials, lighting, animations.

Cụ thể bao gồm:

| Thành phần | Mô tả |
|---|---|
| **Cấu trúc buồng** | Sàn 8×5 m, trần cao 2.25 m, 4 vách (front/aft/port/stbd), 5 cửa sổ kính nghiêng 15° |
| **Console array** | Cabinet steel chính dài 7 m gắn dọc front bulkhead, có wood teak kick-plate dưới chân |
| **Ship wheel (vô lăng)** | Bánh lái gỗ + brass handles, gắn trên pedestal, có animation xoay |
| **Magnetic compass** | Binnacle vàng đồng + glass dome + kelvin balls |
| **Engine telegraph (EOT)** | Lever đỏ + sector dial đỏ-xanh trên pedestal |
| **ECDIS displays (×2)** | Màn hình chart navigation, có texture UI thật |
| **Radar displays (×2)** | Màn hình PPI radar, có texture UI thật |
| **AIS, VHF, Alarm panel** | Các thiết bị phụ trợ |
| **Captain's chair** | Ghế thuyền trưởng (xoay được) |
| **Doors** | 2 cửa hông (port + stbd) |
| **Ceiling lights** | 4 đèn trần + 1 sun + HDRI environment |
| **Ocean horizon** | Plane biển 200×200 m visible qua cửa sổ |

## 💡 Tác dụng (use case)

Asset này là **container chính** cho toàn bộ khóa LMS hàng hải VR. Các use cases cụ thể:

1. **Spawn point**: Học viên VR đeo Quest 3 vào, xuất hiện trong buồng lái này
2. **Bài giảng vận hành**: Tương tác với ship wheel, EOT, compass theo lesson script
3. **Mô phỏng watch-keeping**: Đứng trực ca, quan sát ECDIS/radar, ra lệnh telegraph
4. **Drill khẩn cấp**: Alarm panel nhấp nháy, học viên phản ứng
5. **POV review**: Giảng viên xem lại từ camera helmsman hoặc captain seated

Asset bao gồm **5 VR camera anchors** đã setup (Conning Standing/Seated, Helm, Bridge Wing Port/Stbd) — Unity chỉ cần đọc tọa độ Empty objects này để spawn HMD đúng vị trí chuẩn IMO.

## 📐 Tuân thủ chuẩn quốc tế

Toàn bộ kích thước được drive từ:

- **SOLAS V/22** — Navigation Bridge Visibility (legally binding)
- **IMO MSC.CIRC.982** — Bridge Equipment & Layout ergonomics
- **ABS Guidance Notes 2003** — Navigation Bridge Ergonomic Design
- **IMO MSC.232(82)** — ECDIS Performance Standards (chart display ≥270×270 mm)

Eye height VR HMD spawn = **1.80 m** trên deck (per SOLAS V/22). Console max envelope **1.6 × 0.85 × 1.2 m** (per MSC.CIRC.982).

Chi tiết 40+ dimensions xem `research/RESEARCH_NOTES.md`.

## ⚡ Performance

Target platform: **Meta Quest 3** (Snapdragon XR2 Gen 2, ≥72 FPS).

| Metric | Value | Quest 3 budget | Status |
|---|---|---|---|
| Total objects | 201 | — | OK |
| Total polys (render visible) | ~13,225 | 500K-750K | ✅ <3% budget |
| Materials | 58 (named convention `mat_*`) | — | OK |
| Hero textures | 2K ASTC ready | 2K max | ✅ |
| GLB export size | 79 KB (v0.3) | — | tiny |

Kết luận: cực kỳ rảnh budget. Có thể thêm chi tiết khác (wood, decals, wipers) mà vẫn dưới giới hạn.

## 🎬 Animations bao gồm (demo Blender, runtime sẽ làm bằng Unity scripts)

- Ship wheel xoay 720° (2 vòng) trong 8 giây
- Magnetic compass card lắc ±12° (mô phỏng tàu sóng)
- Engine telegraph lever swing qua 4 vị trí (Stop → Slow Ahead → Half Ahead → Stop)
- Captain "sit-down" camera 4 keyframes (entrance → seated POV)
- Alarm panel LED blink

Demo: `research/anim_v5.0_bridge_demo.mp4` (8 sec, 1280×720, 30 fps, 1.4 MB).

## 📂 Files chính

```
13_Bridge_VR_HardSurface/
├── README.md                                      Documentation chung
├── RELEASE_NOTES.md                               File này (release v1.0)
├── source/
│   ├── bridge_v5.0_animated.blend          ⭐    File chính - animations + console + HDRI
│   ├── bridge_v4.0_console_array.blend            v4 không animation (static)
│   ├── bridge_v3.0_hdri_cycles.blend               v3 chưa có console array
│   ├── bridge_v2.0_pivot.blend                     v2 base from 06_Bridge_Cabin
│   └── bridge_v0.1 → v1.0                          v0/v1 parametric scaffold (reference only)
├── exports/
│   └── BridgeVR_HardSurface_v1.0.glb              Unity-ready glTF (79 KB)
└── research/
    ├── RESEARCH_NOTES.md                          40+ engineering dimensions
    ├── anim_v5.0_bridge_demo.mp4           ⭐    Animation demo MP4
    ├── anim_v5.0_keyframe_f001/080/160/240.png    4 keyframe previews
    └── hero_v0.3 → v4.1 (16 PNGs)                 Render iterations qua các phase
```

## 🔧 Cách sử dụng

### Trong Blender (xem/chỉnh sửa)
```
File → Open → 13_Bridge_VR_HardSurface/source/bridge_v5.0_animated.blend
Spacebar → Play animation (xem MP4 sequence)
F12 → Render single frame
Ctrl+F12 → Render full animation
```

### Trong Unity (import vào VR project)
```
1. Drag exports/BridgeVR_HardSurface_v1.0.glb vào Assets/
2. Drop prefab vào MaritimeBridgeLMS scene
3. Đọc Empty objects "VR_Eye_Conning_Standing" etc. để set HMD spawn point
4. Attach Unity grab interactors lên các kit pieces (wheel, switches, knobs)
```

## 🚧 Còn thiếu (roadmap v1.1+)

- Wipers ngoài cửa sổ (modeling pass)
- Mullion details cao cấp hơn
- Marine-specific HDRI (puresky là sky generic, không có ocean line rõ)
- ECDIS UI variants (track plan vs route monitor mode)
- Bridge wing extensions (open-air doors)
- GLB regenerate sau khi Blender 5.1.2+ fix gltf2 exporter bug

## 📜 License & sources

- HDRI `kloppenheim_06_puresky_2k.hdr`: Poly Haven, **CC0**
- ECDIS/Radar UI: generic training UI generated by `image_gen` (no vendor branding)
- AI bridge concept references: AI-generated, modeling direction only (không phải ảnh thật)
- Engineering data: SOLAS V/22, MSC.CIRC.982, ABS, MSC.232(82) — all public IMO/ABS docs
- Asset reuse: 06_Bridge_Cabin (wheel, compass, EOT, ECDIS, AIS, radar, alarm) — internal project asset

Mọi thứ trong asset này dùng được cho **mục đích giáo dục VR LMS hàng hải** không hạn chế.
