"""Phase 4: PBR materials + lighting + sky for VR maritime bridge.
Creates materials, assigns by object naming pattern, and sets up
a sun + sky world environment with interior fill lights.

Targets glTF / Unity URP compatibility (Principled BSDF, metallic-roughness).
"""
import bpy


def make_principled(name, base_color, metallic=0.0, roughness=0.5,
                    specular=0.5, ior=1.45, emission=None, emission_strength=0.0,
                    transmission=0.0, alpha=1.0):
    mat = bpy.data.materials.get(name)
    if mat is None:
        mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    out.location = (400, 0)
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.location = (0, 0)
    bsdf.inputs["Base Color"].default_value = (*base_color, 1.0)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    if "Specular IOR Level" in bsdf.inputs:
        bsdf.inputs["Specular IOR Level"].default_value = specular
    if "IOR" in bsdf.inputs:
        bsdf.inputs["IOR"].default_value = ior
    if "Transmission Weight" in bsdf.inputs:
        bsdf.inputs["Transmission Weight"].default_value = transmission
    if "Alpha" in bsdf.inputs:
        bsdf.inputs["Alpha"].default_value = alpha
    if emission is not None:
        if "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = (*emission, 1.0)
        if "Emission Strength" in bsdf.inputs:
            bsdf.inputs["Emission Strength"].default_value = emission_strength
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    if alpha < 1.0 or transmission > 0.0:
        mat.blend_method = "BLEND"
    return mat


def assign_mat(obj, mat):
    if obj.data is None or not hasattr(obj.data, "materials"):
        return
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)


def build_materials():
    return {
        "SteelPainted_Gray": make_principled(
            "BR_mat_SteelPainted_Gray",
            base_color=(0.42, 0.45, 0.48), metallic=0.12, roughness=0.55),
        "BrushedSteel": make_principled(
            "BR_mat_BrushedSteel",
            base_color=(0.74, 0.76, 0.78), metallic=0.95, roughness=0.32),
        "PlasticBlack": make_principled(
            "BR_mat_PlasticBlack",
            base_color=(0.04, 0.04, 0.05), metallic=0.0, roughness=0.45),
        "RubberRed": make_principled(
            "BR_mat_RubberRed",
            base_color=(0.42, 0.06, 0.06), metallic=0.0, roughness=0.78),
        "Glass": make_principled(
            "BR_mat_Glass_Window",
            base_color=(0.92, 0.96, 1.0), metallic=0.0, roughness=0.05,
            ior=1.52, transmission=0.95, alpha=0.15),
        "LED_Green": make_principled(
            "BR_mat_LED_Green",
            base_color=(0.05, 0.25, 0.10), metallic=0.0, roughness=0.4,
            emission=(0.10, 1.0, 0.30), emission_strength=10.0),
        "LED_Red": make_principled(
            "BR_mat_LED_Red",
            base_color=(0.30, 0.04, 0.04), metallic=0.0, roughness=0.4,
            emission=(1.0, 0.10, 0.05), emission_strength=10.0),
        "ScreenEmissive": make_principled(
            "BR_mat_ScreenEmissive",
            base_color=(0.02, 0.05, 0.10), metallic=0.0, roughness=0.10,
            emission=(0.10, 0.40, 0.95), emission_strength=4.0),
        "DeckCarpet": make_principled(
            "BR_mat_DeckCarpet",
            base_color=(0.04, 0.06, 0.16), metallic=0.0, roughness=0.92),
        "CeilingPanel": make_principled(
            "BR_mat_CeilingPanel",
            base_color=(0.85, 0.85, 0.82), metallic=0.0, roughness=0.65),
    }


def assign_materials(mats):
    for obj in bpy.data.objects:
        if obj.data is None or not hasattr(obj.data, "polygons"):
            continue
        n = obj.name
        # Structural
        if n == "WH_Deck":
            assign_mat(obj, mats["DeckCarpet"])
        elif n == "WH_Ceiling":
            assign_mat(obj, mats["CeilingPanel"])
        elif n in ("WH_AftBulkhead", "WH_SideWall_PORT", "WH_SideWall_STBD",
                   "WH_FrontBulkhead"):
            assign_mat(obj, mats["SteelPainted_Gray"])
        elif n == "WH_FrontWindow_Glass" or n == "REF_FrontWindow_Plane":
            assign_mat(obj, mats["Glass"])
        # Console parts
        elif "PanelBase" in n:
            assign_mat(obj, mats["SteelPainted_Gray"])
        elif "Bezel_" in n:
            assign_mat(obj, mats["BrushedSteel"])
        elif "_Sw_" in n or "ToggleSwitch" in n:
            assign_mat(obj, mats["PlasticBlack"])
        elif "_Btn_" in n or "PushButton" in n:
            assign_mat(obj, mats["RubberRed"])
        elif "_Knob_" in n or n.endswith("Kit_Knob_v1"):
            assign_mat(obj, mats["BrushedSteel"])
        elif "_LED_" in n or n.endswith("Kit_LED_v1"):
            assign_mat(obj, mats["LED_Green"])
        elif "GrabRail" in n:
            assign_mat(obj, mats["BrushedSteel"])
        # References (no material needed)


