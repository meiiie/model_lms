import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector


MODEL_DIR = "13_Modern_Bridge_Depth_Relief"
MODEL_NAME = "ModernBridgeDepthRelief_VR_v1.0"


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


def mat(name, color, metallic=0.0, roughness=0.55, emission=None, strength=0.0, alpha=1.0):
    material = bpy.data.materials.new(name)
    material.use_nodes = True
    material.diffuse_color = (color[0], color[1], color[2], alpha)
    bsdf = material.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        if "Base Color" in bsdf.inputs:
            bsdf.inputs["Base Color"].default_value = (color[0], color[1], color[2], alpha)
        if "Metallic" in bsdf.inputs:
            bsdf.inputs["Metallic"].default_value = metallic
        if "Roughness" in bsdf.inputs:
            bsdf.inputs["Roughness"].default_value = roughness
        if "Alpha" in bsdf.inputs:
            bsdf.inputs["Alpha"].default_value = alpha
        if emission:
            if "Emission Color" in bsdf.inputs:
                bsdf.inputs["Emission Color"].default_value = emission
            if "Emission Strength" in bsdf.inputs:
                bsdf.inputs["Emission Strength"].default_value = strength
    if alpha < 1.0:
        material.blend_method = "BLEND"
        material.show_transparent_back = True
    return material


def empty(name, loc, parent=None):
    obj = bpy.data.objects.new(name, None)
    obj.empty_display_type = "ARROWS"
    obj.empty_display_size = 0.16
    obj.location = loc
    bpy.context.collection.objects.link(obj)
    if parent:
        obj.parent = parent
    return obj


def cube(name, loc, scale, material=None, rotation=(0, 0, 0), parent=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rotation)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if material:
        obj.data.materials.append(material)
    if parent:
        obj.parent = parent
    return obj


def cyl(name, loc, radius, depth, material=None, vertices=48, rotation=(0, 0, 0), parent=None):
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
    if parent:
        obj.parent = parent
    try:
        bpy.ops.object.shade_smooth()
    except Exception:
        pass
    return obj


def sphere(name, loc, radius, material=None, parent=None):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=40, ring_count=18, radius=radius, location=loc)
    obj = bpy.context.object
    obj.name = name
    if material:
        obj.data.materials.append(material)
    if parent:
        obj.parent = parent
    try:
        bpy.ops.object.shade_smooth()
    except Exception:
        pass
    return obj


def torus(name, loc, major_radius, minor_radius, material=None, rotation=(0, 0, 0), parent=None):
    bpy.ops.mesh.primitive_torus_add(
        major_radius=major_radius,
        minor_radius=minor_radius,
        major_segments=96,
        minor_segments=14,
        location=loc,
        rotation=rotation,
    )
    obj = bpy.context.object
    obj.name = name
    if material:
        obj.data.materials.append(material)
    if parent:
        obj.parent = parent
    try:
        bpy.ops.object.shade_smooth()
    except Exception:
        pass
    return obj


def bevel(obj, amount=0.02, segments=2):
    mod = obj.modifiers.new("vr_bevel", "BEVEL")
    mod.width = amount
    mod.segments = segments
    mod.affect = "EDGES"
    obj.modifiers.new("weighted_normals", "WEIGHTED_NORMAL")
    return obj


def look_at(obj, target):
    direction = Vector(target) - obj.location
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def create_relief_material(albedo_path: Path, normal_path: Path):
    material = bpy.data.materials.new("mat_reference_depth_relief_albedo_normal")
    material.use_nodes = True
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    bsdf = nodes.get("Principled BSDF")

    albedo = nodes.new(type="ShaderNodeTexImage")
    albedo.name = "albedo_reference_image"
    albedo.image = bpy.data.images.load(str(albedo_path))
    albedo.extension = "CLIP"
    links.new(albedo.outputs["Color"], bsdf.inputs["Base Color"])

    normal_tex = nodes.new(type="ShaderNodeTexImage")
    normal_tex.name = "normal_from_depth_map"
    normal_tex.image = bpy.data.images.load(str(normal_path))
    normal_tex.image.colorspace_settings.name = "Non-Color"

    normal_map = nodes.new(type="ShaderNodeNormalMap")
    normal_map.inputs["Strength"].default_value = 0.55
    links.new(normal_tex.outputs["Color"], normal_map.inputs["Color"])
    links.new(normal_map.outputs["Normal"], bsdf.inputs["Normal"])

    if "Roughness" in bsdf.inputs:
        bsdf.inputs["Roughness"].default_value = 0.48
    if "Emission Color" in bsdf.inputs:
        bsdf.inputs["Emission Color"].default_value = (0.025, 0.035, 0.045, 1.0)
    if "Emission Strength" in bsdf.inputs:
        bsdf.inputs["Emission Strength"].default_value = 0.06

    return material


