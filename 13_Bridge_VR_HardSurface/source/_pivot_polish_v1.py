"""Phase 7+8+9 pivot polish:
- Apply ECDIS chart + Radar PPI UI textures to screen materials.
- Identify all screen-like materials and set up emission images.
- Tweak floor/wall/ceiling materials darker per AI reference.
- Improve sky shader for ocean horizon look.
- Render hero from existing helmsman POV camera (or create one).
- Save as bridge_v2.0_pivot.blend in 13_ folder + render to research/.
"""
import bpy
import os
import math


HANDOFF = r"E:\Sach\Sua\test\VR\model_lms\_shared\Bridge_Reference_Handoff_2026-05-10\02_screen_ui_static"
ECDIS_PNG = os.path.join(HANDOFF, "generic_training_ecdis_chart_v1.png")
RADAR_PNG = os.path.join(HANDOFF, "generic_training_radar_ppi_v1.png")


def load_image_for_emission(path):
    img = bpy.data.images.load(path, check_existing=True)
    img.colorspace_settings.name = "sRGB"
    return img


def setup_screen_material(mat, image, emission_strength=2.5):
    """Reset material to a Principled BSDF with image plugged into Emission."""
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial"); out.location = (600, 0)
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled"); bsdf.location = (200, 0)
    bsdf.inputs["Base Color"].default_value = (0.02, 0.02, 0.03, 1.0)
    bsdf.inputs["Metallic"].default_value = 0.0
    bsdf.inputs["Roughness"].default_value = 0.10
    tex = nt.nodes.new("ShaderNodeTexImage"); tex.location = (-200, 0)
    tex.image = image
    if "Emission Color" in bsdf.inputs:
        nt.links.new(tex.outputs["Color"], bsdf.inputs["Emission Color"])
    if "Emission Strength" in bsdf.inputs:
        bsdf.inputs["Emission Strength"].default_value = emission_strength
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])


def find_screen_materials():
    """Find materials that look like display screens, partition into ECDIS-like
    and radar-like groups by name."""
    ecdis = []
    radar = []
    other = []
    for m in bpy.data.materials:
        n = m.name.lower()
        if "ecdis" in n and "screen" in n:
            ecdis.append(m)
        elif "radar" in n and ("screen" in n or "ppi" in n):
            radar.append(m)
        elif "screen" in n or "display" in n or "monitor" in n:
            other.append(m)
    return ecdis, radar, other


def upgrade_floor(mat):
    """Darker matte floor approximating dark vinyl/rubber per AI ref."""
    mat.use_nodes = True
    nt = mat.node_tree; nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial"); out.location = (400, 0)
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled"); bsdf.location = (0, 0)
    bsdf.inputs["Base Color"].default_value = (0.025, 0.030, 0.045, 1.0)
    bsdf.inputs["Metallic"].default_value = 0.0
    bsdf.inputs["Roughness"].default_value = 0.85
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])


def upgrade_wall(mat, color=(0.65, 0.66, 0.66)):
    mat.use_nodes = True
    nt = mat.node_tree; nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial"); out.location = (400, 0)
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled"); bsdf.location = (0, 0)
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Metallic"].default_value = 0.0
    bsdf.inputs["Roughness"].default_value = 0.62
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])


def upgrade_ceiling(mat):
    upgrade_wall(mat, color=(0.86, 0.86, 0.84))


def upgrade_console(mat):
    """Dark gray painted console body."""
    mat.use_nodes = True
    nt = mat.node_tree; nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial"); out.location = (400, 0)
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled"); bsdf.location = (0, 0)
    bsdf.inputs["Base Color"].default_value = (0.07, 0.08, 0.09, 1.0)
    bsdf.inputs["Metallic"].default_value = 0.05
    bsdf.inputs["Roughness"].default_value = 0.45
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])


def setup_world_sky(scene):
    """Better sky for ocean horizon: low sun, dense atmosphere -> golden hour ocean look."""
    world = scene.world or bpy.data.worlds.new("World")
    scene.world = world
    world.use_nodes = True
    nt = world.node_tree; nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputWorld"); out.location = (400, 0)
    bg = nt.nodes.new("ShaderNodeBackground"); bg.location = (200, 0)
    bg.inputs["Strength"].default_value = 0.85
    sky = nt.nodes.new("ShaderNodeTexSky"); sky.location = (-100, 0)
    try:
        sky.sky_type = "MULTIPLE_SCATTERING"
    except Exception:
        try: sky.sky_type = "HOSEK_WILKIE"
        except Exception: pass
    for attr, val in (("sun_elevation", 0.35), ("sun_rotation", 1.20),
                      ("sun_intensity", 0.6), ("air_density", 1.0),
                      ("dust_density", 1.6), ("ozone_density", 1.0)):
        if hasattr(sky, attr):
            try: setattr(sky, attr, val)
            except Exception: pass
    nt.links.new(sky.outputs["Color"], bg.inputs["Color"])
    nt.links.new(bg.outputs["Background"], out.inputs["Surface"])