def setup_world_sky(scene):
    """Procedural sky background simulating ocean horizon."""
    world = scene.world or bpy.data.worlds.new("World")
    scene.world = world
    world.use_nodes = True
    nt = world.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputWorld")
    out.location = (400, 0)
    bg = nt.nodes.new("ShaderNodeBackground")
    bg.location = (200, 0)
    bg.inputs["Strength"].default_value = 1.0
    sky = nt.nodes.new("ShaderNodeTexSky")
    sky.location = (-100, 0)
    # Blender 5.x: try MULTIPLE_SCATTERING (Nishita renamed); fallback HOSEK_WILKIE
    try:
        sky.sky_type = "MULTIPLE_SCATTERING"
    except (TypeError, AttributeError):
        try:
            sky.sky_type = "HOSEK_WILKIE"
        except Exception:
            pass
    # Set sun elevation/rotation if available
    for attr, val in (("sun_elevation", 0.30), ("sun_rotation", 1.20),
                      ("sun_intensity", 1.0), ("air_density", 1.0),
                      ("dust_density", 1.5), ("ozone_density", 1.0)):
        if hasattr(sky, attr):
            try:
                setattr(sky, attr, val)
            except Exception:
                pass
    nt.links.new(sky.outputs["Color"], bg.inputs["Color"])
    nt.links.new(bg.outputs["Background"], out.inputs["Surface"])


def add_lights(scene):
    lighting_col = bpy.data.collections.get("BR_Lighting")
    if lighting_col is None:
        lighting_col = bpy.data.collections.new("BR_Lighting")
        scene.collection.children.link(lighting_col)

    # Sun (matches sky direction roughly)
    sun_data = bpy.data.lights.new("BR_Sun", type="SUN")
    sun_data.energy = 3.5
    sun_data.angle = 0.020
    sun_data.color = (1.0, 0.94, 0.85)
    sun = bpy.data.objects.new("BR_Sun", sun_data)
    sun.rotation_euler = (1.0, 0.3, -0.4)
    lighting_col.objects.link(sun)

    # 4 ceiling area lights (warm interior fill, mounted near ceiling)
    positions = [(-3, -1.5, 2.20), (3, -1.5, 2.20),
                 (-3, -4.5, 2.20), (3, -4.5, 2.20)]
    for i, p in enumerate(positions):
        ld = bpy.data.lights.new(f"BR_CeilingLight_{i}", type="AREA")
        ld.shape = "SQUARE"
        ld.size = 0.5
        ld.energy = 30.0
        ld.color = (1.0, 0.92, 0.82)
        lo = bpy.data.objects.new(f"BR_CeilingLight_{i}", ld)
        lo.location = p
        lo.rotation_euler = (3.14159, 0, 0)  # face down
        lighting_col.objects.link(lo)


def main():
    scene = bpy.context.scene
    mats = build_materials()
    assign_materials(mats)
    setup_world_sky(scene)
    add_lights(scene)

    # Blender 5.x: BLENDER_EEVEE is the new EEVEE Next; legacy was retired.
    scene.render.engine = "BLENDER_EEVEE"

    bpy.ops.wm.save_as_mainfile(
        filepath=r"E:\Sach\Sua\test\VR\model_lms\13_Bridge_VR_HardSurface\source\bridge_v0.3_materials.blend"
    )

    return {
        "materials_created": list(mats.keys()),
        "render_engine": scene.render.engine,
        "world_nodes": [n.bl_idname for n in scene.world.node_tree.nodes],
        "lighting_objects": [o.name for o in bpy.data.collections["BR_Lighting"].objects],
        "saved_as": "bridge_v0.3_materials.blend",
    }


result = main()
