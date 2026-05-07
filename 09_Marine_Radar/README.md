# 📡 Marine Radar (X-band PPI) - Documentation

**v1.0** | 2026-05-07

## 1. Giới thiệu

**Marine Radar** với PPI (Plan Position Indicator) display. X-band radar (9.4 GHz) cho navigation + collision avoidance.

### Real-world specs
- **Frequency:** X-band 9.4 GHz (9.2-9.5 GHz)
- **Range:** 0.125 - 96 nm typical
- **Antenna RPM:** 24-30 (we use 30)
- **PPI:** Round green CRT-style display, classic green sweep
- **ARPA:** Auto Radar Plotting Aid for target tracking

## 2. Dimensions
| | mm |
|---|---:|
| Body Width | 380 |
| Body Height | 420 |
| Body Depth | 150 |
| PPI Diameter | 300 |

## 3. Hierarchy

```
Radar_root
├── Body
│   └── radar_body
├── Screen
│   └── ppi_display              [Round PPI - 1024×1024 texture]
├── Sweep_Animation
│   ├── sweep_pivot (Empty)       [Rotates Y axis - 30 RPM]
│   └── sweep_arm                 [Bright green emissive line]
└── Controls
    ├── knob_range               [Range select]
    ├── knob_gain                [Signal gain]
    ├── knob_brightness          [Display brightness]
    ├── btn_standby
    ├── btn_transmit
    ├── btn_arpa                 [ARPA target acquisition]
    └── btn_ebl_vrm              [EBL/VRM measurement tools]
```

## 4. PPI Texture (1024×1024 round)

- Black/dark green background (radar phosphor)
- 5 concentric range rings (green)
- Cardinal lines (N-S, E-W) + diagonals
- Compass markings (every 5° + major every 30°)
- 8 random target blips with afterglow
- Center own ship cross
- Heading line (N forward)

## 5. Animations (9 clips)

| Clip | Loop | Mô tả |
|---|:---:|---|
| `sweep_rotate` | **Yes** | **30 RPM continuous rotation** (KEY animation!) |
| `sweep_demo_3rev` | No | 3 full revolutions for demo (6 sec) |
| `btn_standby_press` | No | Standby mode |
| `btn_transmit_press` | No | Transmit mode |
| `btn_arpa_press` | No | ARPA mode |
| `btn_ebl_vrm_press` | No | EBL/VRM tools |
| `knob_range_demo` | No | Range knob 180° |
| `knob_gain_demo` | No | Gain knob 180° |
| `knob_brightness_demo` | No | Brightness knob 180° |

## 6. Unity Integration

### Always-rotating sweep (CRITICAL)

```csharp
public class RadarSweepController : MonoBehaviour {
    public Transform sweepPivot;
    public float rpm = 30f;

    void Update() {
        float degPerSec = rpm * 360f / 60f;
        sweepPivot.Rotate(0, -degPerSec * Time.deltaTime, 0);
    }
}
```

### Range selection

```csharp
public class RadarRangeController : MonoBehaviour {
    public float[] ranges = { 0.125f, 0.25f, 0.5f, 1f, 3f, 6f, 12f, 24f, 48f, 96f };
    int currentRangeIndex = 5;

    public void OnKnobRotate(float delta) {
        if (delta > 15f) currentRangeIndex = Mathf.Min(currentRangeIndex + 1, ranges.Length - 1);
        else if (delta < -15f) currentRangeIndex = Mathf.Max(currentRangeIndex - 1, 0);

        float rangeNm = ranges[currentRangeIndex];
        // Scale PPI texture or show different chart layer
    }
}
```

### Live target detection

```csharp
public class RadarTargetDetector : MonoBehaviour {
    public Transform shipTransform;
    public LayerMask radarTargetsLayer;
    public float detectionRangeNm = 6f;

    void Update() {
        var rangeM = detectionRangeNm * 1852f;
        var hits = Physics.OverlapSphere(shipTransform.position, rangeM, radarTargetsLayer);
        // For each target, calculate bearing + range, draw on PPI
    }
}
```

## 7. Files

| File | Size |
|---|---:|
| `source/Radar_VR_v1.0.blend` | 295 KB |
| `exports/Radar_VR_v1.0.glb` | 125 KB |

---
**End of Document**
