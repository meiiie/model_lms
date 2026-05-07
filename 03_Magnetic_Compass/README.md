# 🧭 Magnetic Compass (Marine Binnacle) - Model Documentation

**Phiên bản:** v1.1 (latest)
**Ngày tạo:** 2026-05-07
**Tác giả:** Maritime VR LMS Project

## 🆕 What's new in v1.1
- ✅ **Glass dome dispersion** - sử dụng Shaders Plus addon's "Dispersion Shader Module"
- ✅ Glass có hiệu ứng IOR 1.45 với rainbow caustic
- ✅ Better Lighting V2 preset áp dụng (Presets_005)
- ⚠️ **Lưu ý:** Dispersion shader chỉ render đẹp trong **Cycles**, Eevee Next chỉ approximate
- ⚠️ Khi export sang Unity: Dispersion node group **không transfer**, cần recreate Unity Shader Graph (recipe trong section 6)

---

## 1. Giới thiệu thiết bị thực tế

**Magnetic Compass** (la bàn từ) là thiết bị định hướng cổ điển trên tàu, dùng nguyên lý từ trường Trái Đất. Vẫn được dùng đến nay như **back-up navigation** khi GPS/gyrocompass hỏng.

### Anatomy

```
         🌅 Sun cover (optional, tháo được)
        ┌───────────────┐
        │  Glass Dome    │ ← Trong suốt, cho phép đọc card
        │  ┌───────────┐ │
        │  │ Compass   │ │ ← Card xoay theo từ trường
        │  │  N E S W  │ │   Floats trong oil
        │  └───────────┘ │
        │       │  │      │ ← Lubber line (mark hướng tàu)
        │      ⚪  ⚪      │ ← Kelvin balls (correction iron)
        │   ●  │  │  ●   │
        ├───────────────┤
        │   PEDESTAL    │ ← Wood binnacle stand
        │   (binnacle)  │
        └───────────────┘
```

### Nguyên lý
- 🧲 **Magnetic North:** Card có nam châm dưới đáy, luôn chỉ về cực bắc từ
- 🌊 **Liquid damping:** Card nổi trong dầu (oil) → giảm dao động khi sóng
- ⚖️ **Gimbal mount:** Bowl được treo gimbal → giữ phẳng dù tàu nghiêng
- 🔧 **Kelvin balls (Iron):** Bù từ trường nhiễu loạn từ thân tàu sắt
- 📍 **Lubber line:** Vạch cố định trên rim bowl, chỉ hướng đi của tàu

### Đọc compass
- Heading = số độ trên card đối diện với lubber line
- N = 000°, E = 090°, S = 180°, W = 270°
- "Course 045" = đang đi hướng Đông Bắc

---

## 2. Thông số kỹ thuật model

### Kích thước
| Chiều | Giá trị | Đơn vị |
|---|---:|---|
| **Pedestal height** | 1100 | mm |
| **Pedestal diameter (top)** | 260 | mm |
| **Pedestal diameter (bottom)** | 360 | mm |
| **Base diameter** | 440 | mm |
| **Bowl diameter** | 180 | mm |
| **Bowl height** | 60 | mm |
| **Compass card diameter** | 150 | mm |
| **Glass dome radius** | 85 | mm |
| **Kelvin ball diameter** | 80 | mm |
| **Kelvin arm length** | 150 | mm (từ center ra) |
| **Total bounding box** | 440×180×1240 | mm |

### Geometry stats
| Chỉ số | Số lượng |
|---|---:|
| Total mesh objects | 11 |
| Total vertices | 1,509 |
| Total faces | ~1,400 |
| Materials | 5 (Wood + Brass + Iron + Glass + Card texture) |
| Compass card texture | 1024×1024 procedural |

---

## 3. Hierarchy

```
MagneticCompass_root (Empty - root pivot)
│
├─── 🏛️ Pedestal (static)
│    ├── compass_pedestal       [Wood teak column]
│    └── compass_base            [Wood base disc]
│
├─── 🧭 Compass (interactive)
│    ├── compass_bowl            [Brass housing - open top]
│    ├── glass_dome              [Glass cover - lifts off]
│    └── compass_card_pivot (Empty - rotates Z axis)
│         └── compass_card        [Disc with N/E/S/W texture]
│
├─── ⚖️ Correction_Spheres
│    ├── kelvin_arm_left + kelvin_ball_left
│    └── kelvin_arm_right + kelvin_ball_right
│
└─── 🔧 Details
     └── lubber_line              [Brass heading reference]
```

