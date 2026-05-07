# 📡 Raymarine AIS4000 Class A Transceiver - Model Documentation

**Phiên bản:** v1.0
**Ngày tạo:** 2026-05-07
**Tác giả:** Maritime VR LMS Project

---

## 1. Giới thiệu thiết bị thực tế

**AIS (Automatic Identification System)** là hệ thống nhận dạng tự động trên tàu, dùng để:
- 🛰️ Phát/nhận thông tin vị trí, MMSI, hướng, vận tốc của tàu mình và các tàu xung quanh
- 🚢 Hiển thị "target" trên màn hình (radar-like display)
- ⚠️ Cảnh báo khi có nguy cơ va chạm (CPA/TCPA)
- 📡 Liên lạc dữ liệu giữa tàu và bờ (qua VHF)

**Class A** là phân loại bắt buộc cho tàu thương mại > 300GT theo SOLAS.

**Raymarine AIS4000** (model tham chiếu) là thiết bị chuyên nghiệp với:
- Màn hình LCD 5" màu
- D-pad điều hướng + nút OK
- Knob xoay (rotary encoder) cho menu
- 3 nút chức năng (Power, Menu, Back)
- 2 LED trạng thái (status xanh, alarm đỏ)

---

## 2. Thông số kỹ thuật model

### Kích thước
| Chiều | Đo trong Blender | Đơn vị |
|---|---:|---|
| **Rộng (Width / X)** | 178 mm | Body |
| **Sâu (Depth / Y)** | 55 mm | Body |
| **Cao (Height / Z)** | 128 mm | Body |
| **Bounding box** | 194 × 89 × 164 mm | Bao gồm mount |

### Geometry stats
| Chỉ số | Số lượng |
|---|---:|
| Total mesh objects | 25 |
| Total vertices | ~3,700 |
| Total faces | ~2,800 |
| Materials | 9 (PBR đầy đủ) |
| Embedded textures | 1 (UI screen 1024×512) |

### File sizes
| File | Size | Mục đích |
|---|---:|---|
| `source/AIS4000_VR_v1.0.blend` | ~870 KB | Source-of-truth, edit được |
| `exports/AIS4000_VR_v1.0.glb` | ~890 KB | Import vào Unity |

---

## 3. Hierarchy đầy đủ (cho Unity)

```
AIS4000_root (Empty - root pivot)
│
├─── 📦 Body
│    └── body_main                    [housing - chassis]
│
├─── 🖥️ Screen
│    └── screen_display                [LCD UI - emissive, 1024×512 texture]
│
├─── 🎮 Controls (interactive parts)
│    ├── btn_power                    [Power on/off button]
│    ├── btn_menu                     [Open main menu]
│    ├── btn_back                     [Back/cancel]
│    ├── btn_dpad_up                  [Navigate up]
│    ├── btn_dpad_down                [Navigate down]
│    ├── btn_dpad_left                [Navigate left]
│    ├── btn_dpad_right               [Navigate right]
│    ├── btn_dpad_ok                  [Confirm/select]
│    ├── knob_main                    [Rotary encoder - 24 detents]
│    └── knob_indent                  [Visual marker on knob - rotates with knob]
│
├─── 🦾 Mount
│    ├── mount_arm_left               [Left support arm]
│    ├── mount_arm_right              [Right support arm]
│    ├── mount_pivot_left             [Left tilt pivot knob]
│    ├── mount_pivot_right            [Right tilt pivot knob]
│    └── mount_base                   [Round base plate]
│
└─── 🔧 Details
     ├── led_status                   [Green LED - device active indicator]
     ├── led_alarm                    [Red LED - alarm/alert indicator]
     ├── label_raymarine              [Raymarine logo decal]
     ├── label_model                  [AIS4000 model text decal]
     ├── screw_tl                     [Top-left mounting screw]
     ├── screw_tr                     [Top-right mounting screw]
     ├── screw_bl                     [Bottom-left mounting screw]
     └── screw_br                     [Bottom-right mounting screw]
```

---

## 4. Animation Library (36 clips)

### 4.1. Button animations (8 buttons × 3 actions = 24 clips)

Cho **mỗi nút** trong: `btn_power, btn_menu, btn_back, btn_dpad_{up,down,left,right,ok}`:

