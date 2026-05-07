# 🎮 Unity Integration Pack - Maritime VR LMS

**Mục đích:** Hướng dẫn đầy đủ + C# scripts ready-to-use để integrate toàn bộ library vào Unity 2022.3 + XR Interaction Toolkit.

---

## 📦 Library Contents (9 models)

| # | Model | GLB | FBX | Anims | Use case |
|---:|---|---:|---:|---:|---|
| 01 | AIS4000 | 911 KB | 4.6 MB | 36 | Navigation - target tracking |
| 02 | Ship Wheel | 145 KB | 853 KB | 6 | Steering |
| 03 | Magnetic Compass | 154 KB | 473 KB | 5 | Heading reference |
| 04 | Engine Telegraph (EOT) | 130 KB | 1.6 MB | 19 | Engine orders |
| 05 | Ocean Environment | 233 KB | 270 KB | 1 | Sea view |
| 06 | Bridge Cabin v1.1 | 183 KB | 91 KB | 10 | Container scene + doors + alerts |
| 07 | VHF Radio | 37 KB | - | 10 | Communication |
| 08 | ECDIS Display | 106 KB | - | 9 | Chart navigation |
| 09 | Marine Radar | 125 KB | - | 9 | Target detection |
| **TOTAL** | **9 models** | **~2 MB** | **~7.9 MB** | **105+ anims** | Full bridge VR |

---

## 🚀 Quick Start (15 minutes to working VR scene)

### Step 1: Unity Project Setup

```
Unity Version: 2022.3 LTS or later
Required Packages:
  - XR Interaction Toolkit (3.0+)
  - XR Plugin Management
  - OpenXR Plugin
  - URP (Universal Render Pipeline) - recommended
```

### Step 2: Import Models

```
Drag entire VR_Maritime_LMS_Models/ folder into Assets/
Or selectively:
  Assets/Models/
    Bridge/         ← Bridge_v1.1_empty.glb
    Equipment/      ← all 8 equipment .fbx files
    Environment/    ← Ocean_VR_v1.1.fbx
```

### Step 3: Configure Each Asset

For EACH `.fbx` file:
```
1. Click .fbx → Inspector
2. Model tab:
   - Scale Factor: 1
   - Convert Units: ✓
   - Read/Write Enabled: ✓
3. Animation tab:
   - Set Loop Time:
     ✓ All *_idle, *_wiggle, *_blink, *_pulse, *_scan, *_rotate, *_sweep_rotate
     ✗ All *_press, *_tut, *_to_*, *_on, *_off, *_open, *_close
4. Materials tab:
   - Click "Extract Materials..." → save to Models/MaterialName/Materials/
```

---

## 🎯 Master Controller Scripts

### 1. `BridgeManager.cs` - Auto-spawn equipment at anchors

```csharp
using UnityEngine;
using System.Linq;

public class BridgeManager : MonoBehaviour
{
    [Header("Equipment Prefabs (assign in Inspector)")]
    public GameObject ais4000Prefab;
    public GameObject shipWheelPrefab;
    public GameObject compassPrefab;
    public GameObject eotPrefab;
    public GameObject vhfPrefab;
    public GameObject ecdisPrefab;
    public GameObject radarPrefab;

    [Header("Settings")]
    public bool spawnOnStart = true;

    void Start() {
        if (spawnOnStart) SpawnAllEquipment();
    }

    public void SpawnAllEquipment() {
        var anchors = GetComponentsInChildren<Transform>()
            .Where(t => t.name.StartsWith("anchor_")).ToArray();

        foreach (Transform anchor in anchors) {
            GameObject prefab = GetPrefabForAnchor(anchor.name);
            if (prefab != null) {
                var instance = Instantiate(prefab, anchor.position, anchor.rotation, anchor);
                instance.name = anchor.name.Replace("anchor_", "") + "_instance";
            }
        }
    }

    GameObject GetPrefabForAnchor(string anchorName) {
        return anchorName switch {
            "anchor_AIS4000" => ais4000Prefab,
            "anchor_ShipWheel" => shipWheelPrefab,
            "anchor_Compass" => compassPrefab,
            "anchor_EOT" => eotPrefab,
            "anchor_VHF" => vhfPrefab,
            "anchor_ECDIS" => ecdisPrefab,
            "anchor_Radar" => radarPrefab,
            _ => null
        };
    }
}
```

### 2. `ShipWheelInteractor.cs` - Real-time wheel rotation (procedural)