---

## 4. Animation Library (5 clips)

| Clip | Frames | Loop? | Mô tả |
|---|:---:|:---:|---|
| `compass_card_idle` | 160 | Yes | Wobble ±2.5° (water/swell motion) |
| `compass_card_360_demo` | 180 | No | Full 360° rotation showcase |
| `compass_swing_north` | 70 | No | Returns to N from any heading (with overshoot) |
| `compass_hard_turn` | 80 | No | Ship turns 90° starboard - card rotates -90° smoothly |
| `compass_tut` | 240 | No | Tutorial: N → E → S → W → N (4 cardinal headings) |

### Tutorial Cinematic
```
Frame 1-30:    Hold North (000°)
Frame 30-70:   Turn to East (090°)
Frame 70-100:  Hold East
Frame 100-140: Turn to South (180°)
Frame 140-170: Hold South
Frame 170-210: Turn to West (270°)
Frame 210-240: Return to North (360°)
```

---

## 5. Custom Properties (glTF Extras)

### MagneticCompass_root
```json
{
  "device_type": "Magnetic_Compass",
  "category": "Navigation",
  "course_topic": "MaritimeVR_Navigation",
  "interactive": true
}
```

### compass_card_pivot (the rotating card)
```json
{
  "part_type": "rotation_pivot",
  "interactive": false,
  "rotation_axis": "Z",
  "function": "compass_card_rotation",
  "controllable_by_script": true
}
```

> 💡 **Note:** Card không bị grab bởi user. Unity script set `card_pivot.localRotation` dựa trên ship's heading.

### glass_dome
```json
{
  "part_type": "glass_cover",
  "interactive": true,
  "vr_action": "lift_to_remove"
}
```

### kelvin_ball_left/right
```json
{
  "part_type": "magnetic_correction_sphere",
  "side": "port" / "starboard",
  "function": "deviation_correction"
}
```

---

## 6. Unity Integration Guide

### Bước 1: Import GLB

### Bước 2: Compass Heading Sync Script

Compass card phải xoay TỰ ĐỘNG dựa trên ship's actual heading (không phải user grab):

```csharp
using UnityEngine;

public class CompassController : MonoBehaviour
{
    [Header("References")]
    [SerializeField] private Transform cardPivot;
    [SerializeField] private Transform shipTransform;  // The ship game object

    [Header("Settings")]
    [SerializeField] private float swingDamping = 5f;  // How quickly card settles
    [SerializeField] private float wobbleAmplitude = 1f;  // Subtle wobble for realism
    [SerializeField] private float wobbleSpeed = 0.5f;

    private float currentDisplayedHeading = 0f;
    private float targetHeading = 0f;
    private float wobbleTime = 0f;

    void Update() {
        // Get ship's actual heading (Y rotation)
        float shipHeading = shipTransform.eulerAngles.y;

        // The compass card rotates OPPOSITE to ship (so N stays pointing magnetic north)
        targetHeading = -shipHeading;

        // Smooth follow with damping (simulating liquid drag)
        currentDisplayedHeading = Mathf.LerpAngle(
            currentDisplayedHeading,
            targetHeading,
            Time.deltaTime * swingDamping
        );

        // Add subtle wobble (sea motion)
        wobbleTime += Time.deltaTime * wobbleSpeed;
        float wobble = Mathf.Sin(wobbleTime) * wobbleAmplitude;

        cardPivot.localRotation = Quaternion.Euler(0, 0, currentDisplayedHeading + wobble);
    }

    public float GetHeadingDegrees() {
        // Return current heading shown on lubber line
        return (-currentDisplayedHeading + 360f) % 360f;
    }

    public string GetHeadingCardinal() {
        float h = GetHeadingDegrees();
        if (h < 22.5 || h >= 337.5) return "N";
        if (h < 67.5)  return "NE";
        if (h < 112.5) return "E";
        if (h < 157.5) return "SE";
        if (h < 202.5) return "S";
        if (h < 247.5) return "SW";
        if (h < 292.5) return "W";
        return "NW";
    }
}
```