| Clip | Frames | Loop? | Mô tả |
|---|:---:|:---:|---|
| `{btn}_press` | 10 | No | Single press: rest → -0.8mm Y → hold → release |
| `{btn}_wiggle` | 90 | Yes | Pop out +0.3mm × 2 lần, pause 50f, lặp |
| `{btn}_tut` | 240 | No | Phần của tutorial cinematic, press tại frame riêng |

### 4.2. Knob animations (3 clips)

| Clip | Frames | Loop? | Mô tả |
|---|:---:|:---:|---|
| `knob_idle` | 60 | Yes | Wiggle ±12° quanh trục Y, mượt |
| `knob_demo_rotate` | 120 | Yes | Quay 360° đầy đủ trong 4s |
| `knob_main_tut` | 240 | No | Quay 90° tại cuối tutorial (frame 210-240) |

### 4.3. LED animations (5 clips)

| Clip | Object | Frames | Loop? | Mô tả |
|---|---|:---:|:---:|---|
| `led_status_blink` | mat_led | 60 | Yes | Breathing pulse 3↔8 (smooth bezier) |
| `led_alarm_blink` | mat_led_red | 30 | Yes | Sharp on/off 0↔15 (constant interp) |
| `led_status_on` | mat_led | 15 | No | Ramp 0→8 khi power on |
| `led_status_off` | mat_led | 8 | No | Fade 8→0 khi power off |
| `led_status_tut` | mat_led | 240 | No | Steady 8.0 trong tutorial |

### 4.4. Screen animations (4 clips)

| Clip | Frames | Loop? | Mô tả |
|---|:---:|:---:|---|
| `screen_idle_pulse` | 120 | Yes | Brightness 4.0↔4.5 (LCD refresh feel) |
| `screen_scan` | 240 | Yes | UV vertical drift 0→0.1 (scanline effect) |
| `screen_power_on` | 30 | No | Boot: 0→flicker→1→dim→4 (CRT-style) |
| `screen_power_off` | 18 | No | Shutdown: 4→1.5→0 fade |

### 4.5. Tutorial Cinematic Timeline (combined)

Tất cả các `*_tut` actions chạy đồng thời từ frame 1-240 (8 giây):

```
Frame 1-10:    [Idle] - thiết bị standby, LED status sáng
Frame 10:      btn_power_tut nhấn (turn on demo)
Frame 35:      btn_menu_tut nhấn (open menu)
Frame 65:      btn_dpad_up_tut nhấn (navigate up)
Frame 95:      btn_dpad_down_tut nhấn
Frame 125:     btn_dpad_right_tut nhấn
Frame 155:     btn_dpad_left_tut nhấn
Frame 185:     btn_dpad_ok_tut nhấn (confirm)
Frame 205:     btn_back_tut nhấn (return)
Frame 210-240: knob_main_tut quay 90° (fine adjust)
```

---

## 5. Custom Properties (glTF Extras → Unity GameObject metadata)

Mỗi object có metadata để Unity script đọc qua `gltf.extras`:

### AIS4000_root
```json
{
  "device_type": "AIS_Class_A_Transceiver",
  "manufacturer": "Raymarine",
  "model": "AIS4000",
  "course_topic": "MaritimeVR_Bridge_Equipment",
  "interactive": true
}
```

### knob_main
```json
{
  "part_type": "rotary_encoder",
  "interactive": true,
  "vr_action": "grab_and_rotate",
  "rotation_axis": "Y",
  "detents_per_revolution": 24,
  "function": "menu_navigation_speed_dial"
}
```

### btn_power
```json
{
  "part_type": "tactile_button",
  "interactive": true,
  "vr_action": "press",
  "press_axis": "Y",
  "press_depth_mm": 0.8,
  "function": "power_on_off",
  "long_press_function": "force_shutdown"
}
```

### led_status / led_alarm
```json
{
  "part_type": "indicator_led",
  "color": "green | red",
  "function": "device_active_status | alarm_alert",
  "controllable_by_script": true
}
```

→ Trong Unity, đọc bằng:
```csharp
var extras = gltf.GetExtras(transform);
string vrAction = extras["vr_action"];
```

---

