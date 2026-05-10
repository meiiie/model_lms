"""Phase 16 - Real waves via Blender Ocean Modifier + dark-hemisphere world.

Two upgrades over Phase 15:

1. WORLD SHADER: mix puresky HDRI (upper hemisphere) with deep navy blue
   (lower hemisphere) using Light Path's "Is Camera Ray" + a Geometry-based
   selector. So when the camera ray points DOWN below horizon, we see
   ocean color instead of bright sky-ground.

2. OCEAN PLANE: replace flat plane with a plane carrying Blender's
   built-in Ocean modifier (geometry_mode=GENERATE) for actual wave
   geometry + optional foam. Place at z=-3.5 m so visible above console
   top (z=1.05) through windows from camera eye z=1.65-1.85.

Then re-render 4 keyframe PNGs + 240-frame MP4.
"""
import bpy
import os
import math


BLEND_IN = r"E:\Sach\Sua\test\VR\model_lms\13_Bridge_VR_HardSurface\source\bridge_v5.0_animated.blend"
BLEND_OUT = r"E:\Sach\Sua\test\VR\model_lms\13_Bridge_VR_HardSurface\source\bridge_v6.0_real_waves.blend"
HDRI = r"E:\Sach\Sua\test\VR\model_lms\_shared\HDRIs\kloppenheim_06_puresky_2k.hdr"
OUT_DIR = r"E:\Sach\Sua\test\VR\model_lms\13_Bridge_VR_HardSurface\research"
SEQ_DIR = os.path.join(OUT_DIR, "anim_v6.0_frames")


def build_world_with_ocean_floor(scene):
    """World shader: HDRI for upward rays, deep blue for downward rays."""
    world = scene.world or bpy.data.worlds.new("World")
    scene.world = world
    world.use_nodes = True
    nt = world.node_tree
    nt.nodes.clear()

    out = nt.nodes.new("ShaderNodeOutputWorld"); out.location = (1000, 0)
    bg_mix = nt.nodes.new("ShaderNodeMixShader"); bg_mix.location = (700, 0)

    # Upper hemisphere: HDRI
    bg_sky = nt.nodes.new("ShaderNodeBackground"); bg_sky.location = (400, 200)
    bg_sky.inputs["Strength"].default_value = 1.1
    env = nt.nodes.new("ShaderNodeTexEnvironment"); env.location = (100, 200)
    env.image = bpy.data.images.load(HDRI, check_existing=True)
    mapping = nt.nodes.new("ShaderNodeMapping"); mapping.location = (-150, 200)
    mapping.inputs["Rotation"].default_value[2] = 1.5
    tc = nt.nodes.new("ShaderNodeTexCoord"); tc.location = (-400, 200)

    # Lower hemisphere: deep ocean blue
    bg_ocean = nt.nodes.new("ShaderNodeBackground"); bg_ocean.location = (400, -200)
    bg_ocean.inputs["Color"].default_value = (0.012, 0.025, 0.045, 1.0)
    bg_ocean.inputs["Strength"].default_value = 0.45

    # Selector: incoming ray Z component. Above horizon -> HDRI, below -> ocean
    geom = nt.nodes.new("ShaderNodeNewGeometry"); geom.location = (100, 0)
    sep = nt.nodes.new("ShaderNodeSeparateXYZ"); sep.location = (300, 0)
    map_range = nt.nodes.new("ShaderNodeMapRange"); map_range.location = (500, 0)
    # Map incoming Z from [-0.05, +0.05] to [1, 0] so ray pointing slightly
    # below horizon already starts blending into ocean and rays slightly
    # above are full HDRI.
    map_range.inputs["From Min"].default_value = -0.05
    map_range.inputs["From Max"].default_value = 0.05
    map_range.inputs["To Min"].default_value = 1.0  # below horizon = ocean
    map_range.inputs["To Max"].default_value = 0.0  # above horizon = HDRI
    map_range.clamp = True

    nt.links.new(tc.outputs["Generated"], mapping.inputs["Vector"])
    nt.links.new(mapping.outputs["Vector"], env.inputs["Vector"])
    nt.links.new(env.outputs["Color"], bg_sky.inputs["Color"])
    nt.links.new(geom.outputs["Incoming"], sep.inputs["Vector"])
    nt.links.new(sep.outputs["Z"], map_range.inputs["Value"])
    nt.links.new(map_range.outputs["Result"], bg_mix.inputs["Fac"])
    nt.links.new(bg_sky.outputs["Background"], bg_mix.inputs[1])    # ABOVE
    nt.links.new(bg_ocean.outputs["Background"], bg_mix.inputs[2])  # BELOW
    nt.links.new(bg_mix.outputs["Shader"], out.inputs["Surface"])