### Bước 3: Glass Dome Interaction (optional)

Nếu muốn user "lift" the glass dome to clean/inspect compass:

```csharp
public class GlassDomeInteractor : XRGrabInteractable
{
    [SerializeField] private Transform domeOriginalPosition;
    [SerializeField] private float liftDistance = 0.15f;

    protected override void OnSelectEntered(SelectEnterEventArgs args) {
        base.OnSelectEntered(args);
        // Allow user to lift the dome up
    }

    protected override void OnSelectExited(SelectExitEventArgs args) {
        base.OnSelectExited(args);
        // Snap back to original position when released
        StartCoroutine(SnapBack());
    }

    IEnumerator SnapBack() {
        float t = 0;
        Vector3 startPos = transform.position;
        while (t < 1) {
            t += Time.deltaTime * 3;
            transform.position = Vector3.Lerp(startPos, domeOriginalPosition.position, t);
            yield return null;
        }
    }
}
```

---

## 7. ⚠️ Limitations & Notes

### 7.1. Compass card visibility
- Card có UI texture với compass rose, N/E/S/W markers
- Texture detail có thể khó nhìn ở góc xa
- Trong VR, học viên cúi xuống bowl sẽ thấy rõ
- Nếu cần rõ hơn: tăng emission strength trong Unity

### 7.2. Magnetic correction (Kelvin balls)
- Iron balls là **decorative** - không có physics simulation
- Trong real life: học viên có thể adjust position để correct deviation
- Để LMS lesson "Compass deviation": có thể animate ball di chuyển

### 7.3. Glass dome refraction
- Default IOR 1.05 (nhẹ) để dễ nhìn vào
- Nếu muốn realistic glass: tăng IOR lên 1.45 trong Unity

### 7.4. Heading display
- Real compass có **vạch độ chi tiết** (every 1° hoặc 5°)
- Texture hiện tại có ticks every 5°/10°/30°
- Để zoom-in lesson: nên dùng texture 2048×2048

---

## 8. Render Previews

| File | Mô tả |
|---|---|
| `renders/Compass_hero.png` | 3/4 view - hero shot |
| `renders/Compass_3quarter.png` | Closer 3/4 angle |
| `renders/Compass_topview.png` | Top down (showing card detail) |

---

## 9. Suggested Lessons

| Lesson | Use case |
|---|---|
| **Reading the Compass** | Học viên đọc heading từ card và lubber line |
| **Magnetic Variation** | Compare magnetic vs true north |
| **Compass Deviation** | Adjust Kelvin balls cho ship-specific correction |
| **Course Steering** | Maintain heading using compass (with ship wheel) |
| **Loss of GPS** | Backup navigation scenario |

---

## 10. Changelog

### v1.1 (2026-05-07)
- ✅ **Glass dispersion** via Shaders Plus addon
  - Settings: IOR 1.45, Dispersion Intensity 0.04, Saturation 1.5
  - Internal Reflection enabled
- ✅ **Better Lighting V2 preset** "Presets_005" áp dụng vào scene
- ✅ Re-exported `Compass_VR_v1.1.glb` (154 KB) + `.fbx` (473 KB)
- ⚠️ Dispersion = Cycles-only render quality. Eevee shows approximation.
- ⚠️ Unity recipe: Use **Shader Graph "Refraction Node"** with **chromatic aberration** post-process to mimic dispersion

### v1.0 (2026-05-07)
- ✅ Traditional binnacle với teak wood + brass
- ✅ Glass dome (transparent, refractive)
- ✅ 2 Kelvin balls (correction iron)
- ✅ Procedural compass card texture (1024×1024) với compass rose
- ✅ 5 animation clips
- ✅ Unity heading-sync script template

### Future improvements
- [ ] Variation/deviation indicator
- [ ] Sun cover (removable hood)
- [ ] Pelorus reflector cho bearing readings
- [ ] Gimbal animation (compass tilts when ship rolls)
- [ ] Higher resolution card texture (2048×2048) với readable degree numbers

---

**End of Document**
