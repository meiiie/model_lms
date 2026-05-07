# ⚙️ Engine Order Telegraph (EOT) - Model Documentation

**Phiên bản:** v1.0
**Ngày tạo:** 2026-05-07
**Tác giả:** Maritime VR LMS Project

---

## 1. Giới thiệu thiết bị thực tế

**Engine Order Telegraph (EOT)** = thiết bị **giao tiếp** giữa **buồng lái (bridge)** và **buồng máy (engine room)**.

### Cách hoạt động (cổ điển - cơ khí)

1. **Captain/officer** trên bridge muốn ra lệnh động cơ
2. Move lever → **RED pointer (Ordered)** quay đến vị trí mong muốn
3. **BELL kêu** ở engine room (gây chú ý)
4. **Engineer** ở engine room nhìn dial → đặt **GREEN pointer (Answered)** cùng vị trí
5. Đồng thời điều chỉnh động cơ thực tế
6. Khi 2 pointers trùng vị trí = lệnh đã được ack

### 7 Standard Positions (clockwise from top)

```
              STOP
               │
    SLOW       │       SLOW
    ASTERN ←   ●   →   AHEAD
               │
   HALF        │        HALF
   ASTERN  ←   ●   →    AHEAD
               │
   FULL        │        FULL
   ASTERN  ←   ●   →    AHEAD
```

| Position | Angle (Y) | Engine state |
|---|---:|---|
| **STOP** | 0° | Engine standby |
| **SLOW AHEAD** | +30° | ~25% throttle forward |
| **HALF AHEAD** | +60° | ~50% throttle forward |
| **FULL AHEAD** | +90° | 100% throttle forward |
| **SLOW ASTERN** | -30° | ~25% throttle reverse |
| **HALF ASTERN** | -60° | ~50% throttle reverse |
| **FULL ASTERN** | -90° | 100% throttle reverse (emergency) |

### Modern context
- Hiện đại đã thay bằng **digital throttle/joystick**
- Tuy nhiên EOT vẫn được dùng làm **backup** + **training**
- Cần học vì IMO STCW yêu cầu

---

## 2. Thông số kỹ thuật model

### Kích thước
| Chiều | Giá trị | Đơn vị |
|---|---:|---|
| **Pedestal height** | 1200 | mm |
| **Pedestal diameter** | 200 | mm |
| **Base diameter** | 400 | mm |
| **Dial dome diameter** | 260 | mm |
| **Dome depth** | 60 | mm |
| **Lever handle length** | 180 | mm |
| **Pointer length** (ordered) | 105 | mm |
| **Pointer length** (answered) | 89 | mm |
| **Total bounding box** | 400×260×1500 | mm |

### Geometry stats
| Chỉ số | Số lượng |
|---|---:|
| Total mesh objects | 9 |
| Total vertices | 1,690 |
| Materials | 6 (Pedestal black, Brass, Wood grip, 2 pointers, Dial face) |
| Dial texture | 1024×1024 procedural with color zones |

---

## 3. Hierarchy

```
EOT_root (Empty - root)
│
├─── 🏛️ Pedestal (static)
│    ├── eot_base
│    └── eot_pedestal
│
├─── 🎯 Dome_Display (static)
│    ├── eot_dome           [Brass housing]
│    └── eot_dial_face      [Textured face with positions]
│
├─── 📍 Pointers (rotate independently)
│    ├── pointer_ordered_pivot (Empty - rotates Y)
│    │   └── pointer_ordered  [RED arrow]
│    └── pointer_answered_pivot (Empty - rotates Y)
│        └── pointer_answered [GREEN arrow]
│
├─── 🔧 Handle (interactive)
│    └── handle_lever_pivot (Empty)
│        ├── eot_handle_lever  [Brass bar]
│        └── eot_handle_grip   [Wood ball]
│
└─── 🔔 Details
     └── eot_bell             [Bell on top - decorative]
```

---

## 4. Animation Library (19 clips)

### Position-specific (one-shot, 22 frames each)

| Clip | Target | Mục đích |
|---|---|---|
| `eot_ordered_to_stop` | RED → 0° | Bridge orders STOP |
| `eot_ordered_to_slow_ahead` | RED → +30° | Bridge orders SLOW AHEAD |
| `eot_ordered_to_half_ahead` | RED → +60° | Bridge orders HALF AHEAD |
| `eot_ordered_to_full_ahead` | RED → +90° | Bridge orders FULL AHEAD |
| `eot_ordered_to_slow_astern` | RED → -30° | Bridge orders SLOW ASTERN |
| `eot_ordered_to_half_astern` | RED → -60° | Bridge orders HALF ASTERN |
| `eot_ordered_to_full_astern` | RED → -90° | Bridge orders FULL ASTERN |

