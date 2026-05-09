# Image To Depth Pipeline

This folder contains deterministic utilities for turning a strong 2D bridge
reference into game-ready depth assets.

## Technique

The YouTube reference `8TRcluatftU` demonstrates the production idea:

1. Generate or obtain a depth map from a source image.
2. Use the source image as albedo.
3. Use the depth map as bump/parallax/displacement depending on distance.
4. Convert to real mesh only where the player needs close inspection or sculpting.

For VR training, this becomes a hybrid rule:

- Distant visual richness: albedo + normal/bump/parallax.
- Mid-range non-interactive surfaces: subdivided displacement relief.
- Touched controls: real mesh, real collider, real pivot, real hand pose.

## Local Fallback Generator

The fallback generator does not claim to be a monocular AI depth model. It
creates a cockpit-friendly height prior from the reference image so the pipeline
can run offline and remain reproducible.

```powershell
python tools/depth_pipeline/generate_depth_assets.py `
  12_Modern_Bridge_Cockpit/reference/imagegen_bridge_cockpit_reference_v1.png `
  13_Modern_Bridge_Depth_Relief/textures
```

For production art, replace `bridge_cockpit_height_2048.png` with a stronger
depth map from a dedicated depth-estimation tool, then rerun the Blender relief
generator.
