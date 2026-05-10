# Real Model Pipeline For VR Maritime LMS

Last reviewed: 2026-05-10

This note defines how this project should improve from generated bridge
concepts toward production VR assets. The rule is simple:

> Visual detail can be generated, but interaction surfaces must be modeled.

## Current Render Candidates

| Candidate | Folder | What it is good for | Current limitation |
|---|---|---|---|
| Procedural cockpit | `12_Modern_Bridge_Cockpit` | Real modular geometry, clear anchors, easy Unity colliders, generated texture atlases for displays, surfaces, interactables, and structure | Needs continued object-specific modeling passes |

Rejected experiment:
- `13_Modern_Bridge_Depth_Relief` was removed from the active library. It looked
  richer as a still image, but it was mostly image relief and did not provide
  trustworthy VR interaction geometry.

## Technique Ranking

Use these methods together instead of expecting one tool to solve the whole
bridge.

### 1. Photogrammetry or multi-view reconstruction

Best for real-world fidelity when the team can capture a real bridge or a
physical instrument from many angles. Use Meshroom/AliceVision, COLMAP, or a
similar reconstruction pipeline.

Use it for:
- Helm, telegraph, compass, radio, radar console, panel banks.
- Real texture reference, bevels, worn edges, screw placement, labels.

Do not use raw scan mesh directly in VR. Clean it first:
- Retopology or decimation.
- UV cleanup.
- Baked normal/AO maps.
- Separate colliders and pivots.

### 2. AI image-to-3D

Best for quickly generating shape candidates from reference images. Current
open-source candidates worth testing are Hunyuan3D, TRELLIS, TripoSR, and
InstantMesh.

Use it for:
- Fast first pass of small props.
- Shape studies for non-critical visual dressing.
- References that will be manually rebuilt in Blender.

Do not treat the output as final. Expect cleanup:
- Remove melted geometry and floating fragments.
- Rebuild hard-surface edges.
- Re-scale to metric units.
- Split interactive parts into separate transforms.

### 3. Image-to-texture / subtle relief

Best for distant or mid-range detail when the camera mostly sees the surface
from one direction.

Use it for:
- Back wall detail.
- Non-touch console face texture.
- Surface scratches, panel grooves, vents, small labels.

Do not use it for:
- Telegraph handle.
- Helm wheel.
- Any button, switch, lever, knob, or training target.

### 4. Manual hard-surface modeling

Best for the lesson-critical objects. It is slower but gives correct pivots,
grabbable handles, colliders, stable silhouettes, and readable training logic.

Use it for:
- Engine order telegraph.
- Steering wheel.
- Switches and knobs.
- Bridge collision shell.
- Hand-contact zones.

## Recommended Hybrid Workflow

1. Collect references.
   - One wide bridge front view.
   - Left, center, and right console closeups.
   - Close telegraph front/side/top views.
   - Close helm front/side views.
   - Bridge floor, window frames, and ceiling references.

2. Generate visual concept.
   - Use image generation only to align the art direction.
   - Keep this as reference, not as final geometry.

3. Build the modular bridge in Blender.
   - `BridgeShell`: walls, windows, ceiling, floor, rails.
   - `ConsoleBank`: static console surfaces and display frames.
   - `Telegraph`: separate base, dial, handle, pivot, detents.
   - `Helm`: wheel, column, rotation pivot.
   - `Displays`: screens as separate material slots for Unity UI/video.

4. Apply generated images only where they behave like real materials.
   - Display screens can use emissive radar/ECDIS/engine UI textures.
   - Carpet, non-slip floor, ceiling panels, black metal, brushed metal, red handle material, and wood can use subtle texture atlases.
   - Avoid full-room depth projection as a production asset.
   - For the helm and telegraph, texture the render mesh but keep the wheel, handle, detents, grab anchors, and colliders as real geometry.

5. Prepare VR interaction geometry.
   - Add simple convex colliders per part in Unity.
   - Add accurate grab anchors and pose anchors.
   - Use high-detail render mesh and low-detail collision mesh separately.

6. Optimize for runtime.
   - Use LODs for cockpit shell and distant exterior ship.
   - Keep interactables modular so Unity can cull and profile them separately.
   - Use texture atlases for static console details.
   - Keep physics colliders simple and stable.

## Acceptance Criteria Before Unity Import

For each production asset:

- Metric scale: 1 Blender unit = 1 meter.
- Origin/pivot is meaningful for interaction.
- Naming is stable and human-readable.
- Render mesh and collision mesh are separated.
- Materials are PBR-ready.
- No unapplied negative scale.
- No hidden helper geometry in export.
- FBX export opens in Unity without import warnings.
- README documents source, license/provenance, scale, intended collider, and
  lesson role.

## Immediate Next Improvement

The current best next step is not another full-room one-shot generation. It is:

1. Keep `12_Modern_Bridge_Cockpit` as the active production candidate.
2. Rebuild or replace lesson-critical details with the stronger existing
   assets:
   - `02_Ship_Wheel`
   - `04_Engine_Telegraph`
   - `08_ECDIS`
   - `09_Marine_Radar`
3. Keep generated screen textures active where they improve visual fidelity
   without faking interaction geometry.
4. Treat generated surface/interaction/structure atlases as reference material
   until the target meshes are UV-unwrapped or replaced with authored maps.
5. In Unity, expose only the real telegraph handle and helm as grabbable
   interactables.

This gives the best tradeoff: rich bridge visuals now, correct VR interaction
where the lesson depends on it.

## Source Links

- Unity LOD documentation: https://docs.unity3d.com/Manual/LevelOfDetail.html
- Unity mesh collider documentation: https://docs.unity3d.com/Manual/class-MeshCollider.html
- Unity model import documentation: https://docs.unity3d.com/Manual/ImportingModelFiles.html
- Blender Displace modifier: https://docs.blender.org/manual/en/latest/modeling/modifiers/deform/displace.html
- Blender material displacement: https://docs.blender.org/manual/en/latest/render/materials/components/displacement.html
- Meshroom manual: https://meshroom-manual.readthedocs.io/
- COLMAP documentation: https://colmap.github.io/
- Hunyuan3D: https://github.com/Tencent-Hunyuan/Hunyuan3D-2
- TRELLIS: https://github.com/microsoft/TRELLIS
- TripoSR: https://github.com/VAST-AI-Research/TripoSR
- InstantMesh: https://github.com/TencentARC/InstantMesh