```csharp
using UnityEngine;
using UnityEngine.XR.Interaction.Toolkit;

[RequireComponent(typeof(XRGrabInteractable))]
public class ShipWheelInteractor : MonoBehaviour
{
    public Transform wheelPivot;
    public float maxLockDegrees = 720f;
    public bool springBackToCenter = false;

    public UnityEngine.Events.UnityEvent<float> OnRudderChanged;

    XRGrabInteractable grab;
    float currentAngle = 0f;
    Vector3 lastRight;
    bool isGrabbed;

    void Awake() {
        grab = GetComponent<XRGrabInteractable>();
        grab.selectEntered.AddListener(OnGrab);
        grab.selectExited.AddListener(OnRelease);
    }

    void OnGrab(SelectEnterEventArgs args) {
        isGrabbed = true;
        lastRight = transform.InverseTransformDirection(args.interactorObject.transform.right);
    }

    void OnRelease(SelectExitEventArgs args) => isGrabbed = false;

    void Update() {
        if (!isGrabbed) {
            if (springBackToCenter && Mathf.Abs(currentAngle) > 0.1f) {
                currentAngle = Mathf.MoveTowards(currentAngle, 0, 90 * Time.deltaTime);
                Apply();
            }
            return;
        }

        var interactor = grab.interactorsSelecting[0].transform;
        var currentRight = transform.InverseTransformDirection(interactor.right);
        float delta = Vector3.SignedAngle(lastRight, currentRight, Vector3.up);
        currentAngle = Mathf.Clamp(currentAngle + delta, -maxLockDegrees, maxLockDegrees);
        OnRudderChanged?.Invoke(currentAngle / maxLockDegrees);
        Apply();
        lastRight = currentRight;
    }

    void Apply() => wheelPivot.localRotation = Quaternion.Euler(0, currentAngle, 0);
}
```

### 3. `CompassController.cs` - Auto-rotates with ship heading

```csharp
using UnityEngine;

public class CompassController : MonoBehaviour
{
    public Transform cardPivot;
    public Transform shipTransform;
    public float swingDamping = 5f;

    float currentHeading = 0f;

    void Update() {
        float target = -shipTransform.eulerAngles.y;
        currentHeading = Mathf.LerpAngle(currentHeading, target, Time.deltaTime * swingDamping);
        cardPivot.localRotation = Quaternion.Euler(0, 0, currentHeading);
    }

    public float GetHeadingDegrees() => (-currentHeading + 360f) % 360f;
}
```

### 4. `EOTController.cs` - Engine telegraph

```csharp
using System.Collections;
using UnityEngine;
using UnityEngine.Events;

public class EOTController : MonoBehaviour
{
    public enum Position {
        FullAstern = 0, HalfAstern = 1, SlowAstern = 2,
        Stop = 3,
        SlowAhead = 4, HalfAhead = 5, FullAhead = 6
    }

    public Transform orderedPivot;
    public Transform answeredPivot;
    public AudioSource bellSound;
    public float engineResponseDelay = 1.5f;
    public float pointerSpeed = 90f;

    public UnityEvent<Position> OnOrderChanged;

    Position currentOrder = Position.Stop;

    static float[] PositionAngles = { -90, -60, -30, 0, 30, 60, 90 };

    public void SetOrder(Position newOrder) {
        if (newOrder == currentOrder) return;
        currentOrder = newOrder;
        if (bellSound) bellSound.Play();
        StartCoroutine(RotatePointer(orderedPivot, PositionAngles[(int)newOrder]));
        StartCoroutine(EngineRoomReply(newOrder));
        OnOrderChanged?.Invoke(newOrder);
    }

    IEnumerator RotatePointer(Transform pivot, float targetDeg) {
        float startDeg = pivot.localEulerAngles.y;
        if (startDeg > 180) startDeg -= 360;
        float duration = Mathf.Abs(targetDeg - startDeg) / pointerSpeed;
        for (float t = 0; t < duration; t += Time.deltaTime) {
            float k = Mathf.Clamp01(t / duration);
            pivot.localRotation = Quaternion.Euler(0, Mathf.Lerp(startDeg, targetDeg, k), 0);
            yield return null;
        }
    }

    IEnumerator EngineRoomReply(Position order) {
        yield return new WaitForSeconds(engineResponseDelay);
        StartCoroutine(RotatePointer(answeredPivot, PositionAngles[(int)order]));
    }
}
```

### 5. `LEDBlinker.cs` - LED emission animation (replaces Blender material anims)

