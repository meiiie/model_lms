import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector


MODEL_DIR = "12_Modern_Bridge_Cockpit"
MODEL_NAME = "ModernBridgeCockpit_VR_v1.2"


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
        def set_input(input_name, value):
            if input_name in bsdf.inputs:
                bsdf.inputs[input_name].default_value = value

        set_input("Base Color", (color[0], color[1], color[2], alpha))
        set_input("Metallic", metallic)
        set_input("Roughness", roughness)
        set_input("Alpha", alpha)
        if emission:
            set_input("Emission Color", emission)
            set_input("Emission Strength", strength)
    if alpha < 1.0:
        material.blend_method = "BLEND"
        material.use_screen_refraction = True
        material.show_transparent_back = True
    return material


def set_image_texture(material_name, image_path, emission_strength=0.0, roughness=None, metallic=None):
    image_path = Path(image_path)
    material = bpy.data.materials.get(material_name)
    if not material or not image_path.exists():
        return False

    material.use_nodes = True
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    bsdf = nodes.get("Principled BSDF")
    if not bsdf:
        return False

    image = bpy.data.images.load(str(image_path), check_existing=True)
    tex = nodes.new(type="ShaderNodeTexImage")
    tex.name = f"{material_name}_image"
    tex.label = image_path.name
    tex.image = image
    tex.extension = "REPEAT"
    try:
        image.colorspace_settings.name = "sRGB"
    except Exception:
        pass

    def clear_input_links(input_name):
        if input_name in bsdf.inputs:
            for link in list(bsdf.inputs[input_name].links):
                links.remove(link)

    clear_input_links("Base Color")
    links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])

    if emission_strength > 0.0:
        if "Emission Color" in bsdf.inputs:
            clear_input_links("Emission Color")
            links.new(tex.outputs["Color"], bsdf.inputs["Emission Color"])
        if "Emission Strength" in bsdf.inputs:
            bsdf.inputs["Emission Strength"].default_value = emission_strength

    if roughness is not None and "Roughness" in bsdf.inputs:
        bsdf.inputs["Roughness"].default_value = roughness
    if metallic is not None and "Metallic" in bsdf.inputs:
        bsdf.inputs["Metallic"].default_value = metallic

    material["texture_source"] = str(image_path.relative_to(image_path.parents[2])) if len(image_path.parents) > 2 else str(image_path)
    return True


def image_mat(name, image_path, fallback_color, metallic=0.0, roughness=0.34, emission_strength=0.0):
    material = mat(
        name,
        fallback_color,
        metallic=metallic,
        roughness=roughness,
        emission=fallback_color if emission_strength > 0 else None,
        strength=emission_strength,
    )
    set_image_texture(name, image_path, emission_strength, roughness, metallic)
    return material


def install_texture_materials(texture_dir):
    screen_dir = texture_dir / "screens"
    surface_dir = texture_dir / "surfaces"
    interactive_dir = texture_dir / "interactive"
    structure_dir = texture_dir / "structure"

    set_image_texture("mat_carpet_navy", structure_dir / "structure_nonslip_floor_v1.png", roughness=0.88)
    set_image_texture("mat_ceiling_dark", structure_dir / "structure_ceiling_panels_v1.png", roughness=0.66, metallic=0.08)
    set_image_texture("mat_console_dark", surface_dir / "surface_black_metal_v1.png", roughness=0.36, metallic=0.42)
    set_image_texture("mat_window_frame", structure_dir / "structure_dark_steel_pillar_v1.png", roughness=0.42, metallic=0.55)
    set_image_texture("mat_brushed_metal", interactive_dir / "interactive_brushed_stainless_v1.png", roughness=0.23, metallic=0.85)
    set_image_texture("mat_black_rubber", interactive_dir / "interactive_black_rubber_v1.png", roughness=0.90, metallic=0.0)
    set_image_texture("mat_warm_wood", surface_dir / "surface_warm_wood_v1.png", roughness=0.38)

    image_mat("mat_screen_radar", screen_dir / "screen_radar_v1.png", (0.02, 0.20, 0.14, 1), 0.0, 0.16, 1.25)
    image_mat("mat_screen_chart", screen_dir / "screen_ecdis_chart_v1.png", (0.02, 0.28, 0.45, 1), 0.0, 0.18, 1.05)
    image_mat("mat_screen_engine", screen_dir / "screen_engine_monitor_v1.png", (0.02, 0.16, 0.22, 1), 0.0, 0.18, 1.1)
    image_mat("mat_screen_comms", screen_dir / "screen_comms_status_v1.png", (0.02, 0.16, 0.25, 1), 0.0, 0.18, 1.1)
    image_mat("mat_red_bakelite", interactive_dir / "interactive_red_bakelite_v1.png", (0.78, 0.02, 0.01, 1), 0.0, 0.22, 0.08)
    image_mat("mat_telegraph_dial_face", interactive_dir / "interactive_telegraph_dial_v1.png", (0.01, 0.012, 0.012, 1), 0.0, 0.20, 0.16)
    image_mat("mat_marine_rail_metal", structure_dir / "structure_brushed_rail_wiper_v1.png", (0.62, 0.64, 0.62, 1), 0.85, 0.24, 0.0)


