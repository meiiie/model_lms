# Blender Agent Pipeline

This folder contains deterministic Blender Python scripts used by Codex to
create and update source models for `model_lms`.

The intended workflow is:

1. Create or revise a model with a script in this folder.
2. Run Blender in background mode.
3. Write source `.blend`, runtime `.fbx` / `.glb`, and preview render outputs.
4. Review the generated model in Blender.
5. Sync only approved runtime exports into `VR_Maritime_LMS`.

## Local Blender

Detected on the current workstation:

```text
C:\Program Files\Blender Foundation\Blender 5.1\blender.exe
```

Example:

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.1\blender.exe" `
  --background `
  --python tools/blender_agent/create_bridge_alarm_panel.py `
  -- "E:\Sach\Sua\test\VR\model_lms"
```

Modern bridge cockpit:

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.1\blender.exe" `
  --background `
  --python tools/blender_agent/create_modern_bridge_cockpit.py `
  -- "E:\Sach\Sua\test\VR\model_lms"
```

Depth-relief cockpit:

```powershell
python tools/depth_pipeline/generate_depth_assets.py `
  12_Modern_Bridge_Cockpit/reference/imagegen_bridge_cockpit_reference_v1.png `
  13_Modern_Bridge_Depth_Relief/textures

& "C:\Program Files\Blender Foundation\Blender 5.1\blender.exe" `
  --background `
  --python tools/blender_agent/create_modern_bridge_depth_relief.py `
  -- "E:\Sach\Sua\test\VR\model_lms"
```

## Generators

| Script | Output folder | Runtime intent |
|---|---|---|
| `create_bridge_alarm_panel.py` | `11_Bridge_Alarm_Panel/` | Compact safety-control prop |
| `create_modern_bridge_cockpit.py` | `12_Modern_Bridge_Cockpit/` | Bridge layout/detail candidate with telegraph, helm, console, anchors, and collision proxies |
| `create_modern_bridge_depth_relief.py` | `13_Modern_Bridge_Depth_Relief/` | Image-to-depth hybrid with visual relief plus physical control proxies |

## Standards

- Author source geometry at real-world scale.
- Keep source `.blend` files in the model folder's `source/` directory.
- Put Unity runtime exports in `exports/`.
- Put render previews in `renders/`.
- Use simple collision-friendly geometry for controls.
- Record provenance and runtime-intent notes in each model README.

## Relationship To Image Generation

Image generation can be used for concept/reference boards, but the Blender
scripts are the source of truth for geometry. Generated images should be stored
as references, not as runtime model data, unless explicitly approved.
