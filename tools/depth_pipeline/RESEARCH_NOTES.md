# Depth Map Research Notes

Source video: <https://www.youtube.com/watch?v=8TRcluatftU>

Local research artifacts are stored outside the repo at:

```text
E:\Sach\Sua\test\VR\_research\youtube_8TRcluatftU_depthmap
```

## Key Takeaways

- Depth maps are most useful for making flat surfaces respond to light as if
  they have raised/recessed detail.
- Bump/normal/parallax is cheap and convincing when the surface is not inspected
  at an extreme glancing angle.
- True displacement needs enough mesh subdivision, but too much displacement on
  a broad image causes warped windows, melted frames, and false silhouettes.
- For games, depth maps are best used to fake rooms, carved panels, scratches,
  and medium-distance detail while keeping runtime cost low.
- For VR training, anything the player grabs, blocks with their hand, or uses as
  a lesson target must remain real geometry with real colliders and pivots.

## Rule For VR Maritime LMS

Use image-to-depth as a visual layer, not as the physics layer.

| Surface type | Recommended method |
|---|---|
| Distant bridge detail, panels, room dressing | Albedo + normal/bump/parallax |
| Mid-range wall/console surface relief | Subtle mesh displacement |
| Telegraph handle, helm wheel, buttons, levers | Real mesh + collider + anchor + hand pose |

## Current Implementation

- `generate_depth_assets.py` creates albedo/height/normal maps from the cockpit
  reference image.
- `create_modern_bridge_depth_relief.py` builds a subtle displaced relief panel
  and adds physical proxies for the telegraph and helm.
- The first render used excessive displacement and produced wavy artifacts.
  The final v1 keeps displacement subtle and lets the normal map carry detail.