## 6. ⚠️ Limitations & Known Issues

### 6.1. Material animations và glTF compatibility

LED blink + screen pulse là **material animations** (animate emission strength). glTF 2.0 standard **không support** material property animation natively. Cần extension `KHR_animation_pointer`.

**Giải pháp:**
- ✅ Unity GLTFast plugin có support `KHR_animation_pointer`
- ✅ HOẶC Unity script tự handle (5 dòng code):

```csharp
// Trong Unity, thay thế led_status_blink bằng script:
public class LEDBlinker : MonoBehaviour {
    public Renderer ledRenderer;
    public float minIntensity = 3f, maxIntensity = 8f;
    public float speed = 1f;

    void Update() {
        float t = (Mathf.Sin(Time.time * speed) + 1f) / 2f;
        float intensity = Mathf.Lerp(minIntensity, maxIntensity, t);
        ledRenderer.material.SetColor("_EmissionColor",
            new Color(0.05f, 1f, 0.15f) * intensity);
    }
}
```

### 6.2. Knob xoay theo tay user

`knob_demo_rotate` chỉ là animation **demo**, không phản ứng với tay user.

Để knob xoay real-time theo tay học viên grab → cần **procedural Unity script** (không animate trong Blender):

```csharp
public class KnobInteractor : XRBaseInteractable {
    private float lastAngle;

    void Update() {
        if (isSelected) {
            Vector3 ctrlEuler = interactorsSelecting[0].transform.eulerAngles;
            transform.localRotation = Quaternion.Euler(0, ctrlEuler.y - lastAngle, 0);

            // Trigger detent event mỗi 15° (24 detents/rev)
            if (Mathf.Abs(ctrlEuler.y - lastAngle) >= 15f) {
                OnDetentClick.Invoke();
                lastAngle = ctrlEuler.y;
            }
        }
    }
}
```

### 6.3. Decimation artifacts

Một số đối tượng (`mount_base`, `knob_main`) đã được decimated với `dissolve` modifier. Có thể có vài tris không hoàn toàn flat. Không ảnh hưởng visual nhưng nếu cần collider chính xác, dùng convex hull thay vì mesh collider.

### 6.4. Screen UI texture cố định

UI texture (radar interface với targets, info bars) là static. Để hiển thị UI thực sự dynamic (khi user thao tác), cần:
- Option A: Tạo nhiều biến thể texture, swap qua script
- Option B: Render Canvas Unity vào RenderTexture → assign vào screen material
- Option C: World-space Canvas trực tiếp gắn lên `screen_display`

**Khuyến nghị: Option C** cho LMS - UI dynamic hoàn toàn từ Unity Canvas.

---

## 7. Hướng dẫn Unity Integration

### Bước 1: Import GLB
```
1. Drag exports/AIS4000_VR_v1.0.glb → Assets/Models/AIS4000/
2. Click vào file → Inspector
   ✓ Read/Write Enabled
   ✓ Import Animations
   ✓ Generate Lightmap UVs (cho baked lighting)
3. Tab "Materials" → Extract Materials → Assets/Models/AIS4000/Materials/
```

### Bước 2: Setup loop flags cho clips
```
Animations tab, mỗi clip:
  Loop: btn_*_wiggle, knob_idle, knob_demo_rotate,
        led_*_blink, screen_idle_pulse, screen_scan
  No Loop: tất cả _press, _tut, _on, _off
```

### Bước 3: Build prefab
```
1. Drag model vào scene → tạo GameObject
2. Add Component "XR Grab Interactable" lên AIS4000_root
3. Add Component "Animator" (controller chuẩn bị bước 4)
4. Drag từ Hierarchy → Project (làm prefab)
```

### Bước 4: Animator Controller setup
```
Tạo Animator Controller "AIS4000_Controller":

Layer 0 "Idle":
  - Default state: knob_idle (loop)
  - Sub-states: led_status_blink, screen_idle_pulse (loop)

Layer 1 "Press" (Override, weight 1):
  - State: btn_power_press, btn_menu_press, ... (one-shot)
  - Triggers: TriggerPower, TriggerMenu, TriggerBack, ...

Layer 2 "Hint" (Additive):
  - States: btn_power_wiggle, btn_menu_wiggle, ...
  - Bool params: HintPower, HintMenu, ...

Layer 3 "Tutorial":
  - State: tutorial_demo (plays all _tut clips together)
  - Trigger: PlayTutorial
```

