import math
import os
import sys
from pathlib import Path

import bpy
from mathutils import Vector


MODEL_DIR = "11_Bridge_Alarm_Panel"
MODEL_NAME = "BridgeAlarmPanel_VR_v1.0"


def repo_root_from_args() -> Path:
    if "--" in sys.argv:
        idx = sys.argv.index("--")
        if idx + 1 < len(sys.argv):
            return Path(sys.argv[idx + 1]).resolve()
    return Path(__file__).resolve().parents[2]


def clean_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()
    bpy.context.scene.unit_settings.system = "METRIC"
    bpy.context.scene.unit_settings.scale_length = 1.0


def mat(name, color, metallic=0.0, roughness=0.55, emission=None, strength=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        try:
            bsdf.inputs["Base Color"].default_value = color
            bsdf.inputs["Metallic"].default_value = metallic
            bsdf.inputs["Roughness"].default_value = roughness
            if emission:
                bsdf.inputs["Emission Color"].default_value = emission
                bsdf.inputs["Emission Strength"].default_value = strength
        except Exception:
            pass
    return m


def cube(name, loc, scale, material):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if material:
        obj.data.materials.append(material)
    return obj


def cylinder(name, loc, radius, depth, material, vertices=48, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=vertices,
        radius=radius,
        depth=depth,
        location=loc,
        rotation=rotation,
    )
    obj = bpy.context.object
    obj.name = name
    if material:
        obj.data.materials.append(material)
    try:
        bpy.ops.object.shade_smooth()
    except Exception:
        pass
    return obj


def bevel(obj, amount=0.015, segments=2):
    mod = obj.modifiers.new("small_bevel", "BEVEL")
    mod.width = amount
    mod.segments = segments
    mod.affect = "EDGES"
    obj.modifiers.new("weighted_normals", "WEIGHTED_NORMAL")
    return obj


def text_label(name, body, loc, size, material, align="CENTER"):
    bpy.ops.object.text_add(location=loc, rotation=(0, 0, 0))
    obj = bpy.context.object
    obj.name = name
    obj.data.body = body
    obj.data.align_x = align
    obj.data.align_y = "CENTER"
    obj.data.size = size
    obj.data.extrude = 0.001
    if material:
        obj.data.materials.append(material)
    return obj


def empty(name, loc):
    obj = bpy.data.objects.new(name, None)
    obj.empty_display_type = "ARROWS"
    obj.empty_display_size = 0.08
    obj.location = loc
    bpy.context.collection.objects.link(obj)
    return obj


def look_at(obj, target):
    direction = Vector(target) - obj.location
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def create_model(root: Path):
    clean_scene()

    out_dir = root / MODEL_DIR
    source_dir = out_dir / "source"
    export_dir = out_dir / "exports"
    render_dir = out_dir / "renders"
    for d in (source_dir, export_dir, render_dir):
        d.mkdir(parents=True, exist_ok=True)

    dark = mat("mat_dark_powder_coated_metal", (0.015, 0.018, 0.020, 1), 0.35, 0.38)
    face = mat("mat_graphite_control_face", (0.055, 0.065, 0.070, 1), 0.2, 0.45)
    rubber = mat("mat_black_rubber", (0.005, 0.005, 0.004, 1), 0.0, 0.82)
    red = mat("mat_emergency_red", (0.9, 0.02, 0.015, 1), 0.0, 0.35, (1.0, 0.03, 0.02, 1), 0.2)
    amber = mat("mat_alarm_amber", (1.0, 0.48, 0.02, 1), 0.0, 0.32, (1.0, 0.36, 0.02, 1), 0.35)
    green = mat("mat_status_green", (0.02, 0.72, 0.16, 1), 0.0, 0.38, (0.02, 0.6, 0.1, 1), 0.25)
    blue = mat("mat_silence_blue", (0.02, 0.18, 0.9, 1), 0.0, 0.35, (0.02, 0.12, 0.8, 1), 0.18)
    yellow = mat("mat_emergency_yellow_collar", (1.0, 0.78, 0.04, 1), 0.0, 0.38)
    white = mat("mat_engraved_white_text", (0.9, 0.95, 0.92, 1), 0.0, 0.5)

    root_empty = empty("bridge_alarm_panel_root", (0, 0, 0))
    root_empty["device_type"] = "Bridge_Alarm_Acknowledge_Panel"
    root_empty["category"] = "Maritime_Bridge_Safety"
    root_empty["interactive"] = True
    root_empty["unity_runtime_role"] = "safety_alarm_training_prop"

    base = bevel(cube("body_rear_housing", (0, 0, 0.035), (1.15, 0.42, 0.07), dark), 0.025, 3)
    plate = bevel(cube("panel_control_face", (0, 0, 0.088), (1.08, 0.36, 0.035), face), 0.018, 3)
    top_rail = bevel(cube("guard_top_rail", (0, 0.21, 0.16), (1.16, 0.035, 0.08), dark), 0.012, 2)
    bot_rail = bevel(cube("guard_bottom_rail", (0, -0.21, 0.16), (1.16, 0.035, 0.08), dark), 0.012, 2)

    for obj in (base, plate, top_rail, bot_rail):
        obj.parent = root_empty

    # Emergency mushroom button.
    cylinder("btn_emergency_yellow_guard", (-0.39, 0.03, 0.14), 0.115, 0.025, yellow)
    e_stop = cylinder("btn_emergency_stop_mushroom", (-0.39, 0.03, 0.19), 0.09, 0.065, red)
    bevel(e_stop, 0.012, 3)

    # Four training buttons.
    buttons = [
        ("btn_alarm_ack", "ACK", (-0.08, 0.085, 0.145), amber),
        ("btn_silence", "SILENCE", (0.17, 0.085, 0.145), blue),
        ("btn_general_alarm", "ALARM", (-0.08, -0.095, 0.145), red),
        ("btn_test_lamp", "TEST", (0.17, -0.095, 0.145), green),
    ]
    for obj_name, label, loc, material in buttons:
        cylinder(obj_name + "_bezel", loc, 0.064, 0.018, rubber)
        btn = cylinder(obj_name, (loc[0], loc[1], loc[2] + 0.025), 0.052, 0.035, material)
        btn["interactive"] = True
        btn["vr_action"] = "press"
        btn["lesson_signal"] = obj_name
        bevel(btn, 0.008, 3)
        text_label("label_" + obj_name, label, (loc[0], loc[1] - 0.088, 0.166), 0.035, white)
        empty("grab_target_" + obj_name, (loc[0], loc[1], loc[2] + 0.085))

    text_label("label_panel_title", "BRIDGE ALARM", (0.31, 0.18, 0.165), 0.045, white)
    text_label("label_panel_subtitle", "ACKNOWLEDGE / SILENCE", (0.31, 0.135, 0.165), 0.027, white)
    text_label("label_emergency", "EMERGENCY STOP", (-0.39, -0.11, 0.168), 0.03, white)

    # Guard posts around emergency button.
    for x in (-0.52, -0.26):
        for y in (-0.08, 0.14):
            post = cylinder("guard_post", (x, y, 0.18), 0.018, 0.11, dark, vertices=24)
            post.parent = root_empty

    for obj in bpy.context.scene.objects:
        if obj.name.startswith(("btn_", "label_", "guard_", "body_", "panel_", "grab_target_")):
            obj.parent = root_empty

    # Lighting and render camera.
    bpy.ops.object.light_add(type="AREA", location=(0, -1.1, 1.2))
    l = bpy.context.object
    l.name = "render_key_light"
    l.data.energy = 450
    l.data.size = 1.8
    look_at(l, (0, 0, 0.05))

    bpy.ops.object.camera_add(location=(1.05, -1.25, 0.75))
    cam = bpy.context.object
    look_at(cam, (0, 0, 0.08))
    cam.data.lens = 55
    bpy.context.scene.camera = cam

    try:
        bpy.context.scene.render.engine = "BLENDER_EEVEE_NEXT"
    except Exception:
        pass
    bpy.context.scene.render.resolution_x = 1600
    bpy.context.scene.render.resolution_y = 1000
    bpy.context.scene.view_settings.view_transform = "Filmic"
    bpy.context.scene.view_settings.look = "Medium High Contrast"
    bpy.context.scene.render.filepath = str(render_dir / "BridgeAlarmPanel_hero.png")

    blend_path = source_dir / f"{MODEL_NAME}.blend"
    fbx_path = export_dir / f"{MODEL_NAME}.fbx"
    glb_path = export_dir / f"{MODEL_NAME}.glb"

    bpy.ops.wm.save_as_mainfile(filepath=str(blend_path))

    bpy.ops.export_scene.fbx(
        filepath=str(fbx_path),
        use_selection=False,
        object_types={"EMPTY", "MESH", "OTHER"},
        apply_unit_scale=True,
        add_leaf_bones=False,
        path_mode="COPY",
        embed_textures=True,
        axis_forward="-Z",
        axis_up="Y",
    )

    bpy.ops.export_scene.gltf(
        filepath=str(glb_path),
        export_format="GLB",
        export_apply=True,
        export_yup=True,
    )

    try:
        bpy.ops.render.render(write_still=True)
    except Exception as ex:
        print(f"Render failed: {ex}")

    readme = out_dir / "README.md"
    readme.write_text(
        """# Bridge Alarm / Acknowledge Panel

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
""",
        encoding="utf-8",
    )

    print("Generated:")
    print(blend_path)
    print(fbx_path)
    print(glb_path)
    print(bpy.context.scene.render.filepath)


if __name__ == "__main__":
    create_model(repo_root_from_args())
