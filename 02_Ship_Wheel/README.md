# 🎡 Ship Wheel (Helm) - Model Documentation

**Phiên bản:** v1.0
**Ngày tạo:** 2026-05-07
**Tác giả:** Maritime VR LMS Project

---

## 1. Giới thiệu thiết bị thực tế

**Ship Wheel** (vô lăng tàu / bánh lái) là thiết bị cơ khí cổ điển dùng để điều khiển hướng đi của tàu. Thợ lái (helmsman) xoay wheel → bánh lái dưới tàu xoay tương ứng → tàu đổi hướng.

### Lịch sử & ý nghĩa
- 🚢 **Truyền thống:** Tất cả tàu buồm, tàu hơi nước thế kỷ 18-19 đều dùng wheel
- ⚙️ **Hiện đại:** Tàu thương mại lớn dùng joystick/electric helm, nhưng vẫn có wheel dự phòng (emergency steering) và đào tạo
- 🎓 **LMS:** Quan trọng cho lessons "Steering basics", "COLREG (Rules of the Road)", "Course keeping"

### Hoạt động
- **Số vòng từ port to starboard** (lock-to-lock): thường 2-3 vòng (~720°-1080°)
- Mỗi vòng wheel = ~15° rudder change
- "Hard a-port" = quay hết về trái, "Hard a-starboard" = hết về phải
- "Midships" = wheel ở vị trí 0° (rudder thẳng)

---

## 2. Thông số kỹ thuật model

### Kích thước
| Chiều | Giá trị | Đơn vị |
|---|---:|---|
| **Wheel diameter** | 700 | mm (cả handles) |
| **Rim radius** | 350 | mm |
| **Hub diameter** | 100 | mm |
| **Spokes** | 8 cái radial | |
| **Handle ball diameter** | 50 | mm |
| **Pedestal height** | 1100 | mm |
| **Wheel center từ floor** | 1500 | mm (chest height) |
| **Total bounding box** | 700×80×1550 | mm (W×D×H) |

### Geometry stats
| Chỉ số | Số lượng |
|---|---:|
| Total mesh objects | 19 |
| Total vertices | 3,632 |
| Total faces | 3,536 |
| Materials | 2 (Wood + Brass) |

---

## 3. Hierarchy đầy đủ

```
ShipWheel_root (Empty - root pivot)
│
├─── 🎡 Wheel (rotates as one unit)
│    └── wheel_pivot (Empty - rotation axis Y)
│         ├── wheel_hub          [Brass center]
│         ├── wheel_rim          [Wood torus]
│         ├── wheel_spoke_001-008 [8 wood spokes]
│         └── wheel_handle_001-008 [8 wood ball grips]
│
├─── 🏛️ Pedestal (static)
│    ├── pedestal_column        [Tapered wood stand]
│    ├── pedestal_base          [Round wood base]
│    └── pedestal_cap           [Brass cap top]
│
└─── 🔧 Details (static, chưa có)
```

**Quan trọng:** Toàn bộ wheel xoay quanh `wheel_pivot` (Y axis). Pedestal đứng yên.

---

## 4. Animation Library (6 clips)

| Clip | Frames | Loop? | Mô tả |
|---|:---:|:---:|---|
| `wheel_idle` | 120 | Yes | Subtle wobble ±3° (water motion feel) |
| `wheel_demo_full` | 180 | No | Quay 720° (2 vòng full lock-to-lock) |
| `wheel_hard_port` | 60 | No | Quay -360° hết về trái + hold |
| `wheel_hard_starboard` | 60 | No | Quay +360° hết về phải + hold |
| `wheel_return_center` | 45 | No | Spring-back to 0° với overshoot |
| `wheel_tut` | 240 | No | Cinematic: showing ship steering scenarios |

### Tutorial timeline (`wheel_tut`)
```
Frame 1-30:    Small port turn (-30°) and back
Frame 30-60:   Return to center
Frame 60-100:  Starboard +90° turn
Frame 100-130: Settle at +15°
Frame 130-180: Hard port -180°
Frame 180-220: Recovery
Frame 220-240: Settle at center
```

---

## 5. Custom Properties (glTF Extras)

### ShipWheel_root
```json
{
  "device_type": "Steering_Wheel",
  "category": "Helm",
  "manufacturer": "Traditional",
  "course_topic": "MaritimeVR_Steering",
  "interactive": true
}
```

### wheel_pivot (rotation pivot)
```json
{
  "part_type": "rotation_pivot",
  "interactive": true,
  "vr_action": "grab_and_rotate",
  "rotation_axis": "Y",
  "max_lock_degrees": 720,
  "spring_back_to_center": false,
  "function": "ship_helm_wheel"
}
```

### wheel_handle_001-008
```json
{
  "part_type": "handle",
  "handle_number": 1-8,
  "interactive": true,
  "vr_action": "grip_point"
}
```

→ User grab BẤT KỲ handle nào → wheel_pivot rotates around Y axis

---

## 6. Unity Integration Guide

### Bước 1: Import GLB vào Assets/Models/ShipWheel/

### Bước 2: Animator Controller setup

```
Layer 0 "Idle":
  Default state: wheel_idle (loop)

Layer 1 "Override" (override mode):
  States:
    - wheel_demo_full
    - wheel_hard_port
    - wheel_hard_starboard
    - wheel_return_center
    - wheel_tut
  Triggers: PlayDemo, PlayHardPort, PlayHardStarboard, ReturnCenter, PlayTutorial
```

### Bước 3: Real-time grab+rotate script