### Bước 5: Interaction script

```csharp
using UnityEngine;
using UnityEngine.XR.Interaction.Toolkit;

public class AIS4000DeviceController : MonoBehaviour
{
    [SerializeField] private Animator animator;
    [SerializeField] private MeshRenderer ledStatus;
    [SerializeField] private MeshRenderer ledAlarm;

    private bool isPoweredOn = false;

    public void OnPowerButtonPressed()
    {
        animator.SetTrigger("TriggerPower");

        if (!isPoweredOn) {
            animator.Play("screen_power_on");
            animator.Play("led_status_on");
            isPoweredOn = true;
        } else {
            animator.Play("screen_power_off");
            animator.Play("led_status_off");
            isPoweredOn = false;
        }
    }

    public void OnMenuButtonPressed() {
        animator.SetTrigger("TriggerMenu");
        // Open Unity Canvas menu...
    }

    public void HintToPressMenu() {
        animator.SetBool("HintMenu", true);
        Invoke(nameof(StopHinting), 5f);
    }

    void StopHinting() {
        animator.SetBool("HintMenu", false);
    }

    public void TriggerAlarm(bool state) {
        if (state) animator.Play("led_alarm_blink");
        // ... handle alarm UI
    }

    public void PlayTutorialCinematic() {
        animator.SetTrigger("PlayTutorial");
    }
}
```

### Bước 6: XR Setup

```
Trên prefab AIS4000:
  - XR Grab Interactable (cho phép cầm/xoay thiết bị)
  - Rigidbody (Use Gravity = false, Is Kinematic = true)
  - Box Collider (cho thân chính)

Trên mỗi nút (btn_*):
  - XR Simple Interactable
  - Box Collider (small)
  - Event "Select Entered" → OnPowerButtonPressed()

Trên knob_main:
  - Custom KnobInteractor script (xem section 6.2)
  - Sphere Collider hoặc Capsule Collider
```

---

## 8. Render Previews

| File | Mô tả |
|---|---|
| `renders/AIS4000_FINAL_HERO.png` | Hero shot 3/4 view - dùng cho marketing |
| `renders/AIS4000_view1_hero.png` | 3/4 từ phải |
| `renders/AIS4000_view2_front.png` | Front orthographic - clear logo + UI |
| `renders/AIS4000_view3_left.png` | 3/4 từ trái |
| `renders/AIS4000_view4_side.png` | Side profile - showing depth |
| `renders/anim_tut_f035.png` | Tutorial frame 35 (LED active) |
| `renders/anim_tut_f065.png` | Tutorial frame 65 (D-pad up press) |
| `renders/anim_tut_f230.png` | Tutorial frame 230 (knob rotated 67°) |
| `renders/anim_idle_f007.png` | Idle frame 7 (LED alarm blinking) |

---

## 9. Reference

| File | Source |
|---|---|
| `reference/AIS4000_original_reference.png` | Real-device photo (modeling reference) |

**Inspiration:** Raymarine AIS4000 Class A Transceiver (commercial product).
**Note:** Model là interpretation, không phải sản phẩm chính thức của Raymarine.

---

## 10. Changelog

### v1.0 (2026-05-07)
- ✅ Initial release với 36 animation clips
- ✅ Full PBR materials với baked AO
- ✅ Custom properties metadata cho Unity
- ✅ Y-up convention, Apply transforms
- ✅ Embedded UI texture 1024×512
- ✅ LED status + alarm với boot animations
- ✅ Tutorial cinematic 8-second timeline

### Future improvements (v1.1+ ideas)
- [ ] Generate normal map baked from high-poly bevel
- [ ] Add MOB (Man Overboard) emergency button (red, protected)
- [ ] Add cable connectors on back face (NMEA 2000, power)
- [ ] Add multiple UI texture variants for different menus
- [ ] Add sound effect markers (beep, click) for Unity AudioSource
- [ ] LOD0/LOD1/LOD2 versions cho VR optimization
- [ ] Damage/wear states (used vs new)

---

**End of Document**