def load_height_pixels(height_path: Path):
    image = bpy.data.images.load(str(height_path))
    image.colorspace_settings.name = "Non-Color"
    width, height = image.size
    pixels = list(image.pixels)

    def sample(u: float, v: float) -> float:
        x = max(0, min(width - 1, int(u * (width - 1))))
        y = max(0, min(height - 1, int((1.0 - v) * (height - 1))))
        return pixels[(y * width + x) * 4]

    return sample


def create_depth_relief_mesh(parent, material, height_path: Path):
    sample_height = load_height_pixels(height_path)
    width_m = 10.8
    height_m = 6.075
    center_z = 1.48
    base_y = 2.45
    # Keep geometric displacement subtle. The normal map carries fine detail;
    # excessive mesh displacement turns flat windows and console edges wavy.
    displacement_m = 0.11
    nx = 192
    ny = 108

    verts = []
    uvs = []
    faces = []
    for iy in range(ny + 1):
        v = iy / ny
        for ix in range(nx + 1):
            u = ix / nx
            height = sample_height(u, v)
            x = (u - 0.5) * width_m
            z = center_z + (0.5 - v) * height_m
            y = base_y - height * displacement_m
            verts.append((x, y, z))
            uvs.append((u, 1.0 - v))

    for iy in range(ny):
        for ix in range(nx):
            a = iy * (nx + 1) + ix
            faces.append((a, a + 1, a + nx + 2, a + nx + 1))

    mesh = bpy.data.meshes.new("bridge_reference_depth_relief_mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()

    uv_layer = mesh.uv_layers.new(name="UVMap")
    loop_idx = 0
    for face in faces:
        for vi in face:
            uv_layer.data[loop_idx].uv = uvs[vi]
            loop_idx += 1

    obj = bpy.data.objects.new("visual_bridge_cockpit_depth_relief", mesh)
    obj.data.materials.append(material)
    obj.parent = parent
    obj["runtime_role"] = "visual_depth_relief_not_touchable"
    obj["displacement_source"] = str(height_path.name)
    bpy.context.collection.objects.link(obj)
    obj.modifiers.new("relief_weighted_normals", "WEIGHTED_NORMAL")
    return obj


def add_overlay_frames(parent):
    frame = bpy.data.materials["mat_frame_depth_overlay"]
    metal = bpy.data.materials["mat_brushed_metal"]
    dark = bpy.data.materials["mat_physical_dark"]

    # These frame bars deliberately sit in front of the depth relief, giving
    # strong VR parallax without requiring the entire bridge to be real mesh.
    y = 1.82
    bevel(cube("depth_overlay_top_window_header", (0, y, 2.74), (10.9, 0.10, 0.17), frame, parent=parent), 0.018, 2)
    bevel(cube("depth_overlay_console_sill", (0, y - 0.02, 0.69), (10.9, 0.12, 0.12), frame, parent=parent), 0.016, 2)
    for x in (-4.65, -3.10, -1.55, 0.0, 1.55, 3.10, 4.65):
        bevel(cube("depth_overlay_window_mullion", (x, y - 0.015, 1.82), (0.12, 0.12, 1.80), frame, parent=parent), 0.016, 2)
    for x in (-3.5, -1.15, 1.15, 3.5):
        cyl("depth_overlay_wiper_arm", (x, y - 0.08, 1.94), 0.010, 0.88, metal, 12, (0, math.radians(8), 0), parent)

    # Low-profile physical ledge for scale and occlusion.
    bevel(cube("depth_overlay_real_console_lip", (0, 0.55, 0.79), (9.6, 0.22, 0.12), dark, parent=parent), 0.025, 2)


def add_physical_controls(parent):
    metal = bpy.data.materials["mat_brushed_metal"]
    dark = bpy.data.materials["mat_physical_dark"]
    rubber = bpy.data.materials["mat_rubber"]
    red = bpy.data.materials["mat_handle_red"]

    # Real telegraph proxy: touchable, collidable, and slightly in front of the
    # image-relief telegraph. The image carries visual detail; this carries gameplay.
    bevel(cube("physical_telegraph_pedestal_proxy", (1.35, -0.58, 0.56), (0.52, 0.50, 1.05), dark, parent=parent), 0.04, 3)
    cyl("physical_telegraph_drum_proxy", (1.35, -0.72, 1.28), 0.38, 0.32, dark, 72, (math.radians(90), 0, 0), parent)
    torus("physical_telegraph_chrome_ring_proxy", (1.35, -0.90, 1.28), 0.39, 0.018, metal, (math.radians(90), 0, 0), parent)
    cyl("physical_telegraph_lever_stem_proxy", (1.35, -0.94, 1.67), 0.020, 0.58, metal, 32, (math.radians(12), 0, 0), parent)
    sphere("physical_telegraph_red_handle_proxy", (1.35, -1.04, 1.95), 0.085, red, parent)
    lever_anchor = empty("grab_target_telegraph_handle", (1.35, -1.06, 1.95), parent)
    lever_anchor["unity_anchor"] = True
    lever_anchor["preferred_hand"] = "right"

    # Real helm proxy, intentionally simpler than the background image.
    cyl("physical_helm_column_proxy", (-1.10, -0.62, 0.98), 0.08, 0.48, metal, 48, (math.radians(80), 0, 0), parent)
    wheel = torus("physical_helm_wheel_proxy", (-1.10, -0.88, 1.15), 0.32, 0.020, rubber, (math.radians(90), 0, 0), parent)
    wheel["interactive"] = True
    wheel["vr_action"] = "rotate"
    for i in range(6):
        a = i * math.tau / 6
        cyl(
            f"physical_helm_spoke_proxy_{i}",
            (-1.10 + math.cos(a) * 0.13, -0.89, 1.15 + math.sin(a) * 0.13),
            0.008,
            0.28,
            metal,
            12,
            (math.radians(90), 0, -a),
            parent,
        )
    empty("grab_target_helm_left", (-1.42, -0.94, 1.19), parent)["unity_anchor"] = True
    empty("grab_target_helm_right", (-0.78, -0.94, 1.19), parent)["unity_anchor"] = True


def add_collision_and_player_anchors(parent):
    proxy = bpy.data.materials["mat_collision_proxy"]
    specs = [
        ("COL_depth_relief_backstop", (0, 2.07, 1.45), (10.9, 0.12, 5.95)),
        ("COL_console_lip", (0, 0.52, 0.74), (9.8, 0.28, 0.22)),
        ("COL_telegraph_proxy", (1.35, -0.70, 1.06), (0.62, 0.72, 1.90)),
        ("COL_helm_proxy", (-1.10, -0.82, 1.06), (0.82, 0.45, 0.82)),
    ]
    for name, loc, scale in specs:
        obj = cube(name, loc, scale, proxy, parent=parent)
        obj.display_type = "WIRE"
        obj.hide_render = True
        obj["unity_collider"] = "BoxCollider"

    for name, loc in [
        ("player_start_desktop_vr", (0, -2.70, 1.58)),
        ("left_hand_rest_pose", (-0.48, -1.38, 1.28)),
        ("right_hand_rest_pose", (0.48, -1.38, 1.28)),
        ("lesson_focus_engine_telegraph", (1.35, -0.94, 1.68)),
        ("lesson_focus_helm", (-1.10, -0.88, 1.15)),
    ]:
        anchor = empty(name, loc, parent)
        anchor["unity_anchor"] = True


def create_model(root: Path):
    clean_scene()

    out_dir = root / MODEL_DIR
    source_dir = out_dir / "source"
    export_dir = out_dir / "exports"
    render_dir = out_dir / "renders"
    texture_dir = out_dir / "textures"
    reference_dir = out_dir / "reference"
    for directory in (source_dir, export_dir, render_dir, texture_dir, reference_dir):
        directory.mkdir(parents=True, exist_ok=True)

    albedo = texture_dir / "bridge_cockpit_albedo_2048.png"
    height = texture_dir / "bridge_cockpit_height_2048.png"
    normal = texture_dir / "bridge_cockpit_normal_2048.png"
    missing = [path for path in (albedo, height, normal) if not path.exists()]
    if missing:
        raise FileNotFoundError(
            "Depth texture set is missing. Run tools/depth_pipeline/generate_depth_assets.py first. "
            + ", ".join(str(path) for path in missing)
        )

    mat("mat_frame_depth_overlay", (0.055, 0.060, 0.060, 1), 0.45, 0.30)
    mat("mat_brushed_metal", (0.58, 0.59, 0.57, 1), 0.75, 0.23)
    mat("mat_physical_dark", (0.016, 0.018, 0.020, 1), 0.36, 0.38)
    mat("mat_rubber", (0.006, 0.005, 0.004, 1), 0.0, 0.82)
    mat("mat_handle_red", (0.95, 0.05, 0.025, 1), 0.0, 0.34, (1.0, 0.05, 0.02, 1), 0.15)
    mat("mat_collision_proxy", (1.0, 0.12, 0.04, 0.22), 0.0, 1.0, alpha=0.16)

    root_empty = empty("modern_bridge_depth_relief_root", (0, 0, 0))
    root_empty["model_id"] = "modern_bridge_depth_relief"
    root_empty["version"] = "v1.0"
    root_empty["technique"] = "albedo_plus_depth_mesh_plus_physical_control_proxies"
    root_empty["runtime_target"] = "Unity 6 VR training scene"

    relief_material = create_relief_material(albedo, normal)
    create_depth_relief_mesh(root_empty, relief_material, height)
    add_overlay_frames(root_empty)
    add_physical_controls(root_empty)
    add_collision_and_player_anchors(root_empty)

    bpy.ops.object.light_add(type="AREA", location=(0, -2.6, 2.75))
    key = bpy.context.object
    key.name = "render_soft_front_fill"
    key.data.energy = 360
    key.data.size = 4.8
    look_at(key, (0, 1.5, 1.35))

    bpy.ops.object.light_add(type="SUN", location=(0, 0, 6))
    sun = bpy.context.object
    sun.name = "render_sun_glancing_window_light"
    sun.data.energy = 1.25
    sun.rotation_euler = (math.radians(50), 0, math.radians(-32))

    bpy.ops.object.camera_add(location=(0, -3.55, 1.56))
    camera = bpy.context.object
    camera.name = "render_first_person_depth_relief_camera"
    look_at(camera, (0.22, 1.42, 1.48))
    camera.data.lens = 18
    camera.data.sensor_width = 32
    bpy.context.scene.camera = camera

    try:
        bpy.context.scene.render.engine = "BLENDER_EEVEE_NEXT"
        bpy.context.scene.eevee.taa_render_samples = 64
    except Exception:
        pass
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080
    bpy.context.scene.view_settings.view_transform = "Filmic"
    bpy.context.scene.view_settings.look = "Medium High Contrast"
    bpy.context.scene.render.filepath = str(render_dir / "ModernBridgeDepthRelief_hero.png")

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
        export_extras=True,
    )

    try:
        bpy.ops.render.render(write_still=True)
    except Exception as ex:
        print(f"Render failed: {ex}")

    (out_dir / "README.md").write_text(
        """# Modern Bridge Depth Relief

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
""",
        encoding="utf-8",
    )

    print(f"Saved {blend_path}")
    print(f"Exported {fbx_path}")
    print(f"Exported {glb_path}")
    print(f"Rendered {bpy.context.scene.render.filepath}")


if __name__ == "__main__":
    create_model(repo_root_from_args())
