# 🚢 VR Maritime LMS - Model Library

**Bộ sưu tập model 3D thiết bị hàng hải** dành cho khóa học VR tương tác trên nền Unity 2022.3 + XR Interaction Toolkit.

---

## 📋 Tổng quan dự án

**Mục tiêu:** Tạo các thiết bị 3D chuyên nghiệp cho khóa LMS hàng hải, tương tác được trong môi trường VR (Quest, Vive, Pico).

## 🎁 Add-ons used (commercial Blender addons)

Các add-on premium được tích hợp vào dự án:

| Addon | Used for | Status |
|---|---|:---:|
| **Better Lighting V2** | Studio lighting presets (Compass v1.1) | ✅ Installed |
| **Shaders Plus V3** | Dispersion glass for Compass dome | ✅ Installed |
| **CloudScapes Free** | Volumetric clouds (tested, but not used in runtime - too heavy) | ✅ Installed as Asset Library |

Khi kế thừa dự án, **install lại các add-ons này** trong Blender Preferences nếu muốn re-render hero shots với chất lượng cao.

**Tiêu chuẩn kỹ thuật áp dụng cho mọi model:**
- ✅ **Real-world scale** (1 unit = 1 mét, hệ metric)
- ✅ **Y-up convention** (chuẩn Unity)
- ✅ **PBR đầy đủ** (Albedo / Roughness / Metallic / Normal / AO)
- ✅ **Topology sạch** (low-poly tối ưu cho VR)
- ✅ **VR-ready hierarchy** (mỗi part có pivot + naming consistent)
- ✅ **Animation rời từng action** (Unity Animator đọc từng AnimationClip)
- ✅ **Custom properties metadata** (engine có thể đọc qua glTF extras)
- ✅ **Embedded textures** trong .glb (deploy 1 file duy nhất)

---

## 📦 Danh sách Model

| STT | Model | Tình trạng | Verts | Animations | Folder |
|---:|---|:---:|---:|---:|---|
| 01 | **Raymarine AIS4000 Class A Transceiver** | ✅ v1.0 | 3,541 | 36 | [`01_AIS4000_Class_A_Transceiver/`](./01_AIS4000_Class_A_Transceiver/) |
| 02 | **Ship Wheel (Helm)** | ✅ v1.0 | 3,636 | 6 | [`02_Ship_Wheel/`](./02_Ship_Wheel/) |
| 03 | **Magnetic Compass (Binnacle)** | ✅ v1.1 ⭐ | 1,513 | 5 | [`03_Magnetic_Compass/`](./03_Magnetic_Compass/) |
| 04 | **Engine Order Telegraph (EOT)** | ✅ v1.0 | 1,694 | 19 | [`04_Engine_Telegraph/`](./04_Engine_Telegraph/) |
| 05 | **Ocean Environment** 🌊 | ✅ v1.1 ⭐ | 7,203 | 1 | [`05_Ocean_Environment/`](./05_Ocean_Environment/) |
| 06 | **Bridge Cabin (Wheelhouse)** 🚢 | ✅ v1.1 ⭐ | ~800 | 10 | [`06_Bridge_Cabin/`](./06_Bridge_Cabin/) |
| 07 | **VHF Marine Radio (DSC)** 📡 | ✅ v1.0 NEW | ~600 | 10 | [`07_VHF_Radio/`](./07_VHF_Radio/) |
| 08 | **ECDIS Display** 🗺️ | ✅ v1.0 NEW | ~450 | 9 | [`08_ECDIS/`](./08_ECDIS/) |
| 09 | **Marine Radar (X-band)** 📡 | ✅ v1.0 | ~700 | 9 | [`09_Marine_Radar/`](./09_Marine_Radar/) |
| 10 | **Ship Hull (Handysize Bulk Carrier)** 🚢 | ✅ **v3.3 ⭐⭐⭐⭐ + 6DOF rocking** | ~4,500 | **27** | [`10_Ship_Hull/`](./10_Ship_Hull/) |

