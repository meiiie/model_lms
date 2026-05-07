# 📡 VHF Marine Radio (DSC) - Documentation

**v1.0** | 2026-05-07

## 1. Giới thiệu

**VHF Marine Radio** với DSC (Digital Selective Calling) capability. Standard equipment cho ship-to-ship/ship-to-shore communication.

### Real-world specs
- Frequency: 156-174 MHz (VHF marine band)
- Channels: 16 (international distress) + 70 (DSC) + working channels
- Power: 1W / 25W switchable
- DSC: Class A/B/D depending on vessel size

## 2. Dimensions
| | mm |
|---|---:|
| Width | 180 |
| Height | 100 |
| Depth | 60 |

## 3. Hierarchy

```
VHF_root
├── Body
│   └── vhf_body
├── Screen
│   └── vhf_screen          [LCD with channel display]
├── Controls
│   ├── knob_channel        [Top right - rotates to select channel]
│   ├── knob_volume         [Bottom right - volume/squelch]
│   ├── btn_distress        [RED DSC distress button]
│   ├── btn_ptt             [Push-to-talk button]
│   ├── btn_16              [Quick channel 16 (emergency)]
│   ├── btn_dual            [Dual watch]
│   ├── btn_scan            [Scan channels]
│   └── btn_menu            [Menu navigation]
└── Details
```

## 4. Animation Library (10 clips)

| Clip | Loop | Mô tả |
|---|:---:|---|
| `btn_distress_press` | No | DSC distress alert (3-sec hold required) |
| `btn_ptt_press` | No | Push-to-talk (hold) |
| `btn_16_press` | No | Quick channel 16 |
| `btn_dual_press` | No | Toggle dual watch |
| `btn_scan_press` | No | Start/stop scan |
| `btn_menu_press` | No | Open menu |
| `knob_channel_idle` | Yes | Subtle wobble (alive feel) |
| `knob_channel_demo_rotate` | Yes | Full 360° demo |
| `knob_volume_idle` | Yes | Subtle wobble |
| `knob_volume_demo_rotate` | Yes | Full 360° demo |

## 5. Custom Properties

```json
{
  "VHF_root": {
    "device_type": "VHF_Marine_Radio",
    "category": "Communication",
    "DSC_capable": true
  },
  "btn_distress": {
    "function": "DSC_distress_alert",
    "vr_action": "long_press_3sec",
    "color": "red"
  },
  "knob_channel": {
    "function": "channel_select",
    "rotation_axis": "Y",
    "vr_action": "grab_and_rotate"
  }
}
```

## 6. Unity Integration

```csharp
// VHF Controller
public class VHFController : MonoBehaviour {
    public int currentChannel = 16;
    public bool isPTTHeld = false;

    public void OnPTTPressed() => isPTTHeld = true;
    public void OnPTTReleased() => isPTTHeld = false;

    public void OnDistressLongPress() {
        // Play alarm sound + send DSC distress
        StartCoroutine(SendDSCDistressAlert());
    }

    public void OnChannelKnobRotate(float angle) {
        int channels[] = { 6, 12, 13, 16, 22, 67, 70, 72, 78A };
        // Map angle to channel
        currentChannel = channels[Mathf.RoundToInt(angle / 30f) % channels.Length];
    }
}
```

## 7. Files

| File | Size |
|---|---:|
| `source/VHF_VR_v1.0.blend` | 220 KB |
| `exports/VHF_VR_v1.0.glb` | 37 KB |

---
**End of Document**
