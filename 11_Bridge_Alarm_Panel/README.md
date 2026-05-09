# Bridge Alarm / Acknowledge Panel

Version: v1.0
Created: 2026-05-10
Source: Generated procedurally with Codex + Blender Python.

## Purpose

Safety-control training prop for the VR Maritime LMS bridge scene. It gives the
lesson system a compact panel for alarm acknowledgement, silence, lamp test, and
emergency-stop familiarization.

## Runtime Exports

- `exports/BridgeAlarmPanel_VR_v1.0.fbx`
- `exports/BridgeAlarmPanel_VR_v1.0.glb`

## Source

- `source/BridgeAlarmPanel_VR_v1.0.blend`
- Generator script: `tools/blender_agent/create_bridge_alarm_panel.py`

## Unity Notes

- Real-world scale: meters.
- Use simple BoxCollider or per-button capsule/cylinder colliders in Unity.
- Buttons expose named mesh objects and `grab_target_*` empties for interaction
  anchoring.
- Suggested lesson usage: require the trainee to acknowledge an alarm before
  changing telegraph state.

## License / Provenance

Project-generated training asset. No manufacturer branding, logos, or certified
equipment markings are included. Keep this entry under review in the central
asset license audit before external redistribution.