Same 7 cho **GREEN** pointer (`eot_answered_to_*`) cho engine room ack.

### Idle animations (loops)

| Clip | Target | Effect |
|---|---|---|
| `eot_ordered_idle` | RED | Subtle vibration ±0.5° (engine running) |
| `eot_answered_idle` | GREEN | Subtle vibration ±0.4° |

### Tutorial cinematic (240 frames)

| Clip | Mô tả |
|---|---|
| `eot_ordered_tut` | Sweep: STOP → SL.AHD → HA.AHD → FU.AHD → STOP → FU.AST → STOP |
| `eot_answered_tut` | Same sequence với 5-7 frames delay (engine room reaction time) |
| `eot_handle_demo` | Lever rocks forward/backward để show interaction |

### Tutorial timeline
```
Frame 1-20:    STOP (engine standby)
Frame 20-60:   ORDER: SLOW AHEAD - bell rings, RED moves first, GREEN follows
Frame 60-100:  ORDER: HALF AHEAD
Frame 100-140: ORDER: FULL AHEAD
Frame 140-170: STOP! (sudden order)
Frame 170-215: EMERGENCY FULL ASTERN (collision avoidance scenario)
Frame 215-240: STOP (resume normal)
```

---

## 5. Custom Properties (glTF Extras)

### EOT_root
```json
{
  "device_type": "Engine_Order_Telegraph",
  "category": "Bridge_Engine_Communication",
  "course_topic": "MaritimeVR_EngineRoom_Communication",
  "interactive": true
}
```

### pointer_ordered_pivot (RED - bridge-controlled)
```json
{
  "part_type": "rotation_pivot",
  "interactive": true,
  "vr_action": "grab_handle_to_rotate",
  "rotation_axis": "Y",
  "color": "red",
  "function": "bridge_orders_engine"
}
```

### pointer_answered_pivot (GREEN - engine-controlled)
```json
{
  "part_type": "rotation_pivot",
  "interactive": false,
  "color": "green",
  "function": "engine_room_acknowledges",
  "controllable_by_script": true
}
```

### handle_lever_pivot
```json
{
  "part_type": "rotation_pivot",
  "interactive": true,
  "vr_action": "grab_lever",
  "function": "moves_ordered_pointer"
}
```

### eot_bell
```json
{
  "part_type": "alert_bell",
  "function": "rings_when_order_changes"
}
```

---

## 6. Unity Integration Guide

### Bước 1: Import GLB

### Bước 2: EOT Controller Script

```csharp
using System.Collections;
using UnityEngine;
using UnityEngine.Events;

public class EOTController : MonoBehaviour
{
    public enum Position {
        FullAstern, HalfAstern, SlowAstern,
        Stop,
        SlowAhead, HalfAhead, FullAhead
    }

    [Header("Pivot References")]
    [SerializeField] private Transform orderedPivot;   // RED - bridge controls
    [SerializeField] private Transform answeredPivot;  // GREEN - engine room
    [SerializeField] private Transform leverPivot;
    [SerializeField] private AudioSource bellSound;

    [Header("Settings")]
    [SerializeField] private float engineResponseDelay = 1.5f; // seconds before ack
    [SerializeField] private float pointerSpeed = 90f;  // degrees per second

    [Header("Events")]
    public UnityEvent<Position> OnOrderChanged;
    public UnityEvent<Position> OnEngineAcknowledged;

    private Position currentOrder = Position.Stop;
    private Position currentAck = Position.Stop;

    static float[] PositionAngles = new float[] {
        -90f,  // FullAstern
        -60f,  // HalfAstern
        -30f,  // SlowAstern
          0f,  // Stop
         30f,  // SlowAhead
         60f,  // HalfAhead
         90f   // FullAhead
    };

    public void SetOrder(Position newOrder) {
        if (newOrder == currentOrder) return;

        currentOrder = newOrder;

        // Ring the bell (notify engine room)
        if (bellSound) bellSound.Play();

        // Animate ordered pointer
        StartCoroutine(RotatePointer(orderedPivot, PositionAngles[(int)newOrder]));

        // Engine room responds after delay
        StartCoroutine(EngineAcknowledge(newOrder));

        OnOrderChanged?.Invoke(newOrder);
    }

    IEnumerator RotatePointer(Transform pivot, float targetDeg) {
        float startDeg = pivot.localEulerAngles.y;
        if (startDeg > 180) startDeg -= 360;

        float duration = Mathf.Abs(targetDeg - startDeg) / pointerSpeed;
        float elapsed = 0;

        while (elapsed < duration) {
            elapsed += Time.deltaTime;
            float t = Mathf.Clamp01(elapsed / duration);
            float ang = Mathf.Lerp(startDeg, targetDeg, EaseOutBack(t));
            pivot.localRotation = Quaternion.Euler(0, ang, 0);
            yield return null;
        }
    }

    IEnumerator EngineAcknowledge(Position order) {
        yield return new WaitForSeconds(engineResponseDelay);
        currentAck = order;
        StartCoroutine(RotatePointer(answeredPivot, PositionAngles[(int)order]));
        OnEngineAcknowledged?.Invoke(order);
    }

    float EaseOutBack(float t) {
        const float c1 = 1.70158f;
        const float c3 = c1 + 1;
        return 1 + c3 * Mathf.Pow(t - 1, 3) + c1 * Mathf.Pow(t - 1, 2);
    }
}
```