def find_helmsman_camera():
    """Pick a camera named like helmsman POV; otherwise create one."""
    candidates = [c for c in bpy.data.objects if c.type == "CAMERA" and (
        "helm" in c.name.lower() or "pov" in c.name.lower())]
    if candidates:
        return candidates[0]
    # Fallback: create one at typical helmsman pose
    cd = bpy.data.cameras.new("HeroCam_Helm")
    cd.lens = 22
    cam = bpy.data.objects.new("HeroCam_Helm", cd)
    bpy.context.scene.collection.objects.link(cam)
    cam.location = (0.0, -1.5, 1.7)
    cam.rotation_euler = (math.radians(82), 0, 0)
    return cam


def render_hero(scene, suffix):
    cam = find_helmsman_camera()
    scene.camera = cam
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = 1600
    scene.render.resolution_y = 900
    scene.render.image_settings.file_format = "PNG"
    if hasattr(scene, "eevee") and hasattr(scene.eevee, "taa_render_samples"):
        scene.eevee.taa_render_samples = 96
    if hasattr(scene, "eevee") and hasattr(scene.eevee, "use_raytracing"):
        scene.eevee.use_raytracing = True
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.look = "AgX - Medium High Contrast"
    out = (r"E:\Sach\Sua\test\VR\model_lms\13_Bridge_VR_HardSurface\research\hero_"
           + suffix + ".png")
    scene.render.filepath = out
    bpy.ops.render.render(write_still=True)
    return out


def main():
    scene = bpy.context.scene

    # 1. Apply screen UI textures
    ecdis_img = load_image_for_emission(ECDIS_PNG)
    radar_img = load_image_for_emission(RADAR_PNG)
    ecdis_mats, radar_mats, other_screens = find_screen_materials()

    applied = {"ecdis": [], "radar": [], "other_assigned": []}
    for m in ecdis_mats:
        setup_screen_material(m, ecdis_img, emission_strength=3.0)
        applied["ecdis"].append(m.name)
    for m in radar_mats:
        setup_screen_material(m, radar_img, emission_strength=3.0)
        applied["radar"].append(m.name)
    # Distribute other "screen" materials roughly between ECDIS and radar
    for i, m in enumerate(other_screens):
        if i % 2 == 0:
            setup_screen_material(m, ecdis_img, emission_strength=2.5)
            applied["other_assigned"].append(m.name + " -> ECDIS")
        else:
            setup_screen_material(m, radar_img, emission_strength=2.5)
            applied["other_assigned"].append(m.name + " -> RADAR")

    # 2. Material polish
    polished = []
    for m in bpy.data.materials:
        n = m.name.lower()
        if n == "mat_bridge_floor":
            upgrade_floor(m); polished.append(m.name)
        elif n == "mat_bridge_wall":
            upgrade_wall(m); polished.append(m.name)
        elif n == "mat_bridge_ceiling":
            upgrade_ceiling(m); polished.append(m.name)
        elif n in ("mat_bridge_console", "mat_console_top", "mat_ecdis_body",
                   "mat_ecdis_mount", "mat_eot_pedestal"):
            upgrade_console(m); polished.append(m.name)

    # 3. World sky
    setup_world_sky(scene)

    # 4. Save as bridge_v2.0_pivot.blend
    out_blend = r"E:\Sach\Sua\test\VR\model_lms\13_Bridge_VR_HardSurface\source\bridge_v2.0_pivot.blend"
    bpy.ops.wm.save_as_mainfile(filepath=out_blend)

    # 5. Render hero
    hero_path = render_hero(scene, "v2.0_pivot")

    return {
        "ecdis_materials_textured": applied["ecdis"],
        "radar_materials_textured": applied["radar"],
        "other_screen_materials_textured": applied["other_assigned"],
        "materials_polished": polished,
        "saved_blend": out_blend,
        "hero_render": hero_path,
        "hero_size_kb": os.path.getsize(hero_path) // 1024 if os.path.exists(hero_path) else None,
        "all_material_names_for_diagnosis": sorted([m.name for m in bpy.data.materials]),
    }


result = main()