**KEY POINT:** Animations chỉ là DEMO. Tương tác thật trong VR phải là procedural rotation.

```csharp
using UnityEngine;
using UnityEngine.XR.Interaction.Toolkit;

[RequireComponent(typeof(XRGrabInteractable))]
public class ShipWheelHelm : MonoBehaviour
{
    [SerializeField] private Transform wheelPivot;
    [SerializeField] private float maxLockDegrees = 720f;
    [SerializeField] private bool springBackToCenter = false;
    [SerializeField] private float springSpeed = 90f;

    [Header("Events")]
    public UnityEvent<float> OnRudderAngleChanged; // -1 to +1
    public UnityEvent OnHardPort;
    public UnityEvent OnHardStarboard;
    public UnityEvent OnMidships;

    private float currentAngle = 0f;
    private XRGrabInteractable grab;
    private Vector3 lastInteractorRight;
    private bool isGrabbed = false;

    void Awake() {
        grab = GetComponent<XRGrabInteractable>();
        grab.selectEntered.AddListener(OnGrabbed);
        grab.selectExited.AddListener(OnReleased);
    }

    void OnGrabbed(SelectEnterEventArgs args) {
        isGrabbed = true;
        var interactor = args.interactorObject.transform;
        lastInteractorRight = transform.InverseTransformDirection(interactor.right);
    }

    void OnReleased(SelectExitEventArgs args) {
        isGrabbed = false;
    }

    void Update() {
        if (isGrabbed) {
            UpdateRotationFromInteractor();
        } else if (springBackToCenter && Mathf.Abs(currentAngle) > 0.1f) {
            // Spring back to center
            currentAngle = Mathf.MoveTowards(currentAngle, 0, springSpeed * Time.deltaTime);
            ApplyRotation();
        }
    }

    void UpdateRotationFromInteractor() {
        var interactor = grab.interactorsSelecting[0].transform;
        Vector3 currentInteractorRight = transform.InverseTransformDirection(interactor.right);

        // Calculate angle between last and current orientations (around Y axis)
        float angleDelta = Vector3.SignedAngle(lastInteractorRight, currentInteractorRight, Vector3.up);

        currentAngle += angleDelta;
        currentAngle = Mathf.Clamp(currentAngle, -maxLockDegrees, maxLockDegrees);

        // Trigger threshold events
        if (currentAngle <= -maxLockDegrees + 1) OnHardPort?.Invoke();
        if (currentAngle >= maxLockDegrees - 1) OnHardStarboard?.Invoke();
        if (Mathf.Abs(currentAngle) < 5) OnMidships?.Invoke();

        // Notify rudder system
        float normalizedRudder = currentAngle / maxLockDegrees;  // -1 to +1
        OnRudderAngleChanged?.Invoke(normalizedRudder);

        ApplyRotation();
        lastInteractorRight = currentInteractorRight;
    }

    void ApplyRotation() {
        wheelPivot.localRotation = Quaternion.Euler(0, currentAngle, 0);
    }
}
```

### Bước 4: XR Setup
- Add **XR Grab Interactable** trên `ShipWheel_root`
- Add **Sphere Collider** trên mỗi `wheel_handle_*` (radius ~30mm)
- Tag handles để script biết user đang grab handle nào

---

## 7. ⚠️ Limitations & Notes

### 7.1. Animation vs Real Interaction
- 6 animations là DEMO/cinematic only
- Real-time steering trong VR phải dùng procedural script (xem code trên)
- Animations dùng cho: tutorial, demo video, idle when not interacted

### 7.2. Lock-to-lock degrees
- Default: 720° (2 vòng)
- Có thể chỉnh trong Unity script: `maxLockDegrees`
- Real ships có 1-3 vòng tùy size

### 7.3. Spring-back behavior
- Property `spring_back_to_center` mặc định FALSE
- Set TRUE cho: lifeboat helm, emergency steering
- Set FALSE cho: regular merchant ship helm (giữ vị trí)

### 7.4. Handle interaction details
- 8 handles - bất kỳ handle nào cũng grab được
- Khi user grip 1 handle, wheel rotates around hub axis
- VR controller hand position drives the rotation

---

## 8. Render Previews

| File | Mô tả |
|---|---|
| `renders/ShipWheel_hero.png` | 3/4 angle - hero shot |
| `renders/ShipWheel_front.png` | Front orthographic (showing 8-spoke design) |

---

## 9. Suggested Lessons sử dụng Ship Wheel

| Lesson | Use case |
|---|---|
| **Steering Basics** | Player practice quay wheel, hold heading |
| **COLREG (Rules of the Road)** | Avoid collision scenarios bằng wheel |
| **Course Keeping** | Maintain heading dù sóng/gió |
| **Hard Maneuvers** | Hard a-port, crash stop |
| **Emergency Steering** | Manual helm khi mất hydraulic |

---

## 10. Changelog

### v1.0 (2026-05-07)
- ✅ 8-spoke traditional wheel với mahogany + brass
- ✅ Pedestal stand 1.1m height
- ✅ 6 animation clips
- ✅ Custom properties metadata
- ✅ Real-time grab-and-rotate script template (Unity C#)

### Future improvements
- [ ] Damage/wear states (used vs new)
- [ ] Smaller modern hydraulic wheel variant (300mm diameter)
- [ ] Brass plate engraving "S.S. [SHIP NAME]"
- [ ] Bell rope attached (traditional)
- [ ] Compass binnacle behind wheel (layout reference)

---

**End of Document**