```csharp
using UnityEngine;

public class LEDBlinker : MonoBehaviour
{
    public Renderer ledRenderer;
    public Color ledColor = Color.green;
    public float minIntensity = 3f;
    public float maxIntensity = 8f;
    public float speed = 2f;
    public bool isAlarm = false;

    Material mat;

    void Start() {
        mat = ledRenderer.material;
    }

    void Update() {
        float intensity;
        if (isAlarm) {
            // Sharp on/off blink for alarms
            intensity = (Mathf.Floor(Time.time * speed) % 2 == 0) ? maxIntensity : 0f;
        } else {
            // Smooth breathing pulse for status
            float t = (Mathf.Sin(Time.time * speed) + 1f) * 0.5f;
            intensity = Mathf.Lerp(minIntensity, maxIntensity, t);
        }
        mat.SetColor("_EmissionColor", ledColor * intensity);
    }
}
```

### 6. `KnobInteractor.cs` - Generic rotation for any knob (Compass dispersion, Volume, etc.)

```csharp
using UnityEngine;
using UnityEngine.XR.Interaction.Toolkit;

[RequireComponent(typeof(XRGrabInteractable))]
public class KnobInteractor : MonoBehaviour
{
    public Transform knobMesh;
    public Vector3 rotationAxis = Vector3.up;
    public int detentsPerRevolution = 24;
    public bool clamp = false;
    public float minDeg = -360f, maxDeg = 360f;

    public UnityEngine.Events.UnityEvent OnDetentClick;
    public UnityEngine.Events.UnityEvent<float> OnRotated;

    XRGrabInteractable grab;
    float currentAngle = 0f;
    Vector3 lastDir;
    bool isGrabbed;
    float lastDetentAngle = 0;

    void Awake() {
        grab = GetComponent<XRGrabInteractable>();
        grab.selectEntered.AddListener(args => {
            isGrabbed = true;
            lastDir = transform.InverseTransformDirection(args.interactorObject.transform.up);
        });
        grab.selectExited.AddListener(args => isGrabbed = false);
    }

    void Update() {
        if (!isGrabbed) return;
        var dir = transform.InverseTransformDirection(grab.interactorsSelecting[0].transform.up);
        float delta = Vector3.SignedAngle(lastDir, dir, rotationAxis);
        currentAngle += delta;
        if (clamp) currentAngle = Mathf.Clamp(currentAngle, minDeg, maxDeg);

        knobMesh.localRotation = Quaternion.AngleAxis(currentAngle, rotationAxis);

        // Detent click events
        float detentSize = 360f / detentsPerRevolution;
        if (Mathf.Abs(currentAngle - lastDetentAngle) >= detentSize) {
            OnDetentClick?.Invoke();
            lastDetentAngle = Mathf.Round(currentAngle / detentSize) * detentSize;
        }

        OnRotated?.Invoke(currentAngle);
        lastDir = dir;
    }
}
```

### 7. `RadarSweepController.cs` - Continuously rotating radar sweep

```csharp
using UnityEngine;

public class RadarSweepController : MonoBehaviour
{
    public Transform sweepPivot;
    public float rpm = 30f;  // 30 RPM = 2 sec/revolution

    void Update() {
        float degPerSec = rpm * 360f / 60f;
        sweepPivot.Rotate(0, -degPerSec * Time.deltaTime, 0);
    }
}
```

### 8. `DoorInteractor.cs` - Bridge door open/close

```csharp
using UnityEngine;
using UnityEngine.XR.Interaction.Toolkit;
using System.Collections;

public class DoorInteractor : XRSimpleInteractable
{
    public Transform hingePivot;
    public Animator animator;
    public string openClipName = "door_left_open";
    public string closeClipName = "door_left_close";

    bool isOpen = false;

    protected override void OnSelectEntered(SelectEnterEventArgs args) {
        base.OnSelectEntered(args);
        isOpen = !isOpen;
        if (animator) {
            animator.Play(isOpen ? openClipName : closeClipName);
        }
    }
}
```

---

## 🎬 Animator Controller Setup

### Standard 4-layer setup (per equipment)

```
Layer 0 "Idle" (Weight 1.0):
  Default state: *_idle (loop)

Layer 1 "Tactile Feedback" (Weight 1.0, Override):
  States: *_press, *_to_* (one-shot)
  Triggers: TriggerPower, TriggerMenu, etc.

Layer 2 "Hint" (Weight 1.0, Additive):
  States: *_wiggle (loop)
  Bool params: HintPower, HintMenu, etc.

Layer 3 "Tutorial" (Weight 0/1):
  States: *_tut (one-shot, plays in sequence)
  Trigger: PlayTutorial
```