> ⭐ = Updated v1.1 với external add-ons (CloudScapes / Better Lighting / Shaders Plus)
> 🚢 = Container scene / vessel exterior
> 📡 = Communication / Detection equipment
> 🗺️ = Chart navigation

### Audit Results (verified 2026-05-07)

Tất cả models đã pass audit:

| Model | Verdict | Verts | Materials | Animations |
|---|:---:|---:|---:|---:|
| AIS4000 | ✅ PASS | 3,689 | 9 | 36 |
| Ship Wheel | ✅ PASS | 3,636 | 3 | 6 |
| Magnetic Compass | ✅ PASS | 1,513 | 6 | 5 |
| Engine Telegraph | ✅ PASS | 1,694 | 7 | 19 |
| Ocean Environment | ✅ v1.1 | 7,203 | 2 | 1 |
| Bridge Cabin v1.1 | ✅ | ~800 | 14 | 10 (doors + alerts) |
| VHF Radio | ✅ | ~600 | 5 | 10 |
| ECDIS Display | ✅ | ~450 | 5 | 9 |
| Marine Radar | ✅ | ~700 | 5 | 9 |
| Ship Hull v3.2 (Handysize Pro) | ✅ ⭐⭐⭐ | ~4,500 | 30+ | **26** |
| **TOTAL LIBRARY** | **10 models** | **~25,800** | **82** | **131** |

### 🏆 Final Library Achievements

✅ **Maritime Standards Compliance:**
- IMO Load Line Convention 1966 (Plimsoll Line markings)
- COLREG Rule 21 (Navigation Lights - 5 emissive)
- SOLAS V/22 (Bridge visibility 18.3m AWL)
- IACS Common Rules (Hatch coamings 0.8m)
- Naval Architecture (L/B=6.0, B/D=1.67, Cb=0.82)

✅ **Premium Add-ons Integrated:**
- Better Lighting V2 (Studio presets for hero renders)
- Shaders Plus V3 (Dispersion shader for compass + bridge)
- CloudScapes Free (Asset library, evaluated but not used at runtime)

