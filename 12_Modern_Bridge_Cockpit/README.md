# Modern Bridge Cockpit

Version: v1.0
Created: 2026-05-10
Source: Generated procedurally with Codex + Blender Python from a project-local ImageGen reference.

## Purpose

High-context ship bridge cockpit blockout/detail asset for the VR Maritime LMS.
This is intended as a professional layout reference and Unity import candidate,
not yet the final AAA-quality art pass.

## Runtime Exports

- `exports/ModernBridgeCockpit_VR_v1.0.fbx`
- `exports/ModernBridgeCockpit_VR_v1.0.glb`

## Source

- `source/ModernBridgeCockpit_VR_v1.0.blend`
- Generator script: `tools/blender_agent/create_modern_bridge_cockpit.py`
- Concept reference: `reference/imagegen_bridge_cockpit_reference_v1.png`

## Scale And Orientation

- Authored in meters.
- Primary player start anchor: `player_start_desktop_vr`.
- Unity import target: keep scale factor at 1.0 after verifying model height in scene.
- Collision hints are hidden wire objects prefixed with `COL_`.

## Interaction Anchors

- `grab_target_telegraph_handle`
- `hand_pose_telegraph_right`
- `hand_pose_telegraph_left`
- `grab_target_helm_left`
- `grab_target_helm_right`
- `lesson_focus_engine_telegraph`
- `lesson_focus_helm`

## Runtime Notes

- Import the FBX into Unity first for native editor compatibility.
- Build colliders from `COL_` proxy objects, then hide or strip their renderers.
- Convert the telegraph, helm, and major console areas into prefabs before adding lesson scripts.
- Do not import this whole asset into Quest runtime unchanged; split or LOD it after visual approval.

## Provenance

Created inside the `model_lms` source asset repository. The image reference was
generated for this project and is stored only as concept/reference material.
