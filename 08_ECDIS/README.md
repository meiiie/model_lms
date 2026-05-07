# 🗺️ ECDIS (Electronic Chart Display) - Documentation

**v1.0** | 2026-05-07

## 1. Giới thiệu

**ECDIS** = Electronic Chart Display and Information System. Mandatory cho tàu thương mại theo SOLAS V/19.2.10. Thay thế giấy navigation chart.

### Real-world specs
- **Display:** 24" widescreen TFT (1920×1200 typical)
- **Charts:** ENC (Electronic Navigational Chart) S-57 format
- **Tools:** Route planning, AIS overlay, depth alarms, weather data
- **Backup:** Paper chart still required for redundancy

## 2. Dimensions
| | mm |
|---|---:|
| Width | 620 |
| Height | 380 |
| Depth | 80 |

## 3. Hierarchy

```
ECDIS_root
├── Body
│   ├── ecdis_body          [Monitor housing]
│   └── ecdis_mount          [VESA mount on back]
├── Screen
│   └── ecdis_screen        [Chart display - 1024×640 texture]
└── Controls
    ├── btn_zoom_in/out      [Chart zoom]
    ├── btn_center          [Center on ship]
    ├── btn_route           [Route planning mode]
    ├── btn_layer           [Toggle chart layers]
    ├── btn_target          [Show AIS targets]
    ├── btn_alarm           [Alarm settings]
    ├── btn_menu            [Main menu]
    └── trackball           [Pan chart with sphere]
```

## 4. Chart Texture (1024×640)

Texture chứa:
- Ocean blue background
- 3 land masses (yellow-tan)
- Lat/Lon grid
- Depth contours (concentric)
- Own ship (green triangle, center)
- Course line (forward)
- 4 AIS targets (yellow/orange triangles)
- Planned route waypoints (orange dots + line)
- Top status bar + bottom toolbar
- Right info panel

## 5. Animations (9 clips)

| Clip | Loop | Mô tả |
|---|:---:|---|
| `btn_zoom_in_press` | No | Zoom in chart |
| `btn_zoom_out_press` | No | Zoom out chart |
| `btn_center_press` | No | Center on ship |
| `btn_route_press` | No | Route planning |
| `btn_layer_press` | No | Toggle layers |
| `btn_target_press` | No | Toggle AIS targets |
| `btn_alarm_press` | No | Alarm settings |
| `btn_menu_press` | No | Main menu |
| `trackball_idle` | Yes | Subtle wobble (3 axes) |

## 6. Unity Integration

### Dynamic chart

```csharp
public class ECDISController : MonoBehaviour {
    public Renderer screenRenderer;
    public RenderTexture chartTexture;  // World-space Canvas → RenderTexture
    public Camera chartCamera;          // Top-down camera following ship

    void Start() {
        screenRenderer.material.SetTexture("_BaseMap", chartTexture);
    }

    public void ZoomIn() => chartCamera.orthographicSize *= 0.5f;
    public void ZoomOut() => chartCamera.orthographicSize *= 2.0f;
}
```

### Trackball pan
```csharp
public class TrackballController : MonoBehaviour {
    public Camera chartCamera;

    public void OnTrackballRotate(Vector3 deltaAxis) {
        chartCamera.transform.Translate(
            new Vector3(deltaAxis.z, 0, deltaAxis.x) * 0.5f,
            Space.Self
        );
    }
}
```

## 7. Files

| File | Size |
|---|---:|
| `source/ECDIS_VR_v1.0.blend` | 255 KB |
| `exports/ECDIS_VR_v1.0.glb` | 106 KB |

---
**End of Document**