### Bước 3: Lever Interaction (XR)

```csharp
public class EOTLeverInteractor : XRBaseInteractable
{
    [SerializeField] private EOTController eot;
    [SerializeField] private Transform leverPivot;
    [SerializeField] private float minAngle = -45f;
    [SerializeField] private float maxAngle = 45f;

    private float currentLeverAngle = 0;

    void Update() {
        if (isSelected) {
            // Get controller Y rotation, map to lever angle
            var ctrl = interactorsSelecting[0].transform;
            currentLeverAngle = Mathf.Clamp(
                Mathf.DeltaAngle(0, ctrl.eulerAngles.x),
                minAngle, maxAngle);

            leverPivot.localRotation = Quaternion.Euler(0, currentLeverAngle, 0);

            // Map lever angle to position (7 positions across 90° range)
            int posIndex = Mathf.RoundToInt((currentLeverAngle + 45) / 90 * 6);
            posIndex = Mathf.Clamp(posIndex, 0, 6);

            eot.SetOrder((EOTController.Position)posIndex);
        }
    }
}
```

### Bước 4: Bell sound

Add **AudioSource** to `eot_bell` GameObject với "ship_bell.wav" clip.

---

## 7. ⚠️ Limitations & Notes

### 7.1. Two-pointer system
- RED (ordered) and GREEN (answered) pointers rotate INDEPENDENTLY
- In real life: bridge controls red, engine room controls green
- In LMS: scenarios can simulate engine room delay/disagreement

### 7.2. Bell mechanics
- Bell here is DECORATIVE (no animation/physics)
- Sound effect handled by Unity AudioSource
- Could add small bell shake animation in future

### 7.3. Lever mapping
- Real EOT lever has detents/clicks at each position
- Unity script can add haptic feedback on detent crossings:
```csharp
// In Update() when crossing detent angle:
if (Mathf.Abs(deltaAngle) > 15f) {
    XRController.SendHapticImpulse(0.5f, 0.05f);
    detentClick.Play();
}
```

### 7.4. 7 vs 9 positions
- Some EOTs có thêm "DEAD SLOW AHEAD/ASTERN" (9 positions)
- Model hiện tại có 7 standard - đủ cho LMS basic
- Nếu cần 9 positions: chỉ cần thêm 2 angles (-15°, +15°)

---

## 8. Render Previews

| File | Mô tả |
|---|---|
| `renders/EOT_hero.png` | 3/4 view at STOP position (rest) |
| `renders/EOT_stop_initial.png` | Closer look at dial at STOP |
| `renders/EOT_full_ahead.png` | Pointer at FULL AHEAD position |
| `renders/EOT_full_astern.png` | Pointer at FULL ASTERN |

---

## 9. Suggested Lessons

| Lesson | Use case |
|---|---|
| **Bridge-Engine Communication** | Use telegraph để communicate orders |
| **Standard Engine Orders** | Học 7 positions + when to use |
| **Emergency Procedures** | EMERGENCY FULL ASTERN (collision avoidance) |
| **Wheelhouse Etiquette** | Ack procedures, response times |
| **Maneuvering Situations** | Departure/arrival, docking sequences |

---

## 10. Changelog

### v1.0 (2026-05-07)
- ✅ 7-position telegraph (STOP + 3 ahead + 3 astern)
- ✅ 2 independent pointers (red ordered, green answered)
- ✅ Brass dome with procedural color zones (green/yellow/red)
- ✅ Lever with grip
- ✅ 19 animation clips (positions + idle + tutorial)
- ✅ Unity controller script template
- ✅ Realistic spring-back overshoot

### Future improvements
- [ ] 9-position version (with DEAD SLOW)
- [ ] Engraved position labels (FULL AHEAD, etc.) on metal dial
- [ ] Bell shake animation when ringing
- [ ] Glass cover over dial face
- [ ] Reply lever (engine room answers via separate lever)

---

**End of Document**