def build_ocean_material():
    name = "BR_mat_Ocean_v3_Modifier"
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial"); out.location = (600, 0)
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled"); bsdf.location = (200, 0)
    bsdf.inputs["Base Color"].default_value = (0.012, 0.030, 0.060, 1.0)
    bsdf.inputs["Metallic"].default_value = 0.0
    bsdf.inputs["Roughness"].default_value = 0.06   # very smooth = sky reflection
    if "IOR" in bsdf.inputs:
        bsdf.inputs["IOR"].default_value = 1.33
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return mat


def add_ocean_modifier_plane(scene):
    # Remove any prior ocean plane
    for old_name in ("BR_OceanPlane", "BR_Ocean_v3", "BR_Ocean_Modifier"):
        old = bpy.data.objects.get(old_name)
        if old:
            bpy.data.objects.remove(old, do_unlink=True)

    # Create a new plane via low-level (avoid bpy.ops dependency on context)
    import bmesh
    me = bpy.data.meshes.new("BR_Ocean_Modifier_mesh")
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=0.5)
    bm.to_mesh(me); bm.free()
    obj = bpy.data.objects.new("BR_Ocean_Modifier", me)
    obj.location = (0.0, -100.0, -3.5)
    obj.scale = (1000.0, 1000.0, 1.0)

    # Place into Phase11_Additions collection if exists, else scene root
    coll = bpy.data.collections.get("Phase11_Additions") or scene.collection
    coll.objects.link(obj)

    # Add Ocean modifier
    mod = obj.modifiers.new(name="Ocean", type="OCEAN")
    mod.geometry_mode = "GENERATE"
    mod.resolution = 16              # 16 -> 256x256 grid (decent)
    mod.spatial_size = 100           # meters per tile
    mod.choppiness = 1.5
    mod.wave_scale = 2.5
    mod.wave_scale_min = 0.5
    mod.wave_alignment = 0.4
    mod.wind_velocity = 8.0
    mod.depth = 200.0
    mod.random_seed = 7
    if hasattr(mod, "use_foam"):
        mod.use_foam = True
        mod.foam_coverage = 0.55
        if hasattr(mod, "foam_layer_name"):
            mod.foam_layer_name = "foam"
    # Frame range for animation matches scene (so waves animate too)
    if hasattr(mod, "time"):
        # The 'time' property advances waves per frame; set a frame_start/end
        mod.frame_start = 1
        mod.frame_end = 240

    # Material
    mat = build_ocean_material()
    obj.data.materials.clear()
    obj.data.materials.append(mat)

    obj.hide_render = False
    obj.hide_viewport = False
    return obj


def main():
    bpy.ops.wm.open_mainfile(filepath=BLEND_IN)
    scene = bpy.context.scene

    build_world_with_ocean_floor(scene)
    ocean = add_ocean_modifier_plane(scene)
    print(f"[ocean] {ocean.name} loc={tuple(ocean.location)} scale={tuple(ocean.scale)}",
          flush=True)
    print(f"[ocean] Modifier: {ocean.modifiers[0].name}", flush=True)

    # EEVEE for speed (Cycles would be better quality but much slower)
    scene.render.engine = "BLENDER_EEVEE"
    if hasattr(scene.eevee, "taa_render_samples"):
        scene.eevee.taa_render_samples = 32
    if hasattr(scene.eevee, "use_raytracing"):
        scene.eevee.use_raytracing = True
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.look = "AgX - Medium High Contrast"
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 720
    scene.render.image_settings.file_format = "PNG"

    # Use HeroCam_Anim from v5.0
    cam = bpy.data.objects.get("HeroCam_Anim")
    if cam:
        scene.camera = cam

    # Render 4 keyframes first for fast feedback
    for fn in (1, 80, 160, 240):
        scene.frame_set(fn)
        out_p = os.path.join(OUT_DIR, f"anim_v6.0_keyframe_f{fn:03d}.png")
        scene.render.filepath = out_p
        bpy.ops.render.render(write_still=True)
        print(f"[render] keyframe f{fn} -> {out_p}", flush=True)

    bpy.ops.wm.save_as_mainfile(filepath=BLEND_OUT)
    print(f"[save] {BLEND_OUT}", flush=True)

    # Render full 240-frame animation as PNG sequence
    os.makedirs(SEQ_DIR, exist_ok=True)
    scene.render.filepath = os.path.join(SEQ_DIR, "f")
    scene.frame_start = 1
    scene.frame_end = 240
    print(f"[render] starting full animation -> {SEQ_DIR}", flush=True)
    bpy.ops.render.render(animation=True)
    print("ALL_DONE", flush=True)


if __name__ == "__main__":
    main()