### Master Tutorial Coordinator

```csharp
using UnityEngine;
using System.Collections;

public class TutorialCoordinator : MonoBehaviour
{
    public Animator[] equipmentAnimators;

    public void PlayMasterTutorial() {
        StartCoroutine(PlayAllTutorials());
    }

    IEnumerator PlayAllTutorials() {
        // All equipment plays their _tut animation simultaneously
        foreach (var anim in equipmentAnimators) {
            anim.SetTrigger("PlayTutorial");
        }

        // Wait for tutorial duration (8 seconds)
        yield return new WaitForSeconds(8f);

        // Return to idle
        foreach (var anim in equipmentAnimators) {
            anim.SetTrigger("ReturnToIdle");
        }
    }
}
```

---

## 🎨 Material Conversion: Blender → Unity URP

### Common materials checklist

| Blender Material | Unity URP equivalent |
|---|---|
| Principled BSDF (matte plastic) | URP/Lit (Smoothness 0.4-0.6, Metallic 0) |
| Brass/metal | URP/Lit (Metallic 1.0, Smoothness 0.7) |
| Wood | URP/Lit (with Albedo texture) |
| Glass (transparent) | URP/Lit Surface=Transparent, Smoothness 0.95 |
| Emission (LED, screen) | URP/Lit Emission enabled + HDR color |
| Procedural noise (water, scratches) | **Recreate** in Shader Graph or use baked AO |

### Critical: Material animations DON'T export

**9 LED + Screen animations bị mất** khi export GLB/FBX:
- `led_status_blink/on/off/tut`
- `led_alarm_blink`
- `screen_idle_pulse/scan/power_on/power_off`

→ **Replace với `LEDBlinker.cs` script** trên LED meshes.

---

## 🎯 Performance Tips for Quest 2/3

### Polygon budget
```
Bridge cabin:           600 verts
Equipment library:    ~10,500 verts (all 8)
Ocean (LOD0):          7,200 verts
TOTAL VR scene:       ~18,300 verts ✅ Excellent for Quest
```

### Lighting strategy
```
1. Mark static objects → bake lightmaps
2. 1 directional light (sun through windows)
3. 4 baked area lights (ceiling fixtures)
4. Reserve 2 realtime lights for:
   - Alert lights (red blink)
   - LED indicators
```

### Texture compression
```
All textures (UI screen, dial faces): ASTC 6x6 or 8x8
Albedo: ASTC 8x8 (~30% size reduction)
Normal maps: keep at 1024×1024
```

### Draw call optimization
```
- Combine static furniture meshes
- Use SRP Batcher (URP enabled by default)
- Equipment with shared materials → can be batched
```

---

## 🌐 WebXR / A-Frame Alternative

Nếu không dùng Unity, GLB files cũng work với A-Frame:

```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://aframe.io/releases/1.5.0/aframe.min.js"></script>
  <script src="https://cdn.jsdelivr.net/gh/c-frame/aframe-extras@7.5.0/dist/aframe-extras.min.js"></script>
</head>
<body>
  <a-scene>
    <a-entity gltf-model="06_Bridge_Cabin/exports/Bridge_v1.1_empty.glb"
              position="0 0 -2"></a-entity>
    <a-entity gltf-model="01_AIS4000_Class_A_Transceiver/exports/AIS4000_VR_v1.0.glb"
              position="-1.5 0.95 -4"
              animation-mixer="clip: btn_power_press; loop: once"></a-entity>
    <!-- ... etc -->
    <a-camera position="0 1.6 0"></a-camera>
  </a-scene>
</body>
</html>
```

---

## 📋 Final Integration Checklist

- [ ] All 9 GLB files imported to Unity
- [ ] Materials extracted + converted to URP
- [ ] Animator Controllers created per equipment
- [ ] BridgeManager script + 7 equipment prefabs assigned
- [ ] XR Origin (player rig) positioned at helm
- [ ] LEDBlinker scripts replacing material animations
- [ ] Ship Wheel uses ShipWheelInteractor (procedural)
- [ ] Compass auto-syncs với ship heading
- [ ] EOT bell sound effect added
- [ ] Radar sweep continuously rotating
- [ ] Door interaction (XRSimpleInteractable + animation trigger)
- [ ] Lighting baked for static objects
- [ ] Build target: Quest 2/3 (Android) hoặc PC VR

---

**Total preparation time:** 4-8 hours
**Result:** Production-ready VR Maritime LMS scene với 9 thiết bị + bridge + ocean
