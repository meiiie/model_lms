# Modern Bridge Cockpit

Version: v1.1
Created: 2026-05-10
Source: Generated procedurally with Codex + Blender Python from project-local ImageGen references.

## Purpose

High-context ship bridge cockpit asset for the VR Maritime LMS. This version
keeps the cockpit as real procedural geometry and uses generated raster textures
only where images are appropriate: displays, carpet, ceiling panels, black
metal console surfaces, and wood cabinets.

`13_Modern_Bridge_Depth_Relief` was removed from the active pipeline because it
looked richer in a still render but did not provide trustworthy VR geometry.

## Runtime Exports

- `exports/ModernBridgeCockpit_VR_v1.1.fbx`
- `exports/ModernBridgeCockpit_VR_v1.1.glb`

## Source

- `source/ModernBridgeCockpit_VR_v1.1.blend`
- Generator script: `tools/blender_agent/create_modern_bridge_cockpit.py`
- Concept reference: `reference/imagegen_bridge_cockpit_reference_v1.png`

## Texture Atlases

- `textures/source/screen_ui_atlas_v1.png`
- `textures/source/surface_material_atlas_v1.png`
- `textures/screens/screen_radar_v1.png`
- `textures/screens/screen_ecdis_chart_v1.png`
- `textures/screens/screen_engine_monitor_v1.png`
- `textures/screens/screen_comms_status_v1.png`
- `textures/surfaces/surface_carpet_navy_v1.png`
- `textures/surfaces/surface_ceiling_panels_v1.png`
- `textures/surfaces/surface_black_metal_v1.png`
- `textures/surfaces/surface_warm_wood_v1.png`

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