def empty(name, loc):
    obj = bpy.data.objects.new(name, None)
    obj.empty_display_type = "ARROWS"
    obj.empty_display_size = 0.12
    obj.location = loc
    bpy.context.collection.objects.link(obj)
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


def sphere(name, loc, radius, material=None, segments=32, ring_count=16, parent=None):
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=segments,
        ring_count=ring_count,
        radius=radius,
        location=loc,
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


def torus(name, loc, major_radius, minor_radius, material=None, rotation=(0, 0, 0), parent=None):
    bpy.ops.mesh.primitive_torus_add(
        major_segments=80,
        minor_segments=12,
        major_radius=major_radius,
        minor_radius=minor_radius,
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


def text_obj(name, body, loc, size, material=None, rotation=(math.radians(65), 0, 0), parent=None, align="CENTER"):
    bpy.ops.object.text_add(location=loc, rotation=rotation)
    obj = bpy.context.object
    obj.name = name
    obj.data.body = body
    obj.data.size = size
    obj.data.align_x = align
    obj.data.align_y = "CENTER"
    obj.data.extrude = 0.001
    if material:
        obj.data.materials.append(material)
    if parent:
        obj.parent = parent
    return obj


def assign_parent_by_prefix(parent, prefixes):
    for obj in bpy.context.scene.objects:
        if obj.name.startswith(prefixes):
            obj.parent = parent


def scale_objects_around(prefixes, center, factor):
    center_vec = Vector(center)
    for obj in bpy.context.scene.objects:
        if obj.name.startswith(prefixes):
            obj.location = center_vec + (obj.location - center_vec) * factor
            if obj.type != "EMPTY":
                obj.scale = (obj.scale.x * factor, obj.scale.y * factor, obj.scale.z * factor)


def create_ocean_mesh(parent, ocean_mat):
    width = 120.0
    length = 140.0
    nx = 70
    ny = 70
    verts = []
    faces = []
    for iy in range(ny + 1):
        y = 6.0 + (iy / ny) * length
        for ix in range(nx + 1):
            x = -width / 2.0 + (ix / nx) * width
            z = -0.72
            z += math.sin(x * 0.22 + y * 0.08) * 0.055
            z += math.sin(x * 0.07 - y * 0.14) * 0.035
            verts.append((x, y, z))
    for iy in range(ny):
        for ix in range(nx):
            a = iy * (nx + 1) + ix
            faces.append((a, a + 1, a + nx + 2, a + nx + 1))
    mesh = bpy.data.meshes.new("ocean_wave_preview_mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new("environment_ocean_wave_preview", mesh)
    obj.data.materials.append(ocean_mat)
    obj.parent = parent
    bpy.context.collection.objects.link(obj)
    return obj


def add_sky_backdrop(parent):
    sky = bpy.data.materials["mat_sky_backdrop"]
    cloud = bpy.data.materials["mat_soft_cloud"]

    backdrop = cube("environment_sky_backdrop", (0, 72.0, 18.0), (130.0, 0.05, 58.0), sky, parent=parent)
    backdrop["runtime_role"] = "render_review_backdrop"

    cloud_specs = [
        (-30, 70, 14.0, 8.0, 0.05, 1.4),
        (-18, 71, 18.2, 10.0, 0.05, 1.7),
        (7, 70, 15.8, 7.0, 0.05, 1.1),
        (26, 71, 19.0, 11.0, 0.05, 1.5),
        (42, 70, 13.6, 6.5, 0.05, 1.0),
    ]
    for i, (x, y, z, sx, sy, sz) in enumerate(cloud_specs):
        puff = sphere(f"environment_cloud_soft_puff_{i}", (x, y - 0.04, z), 1.0, cloud, 32, 12, parent)
        puff.scale = (sx, sy, sz)
        puff["runtime_role"] = "render_review_backdrop"


def add_monitor(parent, name, x, y, z, yaw, width=1.0, height=0.58, screen_type="radar"):
    dark = bpy.data.materials["mat_console_dark"]
    black = bpy.data.materials["mat_black_glass"]
    glass = bpy.data.materials["mat_blue_screen"]
    green = bpy.data.materials["mat_radar_green"]
    amber = bpy.data.materials["mat_amber_led"]
    cyan = bpy.data.materials["mat_cyan_ui"]

    rot = (math.radians(67), 0, yaw)
    body = bevel(cube(f"{name}_monitor_body", (x, y, z), (width + 0.14, 0.08, height + 0.14), dark, rot, parent), 0.025, 3)
    screen_material_name = {
        "radar": "mat_screen_radar",
        "chart": "mat_screen_chart",
        "engine": "mat_screen_engine",
        "comms": "mat_screen_comms",
        "nav": "mat_screen_engine",
    }.get(screen_type, "mat_blue_screen")
    screen_material = bpy.data.materials.get(screen_material_name, glass)
    screen = bevel(cube(f"{name}_screen_emissive", (x, y - 0.090, z + 0.035), (width, 0.010, height), screen_material, rot, parent), 0.01, 2)
    screen["display_role"] = screen_type
    screen["material_role"] = "generated_screen_texture"

    if screen_material_name == "mat_blue_screen":
        # Fallback geometry keeps the model usable if texture assets are absent.
        ui_parent = empty(f"{name}_ui_root", (x, y - 0.072, z + 0.03))
        ui_parent.rotation_euler = rot
        ui_parent.parent = parent

        if screen_type == "radar":
            for r in (0.10, 0.18, 0.26):
                ring = torus(f"{name}_radar_range_ring_{r:.2f}", (x, y - 0.079, z + 0.04), r, 0.003, green, rot, parent)
                ring.scale.x = width / height
            for angle in range(0, 180, 30):
                marker = cube(
                    f"{name}_radar_bearing_mark_{angle}",
                    (x, y - 0.082, z + 0.04),
                    (0.006, 0.006, height * 0.90),
                    green,
                    (rot[0], 0, yaw + math.radians(angle)),
                    parent,
                )
                marker["screen_markup"] = True
        elif screen_type == "chart":
            colors = [cyan, green, amber]
            for i in range(14):
                px = x - width * 0.38 + (i % 7) * width * 0.13
                pz = z - height * 0.26 + (i // 7) * height * 0.22
                patch = bevel(cube(f"{name}_chart_patch_{i}", (px, y - 0.081, pz), (width * 0.09, 0.006, height * 0.07), colors[i % 3], rot, parent), 0.003, 1)
                patch["screen_markup"] = True
            for i in range(6):
                line = cube(
                    f"{name}_route_line_{i}",
                    (x - width * 0.25 + i * width * 0.09, y - 0.083, z + height * 0.12 - i * height * 0.055),
                    (width * 0.20, 0.006, 0.006),
                    cyan,
                    (rot[0], 0, yaw - math.radians(14)),
                    parent,
                )
                line["screen_markup"] = True
        else:
            for i in range(9):
                col = [green, amber, cyan][i % 3]
                px = x - width * 0.35 + (i % 3) * width * 0.35
                pz = z - height * 0.22 + (i // 3) * height * 0.22
                widget = bevel(cube(f"{name}_nav_widget_{i}", (px, y - 0.081, pz), (width * 0.18, 0.006, height * 0.10), col, rot, parent), 0.004, 1)
                widget["screen_markup"] = True

    for i in range(4):
        cyl(
            f"{name}_side_knob_{i}",
            (x + width * 0.57, y - 0.08, z - height * 0.22 + i * height * 0.15),
            0.025,
            0.018,
            black,
            24,
            (math.radians(90), 0, 0),
            parent,
        )
    return body, screen


def add_button_row(parent, prefix, x0, y, z, count, spacing, material_names, rot=(math.radians(67), 0, 0)):
    black = bpy.data.materials["mat_black_rubber"]
    for i in range(count):
        material = bpy.data.materials[material_names[i % len(material_names)]]
        loc = (x0 + i * spacing, y, z)
        cyl(f"{prefix}_button_bezel_{i:02}", loc, 0.028, 0.012, black, 24, (math.radians(90), 0, 0), parent)
        button = cyl(f"{prefix}_button_{i:02}", (loc[0], loc[1] - 0.012, loc[2]), 0.020, 0.018, material, 24, (math.radians(90), 0, 0), parent)
        button["interactive"] = True
        button["vr_action"] = "press"


def add_upright_display(parent, name, x, y, z, width, height, screen_type):
    dark = bpy.data.materials["mat_console_dark"]
    metal = bpy.data.materials["mat_brushed_metal"]
    screen_material_name = {
        "radar": "mat_screen_radar",
        "chart": "mat_screen_chart",
        "engine": "mat_screen_engine",
        "comms": "mat_screen_comms",
    }[screen_type]
    screen_material = bpy.data.materials[screen_material_name]

    body = bevel(cube(f"{name}_upright_display_body", (x, y, z), (width + 0.16, 0.10, height + 0.16), dark, parent=parent), 0.025, 3)
    screen = bevel(cube(f"{name}_upright_display_screen", (x, y - 0.058, z), (width, 0.012, height), screen_material, parent=parent), 0.006, 1)
    led_bar = bevel(cube(f"{name}_upright_display_status_bar", (x, y - 0.066, z - height * 0.58), (width * 0.86, 0.012, 0.022), metal, parent=parent), 0.004, 1)
    body["runtime_role"] = "static_bridge_display"
    screen["display_role"] = screen_type
    screen["material_role"] = "generated_screen_texture"
    led_bar["runtime_role"] = "static_bridge_display_detail"
    return body, screen


def add_upright_display_cluster(parent):
    specs = [
        ("left_radar", -3.75, "radar"),
        ("left_chart", -2.45, "chart"),
        ("right_engine", 2.45, "engine"),
        ("right_comms", 3.75, "comms"),
    ]
    for name, x, screen_type in specs:
        add_upright_display(parent, name, x, 0.43, 1.38, 1.02, 0.62, screen_type)


def add_console_bank(parent):
    dark = bpy.data.materials["mat_console_dark"]
    metal = bpy.data.materials["mat_brushed_metal"]
    wood = bpy.data.materials["mat_warm_wood"]
    rubber = bpy.data.materials["mat_black_rubber"]
    amber = bpy.data.materials["mat_amber_led"]
    cyan = bpy.data.materials["mat_cyan_ui"]

    for i, x in enumerate((-3.75, -2.45, -1.15, 1.15, 2.45, 3.75)):
        yaw = math.radians(0)
        top = bevel(cube(f"console_top_module_{i:02}", (x, 1.18, 0.96), (1.22, 0.86, 0.20), dark, (math.radians(-12), 0, yaw), parent), 0.035, 3)
        base = bevel(cube(f"console_wood_cabinet_{i:02}", (x, 1.00, 0.45), (1.22, 0.62, 0.76), wood, (0, 0, yaw), parent), 0.025, 2)
        rail = bevel(cube(f"console_front_metal_lip_{i:02}", (x, 0.66, 0.82), (1.26, 0.06, 0.07), metal, parent=parent), 0.012, 2)
        top["runtime_role"] = "static_bridge_console"
        base["runtime_role"] = "static_bridge_console"
        rail["runtime_role"] = "static_bridge_console"

        screen_type = ["radar", "chart", "engine", "comms", "radar", "chart"][i]
        add_monitor(parent, f"monitor_{i:02}", x, 0.66, 1.23, yaw, 0.92, 0.54, screen_type)
        add_button_row(
            parent,
            f"console_{i:02}",
            x - 0.42,
            0.54,
            0.82,
            7,
            0.14,
            ["mat_amber_led", "mat_green_led", "mat_red_led", "mat_cyan_ui"],
        )

        for d in range(2):
            drawer = bevel(cube(f"console_drawer_{i:02}_{d}", (x, 0.60, 0.32 + d * 0.25), (0.92, 0.035, 0.16), dark, parent=parent), 0.009, 1)
            handle = bevel(cube(f"console_drawer_handle_{i:02}_{d}", (x, 0.565, 0.32 + d * 0.25), (0.24, 0.025, 0.025), metal, parent=parent), 0.006, 1)
            drawer["runtime_role"] = "static_bridge_console"
            handle["runtime_role"] = "static_bridge_console"

    # Central lower console and equipment shelf.
    bevel(cube("central_navigation_plinth", (0, 0.98, 0.52), (1.32, 0.76, 0.90), dark, parent=parent), 0.035, 3)
    bevel(cube("central_sloped_control_panel", (0, 0.52, 0.98), (1.18, 0.72, 0.14), dark, (math.radians(-16), 0, 0), parent), 0.025, 2)
    add_button_row(parent, "central_nav_panel", -0.45, 0.36, 0.98, 8, 0.13, ["mat_amber_led", "mat_green_led", "mat_red_led", "mat_cyan_ui"])

    for i, x in enumerate((-0.28, 0.0, 0.28)):
        cyl(f"central_selector_knob_{i}", (x, 0.34, 1.05), 0.045, 0.04, rubber, 32, (math.radians(90), 0, 0), parent)
        cyl(f"central_selector_cap_{i}", (x, 0.315, 1.05), 0.035, 0.018, metal, 32, (math.radians(90), 0, 0), parent)

    # Compass binnacle dome.
    cyl("magnetic_compass_base", (0, 1.15, 1.08), 0.22, 0.14, dark, 64, parent=parent)
    dome = sphere("magnetic_compass_glass_dome", (0, 1.15, 1.20), 0.24, bpy.data.materials["mat_window_glass"], 48, 16, parent)
    dome.scale.z = 0.42
    dome["runtime_role"] = "decorative_navigation_instrument"
    torus("magnetic_compass_chrome_ring", (0, 1.15, 1.18), 0.22, 0.012, metal, parent=parent)

    # Radio handset and cord on left console.
    handset = bevel(cube("vhf_hanging_handset", (-4.40, 0.44, 0.68), (0.12, 0.07, 0.32), rubber, (0, 0, math.radians(8)), parent), 0.025, 3)
    handset["runtime_role"] = "decorative_handset"
    for i in range(9):
        cyl(f"vhf_coiled_cord_segment_{i}", (-4.26 + i * 0.035, 0.43, 0.80 - math.sin(i * 0.9) * 0.06), 0.009, 0.09, rubber, 12, (0, math.radians(80), math.radians(90)), parent)


def add_windows_and_ship(parent):
    frame = bpy.data.materials["mat_window_frame"]
    glass = bpy.data.materials["mat_window_glass"]
    metal = bpy.data.materials["mat_marine_rail_metal"]
    dark = bpy.data.materials["mat_console_dark"]
    deck = bpy.data.materials["mat_ship_deck"]

    # Front window band with thick bridge mullions.
    y = 2.55
    bevel(cube("front_bridge_header_beam", (0, y, 2.55), (10.3, 0.18, 0.28), frame, parent=parent), 0.025, 2)
    bevel(cube("front_bridge_sill_beam", (0, y, 1.08), (10.3, 0.18, 0.22), frame, parent=parent), 0.025, 2)
    for x in (-5.05, -3.35, -1.68, 0.0, 1.68, 3.35, 5.05):
        col = bevel(cube("front_window_mullion", (x, y, 1.83), (0.16, 0.22, 1.55), frame, (0, 0, math.radians(-5 if x < 0 else 5)), parent), 0.02, 2)
        col["runtime_role"] = "bridge_window_frame"
    for i, x in enumerate((-4.2, -2.5, -0.84, 0.84, 2.5, 4.2)):
        pane = cube(f"front_window_glass_panel_{i}", (x, y + 0.015, 1.86), (1.42, 0.025, 1.24), glass, parent=parent)
        pane["runtime_role"] = "transparent_bridge_window"
        # Wipers.
        cyl(f"front_window_wiper_pivot_{i}", (x + 0.46, y - 0.045, 2.42), 0.025, 0.025, metal, 24, (math.radians(90), 0, 0), parent)
        blade = bevel(cube(f"front_window_wiper_arm_{i}", (x + 0.30, y - 0.055, 1.93), (0.035, 0.025, 0.92), metal, (0, 0, math.radians(-9)), parent), 0.005, 1)
        blade["runtime_role"] = "decorative_wiper"

    # Side frames hint a wrap-around bridge.
    for side, sx in (("left", -5.20), ("right", 5.20)):
        bevel(cube(f"{side}_side_window_frame", (sx, 0.55, 1.86), (0.14, 3.6, 1.42), frame, parent=parent), 0.025, 2)
        for j in range(2):
            pane = cube(f"{side}_side_window_glass_{j}", (sx, -0.12 + j * 1.35, 1.86), (0.028, 1.10, 1.14), glass, parent=parent)
            pane["runtime_role"] = "transparent_bridge_window"

    # Bow and rail outside the windows for strong maritime context.
    bow = bevel(cube("ship_bow_deck_visible_from_bridge", (0, 9.6, -0.25), (3.0, 9.0, 0.16), deck, parent=parent), 0.02, 1)
    bow.scale.x = 0.72
    bow["runtime_role"] = "exterior_reference_geometry"
    bevel(cube("ship_bow_raised_forecastle", (0, 14.0, 0.05), (1.55, 1.35, 0.36), dark, parent=parent), 0.035, 2)
    cyl("ship_bow_mast", (0, 15.1, 1.05), 0.035, 2.2, metal, 24, parent=parent)
    cyl("ship_bow_mast_crossbar", (0, 15.1, 1.70), 0.018, 1.1, metal, 16, (0, math.radians(90), 0), parent)

    for x in (-1.75, 1.75):
        cyl(f"bow_rail_longitudinal_{x}", (x, 10.4, 0.32), 0.014, 8.4, metal, 12, (math.radians(90), 0, 0), parent)
        for k in range(8):
            cyl(f"bow_rail_post_{x}_{k}", (x, 6.7 + k * 1.05, 0.16), 0.018, 0.72, metal, 12, parent=parent)


def add_helm(parent):
    metal = bpy.data.materials["mat_brushed_metal"]
    rubber = bpy.data.materials["mat_black_rubber"]
    dark = bpy.data.materials["mat_console_dark"]

    bevel(cube("helm_pedestal", (-1.10, 0.14, 0.58), (0.48, 0.44, 0.92), dark, parent=parent), 0.035, 3)
    cyl("helm_column", (-1.10, 0.07, 1.05), 0.10, 0.42, metal, 48, (math.radians(77), 0, 0), parent)
    wheel = torus("helm_wheel_outer_ring", (-1.10, -0.14, 1.18), 0.37, 0.022, rubber, (math.radians(90), 0, 0), parent)
    wheel["interactive"] = True
    wheel["vr_action"] = "rotate"
    wheel["axis"] = "local_y"
    cyl("helm_wheel_hub", (-1.10, -0.16, 1.18), 0.10, 0.08, metal, 48, (math.radians(90), 0, 0), parent)
    for i in range(8):
        a = i * math.tau / 8
        sx = math.cos(a) * 0.18
        sz = math.sin(a) * 0.18
        spoke = cyl(
            f"helm_wheel_spoke_{i}",
            (-1.10 + sx, -0.16, 1.18 + sz),
            0.010,
            0.35,
            metal,
            16,
            (math.radians(90), 0, -a),
            parent,
        )
        spoke["runtime_role"] = "interactive_helm_detail"
    for i in range(8):
        a = i * math.tau / 8
        sphere(f"helm_wheel_handle_{i}", (-1.10 + math.cos(a) * 0.40, -0.16, 1.18 + math.sin(a) * 0.40), 0.045, rubber, 24, 12, parent)
    empty("grab_target_helm_left", (-1.48, -0.20, 1.22)).parent = parent
    empty("grab_target_helm_right", (-0.72, -0.20, 1.22)).parent = parent


def add_engine_telegraph(parent):
    metal = bpy.data.materials["mat_brushed_metal"]
    dark = bpy.data.materials["mat_console_dark"]
    black = bpy.data.materials["mat_telegraph_dial_face"]
    red = bpy.data.materials["mat_red_bakelite"]
    green = bpy.data.materials["mat_green_led"]
    amber = bpy.data.materials["mat_amber_led"]
    white = bpy.data.materials["mat_label_white"]

    bevel(cube("telegraph_floor_pedestal", (1.05, -0.26, 0.50), (0.58, 0.58, 0.90), dark, parent=parent), 0.05, 4)
    cyl("telegraph_round_base_chrome", (1.05, -0.26, 0.98), 0.34, 0.10, metal, 80, parent=parent)
    cyl("telegraph_drum_body", (1.05, -0.26, 1.22), 0.46, 0.42, dark, 96, (math.radians(90), 0, 0), parent)
    dial = cyl("telegraph_front_dial_face_textured", (1.05, -0.48, 1.22), 0.43, 0.035, black, 96, (math.radians(90), 0, 0), parent)
    dial["material_role"] = "generated_telegraph_dial_texture"
    torus("telegraph_chrome_outer_ring", (1.05, -0.50, 1.22), 0.45, 0.018, metal, (math.radians(90), 0, 0), parent)

    labels = [
        ("FULL AST", red, -52),
        ("HALF", amber, -30),
        ("STOP", white, 0),
        ("SLOW", green, 30),
        ("FULL AHD", green, 52),
    ]
    for i, (label, material, deg) in enumerate(labels):
        x = 1.05 + math.sin(math.radians(deg)) * 0.28
        z = 1.22 + math.cos(math.radians(deg)) * 0.26
        tick = cube(f"telegraph_order_tick_{i}", (x, -0.525, z), (0.09, 0.010, 0.020), material, (0, 0, math.radians(-deg)), parent)
        tick["telegraph_order"] = label
        text_obj(
            f"telegraph_label_{i}",
            label,
            (x, -0.54, z - 0.05),
            0.045,
            material,
            (math.radians(90), 0, 0),
            parent,
        )

    lever_root = empty("telegraph_lever_pivot", (1.05, -0.50, 1.36))
    lever_root.parent = parent
    lever_root["interactive"] = True
    lever_root["vr_action"] = "lever_arc"
    lever_root["arc_degrees"] = 104
    lever_root["lesson_signal"] = "engine_order_telegraph"
    cyl("telegraph_lever_stem", (1.05, -0.61, 1.67), 0.025, 0.64, metal, 32, (math.radians(13), 0, 0), parent)
    sphere("telegraph_red_handle_grip", (1.05, -0.71, 1.98), 0.095, red, 40, 20, parent)
    empty("grab_target_telegraph_handle", (1.05, -0.73, 1.98)).parent = parent
    empty("hand_pose_telegraph_right", (1.20, -0.78, 1.86)).parent = parent
    empty("hand_pose_telegraph_left", (0.88, -0.78, 1.86)).parent = parent


def add_room_shell(parent):
    floor_mat = bpy.data.materials["mat_carpet_navy"]
    wall_mat = bpy.data.materials["mat_bridge_wall"]
    ceiling_mat = bpy.data.materials["mat_ceiling_dark"]
    metal = bpy.data.materials["mat_brushed_metal"]
    dark = bpy.data.materials["mat_console_dark"]
    rubber = bpy.data.materials["mat_black_rubber"]

    floor = bevel(cube("bridge_floor_collision_visible", (0, -0.65, -0.04), (10.6, 7.8, 0.08), floor_mat, parent=parent), 0.02, 1)
    floor["collision_hint"] = "box"
    ceiling = bevel(cube("bridge_ceiling_panel", (0, -0.35, 2.82), (10.6, 7.8, 0.12), ceiling_mat, parent=parent), 0.02, 1)
    ceiling["runtime_role"] = "static_bridge_shell"
    back_wall = bevel(cube("bridge_rear_wall", (0, -3.95, 1.38), (10.6, 0.12, 2.75), wall_mat, parent=parent), 0.02, 1)
    back_wall["runtime_role"] = "static_bridge_shell"
    left_wall = bevel(cube("bridge_left_wall", (-5.28, -0.65, 1.38), (0.12, 7.8, 2.75), wall_mat, parent=parent), 0.02, 1)
    right_wall = bevel(cube("bridge_right_wall", (5.28, -0.65, 1.38), (0.12, 7.8, 2.75), wall_mat, parent=parent), 0.02, 1)

    # Real geometry seams keep the floor/ceiling readable in VR even when
    # texture mipmaps soften at headset distance.
    for i, x in enumerate((-4.20, -2.80, -1.40, 0.0, 1.40, 2.80, 4.20)):
        seam = bevel(cube(f"floor_panel_longitudinal_seam_{i}", (x, -0.65, 0.018), (0.018, 7.15, 0.012), rubber, parent=parent), 0.003, 1)
        seam["runtime_role"] = "floor_panel_geometry_detail"
    for i, y in enumerate((-3.35, -2.25, -1.15, -0.05, 1.05, 2.15)):
        seam = bevel(cube(f"floor_panel_cross_seam_{i}", (0, y, 0.020), (10.15, 0.016, 0.012), rubber, parent=parent), 0.003, 1)
        seam["runtime_role"] = "floor_panel_geometry_detail"
    for i, y in enumerate((-2.95, -2.55, -2.15, -1.75, -1.35)):
        strip = bevel(cube(f"floor_player_antislip_strip_{i}", (0, y, 0.030), (2.20, 0.026, 0.014), dark, parent=parent), 0.004, 1)
        strip["runtime_role"] = "floor_antislip_contact_detail"

    for i, x in enumerate((-3.9, -1.3, 1.3, 3.9)):
        beam = bevel(cube(f"ceiling_cross_beam_{i}", (x, -0.35, 2.735), (0.075, 7.25, 0.075), dark, parent=parent), 0.012, 2)
        beam["runtime_role"] = "ceiling_geometry_detail"
    for i, y in enumerate((-2.8, -1.3, 0.2, 1.7)):
        beam = bevel(cube(f"ceiling_longitudinal_beam_{i}", (0, y, 2.728), (10.15, 0.055, 0.060), dark, parent=parent), 0.010, 2)
        beam["runtime_role"] = "ceiling_geometry_detail"

    for i, x in enumerate((-3.8, -1.3, 1.3, 3.8)):
        bevel(cube(f"ceiling_light_panel_{i}", (x, -0.92, 2.74), (1.15, 0.12, 0.035), bpy.data.materials["mat_soft_light"], parent=parent), 0.015, 2)
        cyl(f"ceiling_vent_round_{i}", (x + 0.6, 0.85, 2.735), 0.16, 0.018, metal, 48, parent=parent)


def add_collision_and_anchors(parent):
    collision_mat = bpy.data.materials["mat_collision_proxy"]
    specs = [
        ("COL_bridge_floor", (0, -0.65, 0.04), (10.6, 7.8, 0.08)),
        ("COL_console_bank", (0, 0.96, 0.82), (9.9, 1.00, 1.12)),
        ("COL_telegraph_pedestal", (1.05, -0.28, 0.86), (0.70, 0.70, 1.72)),
        ("COL_helm_pedestal", (-1.10, 0.04, 0.72), (0.68, 0.62, 1.44)),
        ("COL_left_wall", (-5.28, -0.65, 1.38), (0.12, 7.8, 2.75)),
        ("COL_right_wall", (5.28, -0.65, 1.38), (0.12, 7.8, 2.75)),
        ("COL_rear_wall", (0, -3.95, 1.38), (10.6, 0.12, 2.75)),
        ("COL_front_window_band", (0, 2.56, 1.70), (10.6, 0.18, 1.90)),
    ]
    for name, loc, scale in specs:
        proxy = cube(name, loc, scale, collision_mat, parent=parent)
        proxy.display_type = "WIRE"
        proxy.hide_render = True
        proxy["unity_collider"] = "BoxCollider"
        proxy["runtime_role"] = "collision_proxy"

    for name, loc in [
        ("player_start_desktop_vr", (0, -1.95, 1.62)),
        ("left_hand_rest_pose", (-0.46, -1.10, 1.28)),
        ("right_hand_rest_pose", (0.46, -1.10, 1.28)),
        ("lesson_focus_engine_telegraph", (1.05, -0.55, 1.65)),
        ("lesson_focus_helm", (-1.10, -0.18, 1.20)),
    ]:
        anchor = empty(name, loc)
        anchor.parent = parent
        anchor["unity_anchor"] = True


def create_model(root: Path):
    clean_scene()

    out_dir = root / MODEL_DIR
    source_dir = out_dir / "source"
    export_dir = out_dir / "exports"
    render_dir = out_dir / "renders"
    reference_dir = out_dir / "reference"
    texture_dir = out_dir / "textures"
    for directory in (source_dir, export_dir, render_dir, reference_dir, texture_dir):
        directory.mkdir(parents=True, exist_ok=True)

    # PBR-ish materials. These are intentionally procedural and lightweight.
    mat("mat_console_dark", (0.020, 0.024, 0.026, 1), 0.35, 0.34)
    mat("mat_black_glass", (0.002, 0.004, 0.006, 1), 0.1, 0.12, (0.02, 0.06, 0.10, 1), 0.05)
    mat("mat_brushed_metal", (0.55, 0.57, 0.56, 1), 0.75, 0.22)
    mat("mat_window_frame", (0.10, 0.105, 0.105, 1), 0.5, 0.28)
    mat("mat_window_glass", (0.72, 0.90, 1.0, 1), 0.0, 0.03, (0.08, 0.16, 0.22, 1), 0.01, alpha=0.10)
    mat("mat_carpet_navy", (0.006, 0.018, 0.040, 1), 0.0, 0.92)
    mat("mat_bridge_wall", (0.19, 0.23, 0.24, 1), 0.0, 0.72)
    mat("mat_ceiling_dark", (0.045, 0.050, 0.055, 1), 0.1, 0.62)
    mat("mat_warm_wood", (0.46, 0.22, 0.09, 1), 0.0, 0.42)
    mat("mat_ship_deck", (0.20, 0.25, 0.30, 1), 0.2, 0.48)
    mat("mat_ocean_teal", (0.00, 0.23, 0.32, 1), 0.0, 0.18, (0.00, 0.08, 0.12, 1), 0.03)
    mat("mat_sky_backdrop", (0.44, 0.72, 0.96, 1), 0.0, 0.65, (0.18, 0.34, 0.55, 1), 0.12)
    mat("mat_soft_cloud", (0.92, 0.95, 0.96, 1), 0.0, 0.78, (0.52, 0.58, 0.62, 1), 0.05, alpha=0.68)
    mat("mat_blue_screen", (0.02, 0.10, 0.16, 1), 0.0, 0.20, (0.02, 0.20, 0.42, 1), 0.55)
    mat("mat_radar_green", (0.05, 0.95, 0.38, 1), 0.0, 0.35, (0.02, 0.80, 0.30, 1), 0.75)
    mat("mat_cyan_ui", (0.02, 0.82, 1.0, 1), 0.0, 0.28, (0.02, 0.60, 1.0, 1), 0.65)
    mat("mat_amber_led", (1.0, 0.42, 0.02, 1), 0.0, 0.32, (1.0, 0.32, 0.02, 1), 0.75)
    mat("mat_green_led", (0.02, 0.75, 0.18, 1), 0.0, 0.34, (0.02, 0.55, 0.12, 1), 0.65)
    mat("mat_red_led", (0.95, 0.04, 0.02, 1), 0.0, 0.34, (0.95, 0.02, 0.02, 1), 0.65)
    mat("mat_label_white", (0.92, 0.96, 0.96, 1), 0.0, 0.60, (0.60, 0.75, 0.80, 1), 0.18)
    mat("mat_black_rubber", (0.004, 0.004, 0.003, 1), 0.0, 0.86)
    mat("mat_soft_light", (0.85, 0.92, 1.0, 1), 0.0, 0.2, (0.75, 0.88, 1.0, 1), 1.2)
    mat("mat_collision_proxy", (1.0, 0.12, 0.04, 0.25), 0.0, 1.0, alpha=0.18)
    install_texture_materials(texture_dir)

    root_empty = empty("modern_bridge_cockpit_root", (0, 0, 0))
    root_empty["model_id"] = "modern_bridge_cockpit"
    root_empty["version"] = "v1.2"
    root_empty["unit_scale"] = "meters"
    root_empty["runtime_target"] = "Unity 6 VR training scene"
    root_empty["reference_image"] = "reference/imagegen_bridge_cockpit_reference_v1.png"
    root_empty["texture_strategy"] = "procedural geometry plus project-local ImageGen screen and surface atlases"
    root_empty["interactive_anchors"] = "telegraph, helm, screens"

    create_ocean_mesh(root_empty, bpy.data.materials["mat_ocean_teal"])
    add_sky_backdrop(root_empty)
    add_room_shell(root_empty)
    add_windows_and_ship(root_empty)
    add_console_bank(root_empty)
    add_upright_display_cluster(root_empty)
    add_helm(root_empty)
    add_engine_telegraph(root_empty)
    scale_objects_around(
        ("telegraph_", "grab_target_telegraph", "hand_pose_telegraph"),
        (1.05, -0.30, 0.50),
        0.84,
    )
    add_collision_and_anchors(root_empty)

    # Camera and lighting for the review render.
    bpy.ops.object.light_add(type="SUN", location=(0, 0, 4))
    sun = bpy.context.object
    sun.name = "render_sun_from_starboard_window"
    sun.data.energy = 2.4
    sun.rotation_euler = (math.radians(42), 0, math.radians(-34))

    bpy.ops.object.light_add(type="AREA", location=(0.0, -2.15, 2.35))
    key = bpy.context.object
    key.name = "render_soft_bridge_fill"
    key.data.energy = 420
    key.data.size = 5.2
    look_at(key, (0, 0.8, 1.15))

    bpy.ops.object.camera_add(location=(0.0, -3.72, 1.55))
    cam = bpy.context.object
    cam.name = "render_first_person_bridge_camera"
    look_at(cam, (0.15, 0.92, 1.30))
    cam.data.lens = 17
    cam.data.sensor_width = 32
    bpy.context.scene.camera = cam

    # Rendering settings: stable and fast enough for workstation iteration.
    try:
        bpy.context.scene.render.engine = "BLENDER_EEVEE_NEXT"
        bpy.context.scene.eevee.taa_render_samples = 64
    except Exception:
        pass
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080
    bpy.context.scene.view_settings.view_transform = "Filmic"
    bpy.context.scene.view_settings.look = "Medium High Contrast"
    bpy.context.scene.render.filepath = str(render_dir / "ModernBridgeCockpit_hero.png")

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

    readme = out_dir / "README.md"
    readme.write_text(
        """# Modern Bridge Cockpit

Version: v1.2
Created: 2026-05-10
Source: Generated procedurally with Codex + Blender Python from project-local ImageGen references.

## Purpose

High-context ship bridge cockpit asset for the VR Maritime LMS. This version
keeps the cockpit as real procedural geometry and uses generated raster textures
only where images are appropriate: displays, carpet, ceiling panels, black
metal console surfaces, and wood cabinets.

v1.2 adds dedicated interaction/structure textures for the ship wheel,
telegraph lever, telegraph dial, non-slip bridge floor, ceiling panels, window
pillars, rails, and wipers. It also adds real geometry seams/strips for the
floor and ceiling so the room reads correctly in VR when texture mipmaps soften.

`13_Modern_Bridge_Depth_Relief` was removed from the active pipeline because it
looked richer in a still render but did not provide trustworthy VR geometry.

## Runtime Exports

- `exports/ModernBridgeCockpit_VR_v1.2.fbx`
- `exports/ModernBridgeCockpit_VR_v1.2.glb`

## Source

- `source/ModernBridgeCockpit_VR_v1.2.blend`
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
""",
        encoding="utf-8",
    )

    print(f"Saved {blend_path}")
    print(f"Exported {fbx_path}")
    print(f"Exported {glb_path}")
    print(f"Rendered {bpy.context.scene.render.filepath}")


if __name__ == "__main__":
    create_model(repo_root_from_args())
