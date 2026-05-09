# Modern Bridge Depth Relief

Version: v1.0
Created: 2026-05-10
Technique: Image albedo + generated depth map + displaced mesh + physical control proxies.

## Purpose

This asset tests the image-to-depth workflow from the depth-map Blender tutorial.
It gives the bridge a much richer visual surface than a blockout while keeping
gameplay-critical objects as real geometry.

## Files

- `textures/bridge_cockpit_albedo_2048.png`
- `textures/bridge_cockpit_height_2048.png`
- `textures/bridge_cockpit_normal_2048.png`
- `source/ModernBridgeDepthRelief_VR_v1.0.blend`
- `exports/ModernBridgeDepthRelief_VR_v1.0.fbx`
- `exports/ModernBridgeDepthRelief_VR_v1.0.glb`
- `renders/ModernBridgeDepthRelief_hero.png`

## Runtime Rule

Use this for bridge background/interior richness, not as the only gameplay
mesh. The telegraph and helm proxies included here show where real interactive
prefabs should sit in Unity.

## Interaction Anchors

- `player_start_desktop_vr`
- `left_hand_rest_pose`
- `right_hand_rest_pose`
- `grab_target_telegraph_handle`
- `grab_target_helm_left`
- `grab_target_helm_right`

## Unity Notes

- Import FBX first.
- Build colliders from `COL_` objects.
- Keep the albedo/height/normal texture max size at 2048 for desktop preview;
  use 1024 or split into modular panels for Quest.
- Replace the generated fallback height map with a stronger AI depth map when
  final art reference is approved.