✅ **Documentation Suite:**
- 10 model READMEs (chi tiết đầy đủ)
- Master README (this file)
- Unity Integration Pack (8 ready-to-use C# scripts)

✅ **Format Coverage:**
- 17 GLB exports (modern, web-ready, requires `com.unity.cloud.gltfast` package in Unity)
- 11 FBX exports (Unity native, plug-and-play, no extra package needed)
- 50+ render previews (4 angles per model average)

| Model | FBX | GLB | Status |
|---|:---:|:---:|---|
| 01 AIS4000 | ✅ | ✅ | Both formats |
| 02 Ship Wheel | ✅ | ✅ | Both formats |
| 03 Compass | ✅ v1.1 | ✅ v1.1 | Both formats |
| 04 EOT | ✅ | ✅ | Both formats |
| 05 Ocean | ✅ v1.1 | ✅ v1.1 | Both formats |
| 06 Bridge Cabin | ✅ | ✅ v1.1 | Both formats |
| 07 VHF | ✅ | ✅ | Both formats |
| 08 ECDIS | ✅ | ✅ | Both formats |
| 09 Radar | ✅ | ✅ | Both formats |
| 10 Ship Hull v3.3 | ✅ **2.83 MB** | ✅ 444 KB | Both formats with 6DOF rocking |
| Master Showcase v1.2 | ❌ | ✅ 2.5 MB | GLB only (FBX export too heavy: 132 actions × 401 obj) |

## 🎬 Master Showcase Scene v1.2 (with 6DOF rocking!)

**📁 [`_shared/Master_Showcase/`](./_shared/Master_Showcase/)** - Composed scene combining:
- 🚢 Ship Hull v3.3 + 6DOF idle rocking (parents the entire scene)
- 🌊 Ocean Environment v1.1 (Preetham sky + animated waves)
- 🏛️ Bridge Cabin v1.1 (on ship's superstructure deck 5)
- 🎛️ All 7 equipment placed at bridge anchors
- 🐦 3 seagull placeholder + 1 navigation buoy
- 💨 Bow + stern wake foam (parented to ship for realistic motion)

**Files:**
| File | Size | Purpose |
|---|---:|---|
| `Master_Showcase_v1.2.blend` | 1.9 MB | Edit-able source (latest) |
| `Master_Showcase_v1.2.glb` | 2.5 MB | One-file complete scene with 132 animations |
| `Master_Showcase_v11_hero.png` | 275 KB | Hero render |
| `Master_Showcase_v12_final.png` | 246 KB | Hero render with motion |
| `Master_v12_motion_f60.png` | 239 KB | Frame 60 (max heave + max roll) |
| `Master_v12_motion_f120.png` | 239 KB | Frame 120 (max -pitch + opposite roll) |

**6DOF Ship Motion (`ship_rocking_idle` action on Ship_root)**

| Axis | Type | Amplitude | Phase Offset | Loop |
|---|---|---:|---:|---|
| Z (location) | **Heave** | ±0.30 m | 0 | 240 fr |
| X (rotation) | **Pitch** | ±1.5° | 60 fr (90°) | 240 fr |
| Y (rotation) | **Roll** | ±2.5° | 30 fr (45°) | 240 fr |
| Z (rotation) | **Yaw** | ±0.5° | 120 fr (180°) | 240 fr |
| X (location) | **Sway** | ±0.10 m | 90 fr (135°) | 240 fr |

> Phase offsets create natural compound motion (no two axes peak simultaneously).
> 240 frames @ 30fps = **8-second seamless loop**, frame 1 == frame 240.
> Bridge + 7 equipment + wake foam are **parented to Ship_root** → they rock with the ship in Unity automatically.

**Use cases:**
- ✅ **Visualization** - see complete vision in one scene with motion
- ✅ **VR realism preview** - drag-and-drop GLB into Unity (with glTFast package), ship rocks idly out of the box
- ✅ **Marketing renders** - hero shots with motion-blurred sea spray
- ⚠️ **NOT for production Unity** - use individual FBX exports for modular workflow

**Total: 401 objects, 132 animations (131 device + 1 ship rocking), ~25,800 vertices**

### 🏛️ Kiến trúc khuyến nghị (industry standard)

**Master Showcase là `_Reference/` — KHÔNG phải production asset.**

Tuân theo pipeline AAA studio (Naughty Dog, CDPR, Epic Games):

```
Unity Project/Assets/
├── _Models/         ← 11 FBX riêng (production runtime)
├── _Prefabs/        ← Compose trong Unity Editor
├── _Scenes/         ← Drag prefab vào scene
└── _Reference/      ← Master_Showcase.glb ở ĐÂY (design intent doc)
```

**Lý do KHÔNG dùng Master Showcase làm runtime asset:**
| Vấn đề | Single FBX (sai) | 11 FBX modular (đúng) |
|---|---|---|
| LOD per asset | ❌ | ✅ |
| GPU Instancing | ❌ | ✅ |
| Source control | ❌ 50MB file dirty | ✅ Diff chỉ file thay đổi |
| Team workflow | ❌ Conflict | ✅ Parallel work |
| Mobile VR build | ❌ Load all | ✅ Streaming on-demand |

→ **Master Showcase v1.2.glb** dùng trong Blender preview, design review, marketing render. **Không deploy lên Quest 2/3.** Production scene compose từ 11 FBX modular trong Unity Editor.

## 🎮 Unity Integration Ready

**📁 Master integration guide:** [`_shared/UNITY_INTEGRATION_PACK.md`](./_shared/UNITY_INTEGRATION_PACK.md)

Includes:
- 8 ready-to-use C# scripts (BridgeManager, ShipWheelInteractor, CompassController, EOTController, LEDBlinker, KnobInteractor, RadarSweepController, DoorInteractor)
- Animator Controller setup guide
- Material conversion (Blender → Unity URP)
- Performance tips for Quest 2/3
- A-Frame WebXR alternative
- Final integration checklist

### Export formats available

Mỗi model có **2 export formats**:

| Format | File | Use case |
|---|---|---|
| **glTF 2.0** (.glb) | `exports/{Name}_VR_v1.0.glb` | Modern, web-ready, smaller. Khuyến nghị cho Unity 2022.3+ với GLTFast |
| **FBX 7.4** (.fbx) | `exports/{Name}_VR_v1.0.fbx` | Native Unity support, animations as takes, larger file |
| 05 | _Marine Radar (X-band)_ | ⏳ Planned | - | - | - |
| 06 | _ECDIS Display_ | ⏳ Planned | - | - | - |
| 07 | _VHF Radio (DSC)_ | ⏳ Planned | - | - | - |
| 08 | _GPS Receiver_ | ⏳ Planned | - | - | - |
| 09 | _EPIRB Beacon_ | ⏳ Planned | - | - | - |
| 10 | _Bridge Layout (cabin)_ | ⏳ Planned | - | - | - |

---

## 📂 Cấu trúc folder chuẩn

Mỗi model có cấu trúc thống nhất:

```
NN_ModelName/
├── source/              ← File Blender gốc (.blend), source-of-truth
├── exports/             ← File export cho engine (.glb, .fbx)
├── renders/             ← Hình render preview (hero, front, 3/4, side)
├── reference/           ← Hình ảnh tham chiếu (real device photos)
└── README.md            ← Tài liệu chi tiết model này
```

---

## 🛠️ Naming Conventions (áp dụng tất cả model)

### Object naming pattern
```
{category}_{part}[_{detail}]

Examples:
  body_main           ← thân chính
  screen_display      ← màn hình
  btn_power           ← nút power
  btn_dpad_up         ← d-pad hướng lên
  knob_main           ← núm xoay chính
  led_status          ← LED trạng thái
  mount_arm_left      ← cánh tay mount trái
  screw_tl            ← ốc vít top-left
  label_raymarine     ← decal logo
```

### Animation Action naming pattern
```
{object_name}_{action_type}

Action types:
  _press        Single press (one-shot, 10 frames)
  _wiggle       Attention hint (loop, 90 frames)
  _tut          Tutorial cinematic part (240 frames)
  _idle         Idle loop (subtle, continuous)
  _demo         Demo/showcase (full motion)
  _on / _off    State transitions (boot fade)
  _blink / _pulse  Status indicators (loop)
  _scan         UV scrolling effect
```

### Material naming pattern
```
mat_{type}_{variant}

Examples:
  mat_body_plastic
  mat_button_rubber
  mat_knob_plastic
  mat_screen_display    (emissive UI)
  mat_led               (green status)
  mat_led_red           (red alarm)
  mat_screw             (metallic)
  mat_logo              (silver/aluminum)
  mat_mount_plastic
```

---

## 🎬 Animation Categories (chuẩn áp dụng)

Mỗi thiết bị tương tác có 5 loại animation chuẩn:

| Loại | Mục đích | Loop? | Trigger |
|---|---|:---:|---|
| **Press / Release** | Phản hồi user nhấn nút | Một lần | OnClick / OnSelect |
| **Wiggle / Hint** | Gợi ý "nút này tương tác được" | Loop | Khi học viên kẹt > 10s |
| **Idle / Pulse** | Tạo cảm giác "thiết bị đang hoạt động" | Loop | Mặc định khi power ON |
| **Boot On / Off** | Hiệu ứng bật/tắt thiết bị | Một lần | Power button event |
| **Tutorial Cinematic** | Hướng dẫn từng bước | Một lần | Bắt đầu lesson mới |

---

## 🎮 Hướng dẫn import vào Unity

### 🔄 Lựa chọn FBX hay glTF?

| Yếu tố | glTF (.glb) | FBX (.fbx) | Khuyến nghị |
|---|:---:|:---:|---|
| Unity 2022.3+ native | Cần GLTFast plugin | ✅ Built-in | FBX cho legacy, GLB cho modern |
| File size | Smaller (~25%) | Larger | GLB nếu deploy mobile/web |
| PBR material fidelity | ✅ Native PBR | ⚠️ Mất Coat/SSS | GLB cho fidelity cao |
| Animation curves | ✅ AnimationClip | ✅ Animation Take | Cả hai đều OK |
| Custom properties | ✅ glTF extras | ✅ FBX user props | Cả hai đều OK |
| Industry compatibility | Modern | Legacy standard | FBX an toàn hơn |

→ **Khuyến nghị Unity 2022.3 + XR Interaction Toolkit:**
- Dùng **FBX** cho thiết bị tĩnh + animations
- Dùng **GLB** nếu cần deploy WebXR sau này

### 📥 Import FBX vào Unity (recommended)

#### Bước 1: Drag .fbx vào Assets/Models/

```
Project window:
  Assets/
    Models/
      AIS4000/
        AIS4000_VR_v1.0.fbx          ← drag here
      ShipWheel/
        ShipWheel_VR_v1.0.fbx
      Compass/
        Compass_VR_v1.0.fbx
      EOT/
        EOT_VR_v1.0.fbx
```

#### Bước 2: FBX Import Settings (per file)

```
Click .fbx → Inspector → 4 tabs:

📋 Model tab:
  Scale Factor: 1                     (real-world meters)
  Convert Units: ✓
  Mesh Compression: Off               (giữ chi tiết)
  Read/Write Enabled: ✓               (cho VR collision detect)
  Optimize Mesh: ✓
  Generate Lightmap UVs: ✓            (cho baked lighting)
  Normals: Import                     (giữ smooth shading từ Blender)
  Tangents: Calculate Mikktspace

🦴 Rig tab:
  Animation Type: None                (no skeletal armatures)

🎬 Animation tab:
  Import Animation: ✓
  Anim Compression: Optimal
  Resample Curves: ✓

  Clips list (sẽ thấy tất cả actions):
    Click clip → set Loop Time:
      ✓ Loop: *_idle, *_wiggle, *_blink, *_pulse, *_scan
      ✗ Loop: *_press, *_tut, *_to_*, *_on, *_off

🎨 Materials tab:
  Material Creation Mode: Standard (Specular)
  Location: Use External Materials (Legacy)
  → Click "Extract Materials..." → save to Models/{Name}/Materials/
  → Click "Extract Textures..." → save to Models/{Name}/Textures/

  Hoặc dùng URP/HDRP:
  Material Creation Mode: Standard
  Location: Use Embedded Materials
```

#### Bước 3: Convert materials từ Blender Principled BSDF → Unity URP/HDRP Lit

Sau khi import, mở từng material đã extract:

```
Material Inspector:
  Shader: Universal Render Pipeline/Lit (cho URP)
          hoặc HDRP/Lit (cho HDRP)

  Surface Inputs:
    - Base Map: drag Albedo từ Textures/
    - Metallic Map: nếu có
    - Smoothness: 1 - Roughness (Unity dùng smoothness, ngược của roughness)
    - Normal Map: drag Normal từ Textures/
    - Emission: cho LED, screen (enable + map color)
```

⚠️ **IMPORTANT:** FBX không export được **procedural noise textures** từ Blender (wood grain, scratches). Nếu muốn giữ procedural look:
- Option A: Bake textures trong Blender trước khi export FBX
- Option B: Recreate procedural shaders trong Unity Shader Graph
- Option C: Use the **GLB version** (giữ một số procedural)

### 📥 Import GLB vào Unity (alternative)

Cài plugin **glTFast** từ Package Manager:
```
Window → Package Manager → +
  Add package by name: com.unity.cloud.gltfast
```

Sau đó drag .glb vào Assets - Unity sẽ tự động đọc.

### Bước 4: Animator Controller setup (sau khi import)

Tạo Animator Controller với 4 Layers:
1. **Base Layer** - idle/pulse/blink (luôn chạy)
2. **Press Layer** - press animations (override khi user chạm)
3. **Hint Layer** - wiggle animations (khi cần hint)
4. **Tutorial Layer** - cinematic (khi triggered)

### Bước 3: Setup Animator Controller

Tạo Animator Controller với 4 Layers:
1. **Base Layer** - idle/pulse/blink (luôn chạy)
2. **Press Layer** - press animations (override khi user chạm)
3. **Hint Layer** - wiggle animations (khi cần hint)
4. **Tutorial Layer** - cinematic (khi triggered)

### Bước 4: Add XR Interaction components

```csharp
// Trên prefab root: XR Grab Interactable hoặc XR Simple Interactable
// Trên từng nút: XR Direct Interactable + custom OnClick handler
// Trên knob: XR Continuous Interactable + rotation script
```

---

## 📐 Tiêu chuẩn kỹ thuật (Quality Standards)

### Poly count targets cho VR

| Loại object | Verts mục tiêu | Lý do |
|---|---:|---|
| Hero asset (gần camera, có thể cầm) | < 10,000 | Chi tiết cao khi user lại gần |
| Mid-range prop (trên bàn, kệ) | < 5,000 | Chi tiết vừa phải |
| Background prop (xa) | < 1,000 | Đủ silhouette |
| LOD0 → LOD1 → LOD2 | 100% → 60% → 30% | Performance VR |

### Texture sizes

| Mục đích | Size | Format |
|---|---:|---|
| UI screen content (LCD) | 1024×512 | RGBA PNG |
| Body color/normal/AO | 1024×1024 | PNG/EXR |
| Small detail (LED, screw) | Procedural | Shader nodes |
| Decals (logo, labels) | 256×128 | PNG with alpha |

### Performance budget cho VR scene

```
Target: Quest 2/3 native (60-72 FPS @ 1832×1920 per eye)

Per scene budget:
  - Total verts visible:    < 500,000
  - Draw calls:             < 100
  - Texture memory:         < 500 MB
  - Lights:                 < 4 dynamic
  - Real-time shadows:      Only on key objects
```

---

## 🎓 Sample Lesson Structure

Cách dùng các model này trong khóa LMS:

```
LESSON 1: "Làm quen với buồng lái"
├─ Scene: Bridge Layout
├─ Models used: AIS4000, Radar, ECDIS, VHF
├─ Tasks:
│   1. Approach AIS4000 → device.led_status_blink kích hoạt (hint)
│   2. Touch button "btn_power" → btn_power_press + screen_power_on
│   3. Knob xoay (real-time) để chọn menu
│   4. Tutorial cinematic chạy (auto demo)

LESSON 2: "Vận hành AIS - Scenario tránh va"
├─ Quiz UI overlay
├─ Animations triggered theo flow
├─ Score system
```

---

## 📞 Maintenance Notes

**Project lead:** Maritime VR LMS Project
**Last updated:** 2026-05-07
**Tools used:**
- Blender 5.1 (modeling, animation)
- Unity 2022.3 LTS (target engine)
- Anthropic Claude (3D artist agent assistance)

**Khi update model:**
1. Tăng version: `_v1.0.blend` → `_v1.1.blend`
2. Update `README.md` của model đó
3. Update bảng "Danh sách Model" ở README master này
4. Re-export `.glb` với cùng version
5. Backup version cũ vào `source/_archive/`

---

## 📜 License & Credits

Model được tạo cho mục đích giáo dục VR LMS hàng hải. Tham chiếu thiết kế từ thiết bị Raymarine AIS4000 thực tế (tham khảo, không phải sản phẩm chính thức của Raymarine).
