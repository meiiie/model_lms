# Modern Bridge Cockpit

Version: v1.4
Created: 2026-05-10
Source: Generated procedurally with Codex + Blender Python from project-local ImageGen references.

## Purpose

High-context ship bridge cockpit asset for the VR Maritime LMS. This version
keeps the cockpit as real procedural geometry and uses generated raster textures
only where images are appropriate and mapping is stable: display screens. The
room shell, helm, telegraph, floor, ceiling, pillars, rails, and contact parts
use PBR materials plus real geometry detail.

v1.3 corrected the v1.2 texture-drift issue by removing unwrapped image textures
from contact-critical and large structural meshes. The ship wheel, telegraph
lever, telegraph dial, non-slip bridge floor, ceiling panels, window pillars,
rails, and wipers now use stable PBR materials plus real geometry detail until
they receive dedicated UV unwraps.

v1.4 adds Unity-ready training animation clips on proper pivots:
`helm_wheel_sweep`, `telegraph_lever_order_sweep`, and
`front_wipers_idle_sweep`. These are preview/hint/fallback clips; gameplay
should still drive the same pivots with XR or desktop interaction scripts.

`13_Modern_Bridge_Depth_Relief` was removed from the active pipeline because it
looked richer in a still render but did not provide trustworthy VR geometry.

## Runtime Exports

- `exports/ModernBridgeCockpit_VR_v1.4.fbx`
- `exports/ModernBridgeCockpit_VR_v1.4.glb`

## Source

- `source/ModernBridgeCockpit_VR_v1.4.blend`
- Generator script: `tools/blender_agent/create_modern_bridge_cockpit.py`
- Concept reference: `reference/imagegen_bridge_cockpit_reference_v1.png`

## Texture Atlases

- `textures/source/screen_ui_atlas_v1.png`
- `textures/source/surface_material_atlas_v1.png`
- `textures/source/interactive_material_atlas_v1.png`
- `textures/source/structure_material_atlas_v1.png`
- `textures/screens/screen_radar_v1.png`
- `textures/screens/screen_ecdis_chart_v1.png`
- `textures/screens/screen_engine_monitor_v1.png`
- `textures/screens/screen_comms_status_v1.png`
- `textures/surfaces/surface_carpet_navy_v1.png`
- `textures/surfaces/surface_ceiling_panels_v1.png`
- `textures/surfaces/surface_black_metal_v1.png`
- `textures/surfaces/surface_warm_wood_v1.png`
- `textures/interactive/interactive_black_rubber_v1.png`
- `textures/interactive/interactive_brushed_stainless_v1.png`
- `textures/interactive/interactive_red_bakelite_v1.png`
- `textures/interactive/interactive_telegraph_dial_v1.png`
- `textures/structure/structure_nonslip_floor_v1.png`
- `textures/structure/structure_ceiling_panels_v1.png`
- `textures/structure/structure_dark_steel_pillar_v1.png`
- `textures/structure/structure_brushed_rail_wiper_v1.png`

Only the screen textures are actively bound in v1.4. Surface, interaction, and
structure atlases are retained as art references until the affected meshes are
UV-unwrapped or replaced with authored material maps.

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

## Animation Clips

- `helm_wheel_sweep`: local-Y wheel rotation, -70 to +70 degrees.
- `telegraph_lever_order_sweep`: local-Y lever arc through astern, stop, and ahead detents.
- `front_wipers_idle_sweep`: local-Y window wiper sweep for ambient/weather scenarios.

These clips are intentionally simple and deterministic. Use them for preview,
lesson hints, or fallback demonstrations; drive interactable pivots from Unity
scripts during actual learner input.

## Runtime Notes

- Import the FBX into Unity first for native editor compatibility.
- Build colliders from `COL_` proxy objects, then hide or strip their renderers.
- Convert the telegraph, helm, and major console areas into prefabs before adding lesson scripts.
- Do not import this whole asset into Quest runtime unchanged; split or LOD it after visual approval.

## Provenance

Created inside the `model_lms` source asset repository. The image reference was
generated for this project and is stored only as concept/reference material.
