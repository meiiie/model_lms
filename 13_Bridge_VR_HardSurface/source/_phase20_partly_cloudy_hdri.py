"""Phase 20 - Replace HDRI with kloofendal_38d_partly_cloudy_puresky.

This puresky variant has real cumulus clouds painted into the HDRI itself,
so we don't need any volumetric simulation. Much faster, much more
predictable, and the clouds match the sun direction automatically.

Plan:
  1. Open v6.0 (clean base, no clouds, has Ocean Modifier)
  2. Disable BR_CloudSlab_v2 / BR_CloudSlab if present (don't need them)
  3. Replace HDRI in world shader with new partly_cloudy_puresky HDRI
  4. Keep the lower-hemisphere mix so ocean stays dark below horizon
  5. Add BR_SunSphere as well (sun visible in window matches HDRI sun)
  6. Boost BR_Sun energy a bit (cloud rim lighting via direct sun)
  7. Render 4 keyframes + full 240-frame MP4
"""
import bpy
import bmesh
import math
import os


BLEND_IN = r"E:\Sach\Sua\test\VR\model_lms\13_Bridge_VR_HardSurface\source\bridge_v6.0_real_waves.blend"
BLEND_OUT = r"E:\Sach\Sua\test\VR\model_lms\13_Bridge_VR_HardSurface\source\bridge_v8.0_partly_cloudy.blend"
HDRI_NEW = r"E:\Sach\Sua\test\VR\model_lms\_shared\HDRIs\kloofendal_38d_partly_cloudy_puresky_2k.hdr"
OUT_DIR = r"E:\Sach\Sua\test\VR\model_lms\13_Bridge_VR_HardSurface\research"
SEQ_DIR = os.path.join(OUT_DIR, "anim_v8.0_frames")


def swap_hdri_in_world(scene):
    world = scene.world
    nt = world.node_tree
    # Find existing Environment Texture node
    env = None
    for n in nt.nodes:
        if n.type == "TEX_ENVIRONMENT":
            env = n
            break
    if env is None:
        # Build fresh world shader (use mix-hemisphere approach from v6)
        nt.nodes.clear()
        out = nt.nodes.new("ShaderNodeOutputWorld"); out.location = (1000, 0)
        bg_mix = nt.nodes.new("ShaderNodeMixShader"); bg_mix.location = (700, 0)

        bg_sky = nt.nodes.new("ShaderNodeBackground"); bg_sky.location = (400, 200)
        bg_sky.inputs["Strength"].default_value = 1.0
        env = nt.nodes.new("ShaderNodeTexEnvironment"); env.location = (100, 200)
        mapping = nt.nodes.new("ShaderNodeMapping"); mapping.location = (-150, 200)
        mapping.inputs["Rotation"].default_value[2] = 0.8
        tc = nt.nodes.new("ShaderNodeTexCoord"); tc.location = (-400, 200)

        bg_ocean = nt.nodes.new("ShaderNodeBackground"); bg_ocean.location = (400, -200)
        bg_ocean.inputs["Color"].default_value = (0.012, 0.025, 0.045, 1.0)
        bg_ocean.inputs["Strength"].default_value = 0.40

        geom = nt.nodes.new("ShaderNodeNewGeometry"); geom.location = (100, 0)
        sep = nt.nodes.new("ShaderNodeSeparateXYZ"); sep.location = (300, 0)
        mr = nt.nodes.new("ShaderNodeMapRange"); mr.location = (500, 0)
        mr.inputs["From Min"].default_value = -0.05
        mr.inputs["From Max"].default_value = 0.05
        mr.inputs["To Min"].default_value = 1.0
        mr.inputs["To Max"].default_value = 0.0
        mr.clamp = True

        nt.links.new(tc.outputs["Generated"], mapping.inputs["Vector"])
        nt.links.new(mapping.outputs["Vector"], env.inputs["Vector"])
        nt.links.new(env.outputs["Color"], bg_sky.inputs["Color"])
        nt.links.new(geom.outputs["Incoming"], sep.inputs["Vector"])
        nt.links.new(sep.outputs["Z"], mr.inputs["Value"])
        nt.links.new(mr.outputs["Result"], bg_mix.inputs["Fac"])
        nt.links.new(bg_sky.outputs["Background"], bg_mix.inputs[1])
        nt.links.new(bg_ocean.outputs["Background"], bg_mix.inputs[2])
        nt.links.new(bg_mix.outputs["Shader"], out.inputs["Surface"])

    # Load and assign new HDRI
    env.image = bpy.data.images.load(HDRI_NEW, check_existing=True)
    print(f"[world] HDRI -> {HDRI_NEW}", flush=True)


def remove_cloud_volumetrics(scene):
    """Remove any volumetric cloud slabs from prior phases."""
    for name in ("BR_CloudSlab", "BR_CloudSlab_v2"):
        old = bpy.data.objects.get(name)
        if old:
            bpy.data.objects.remove(old, do_unlink=True)
            print(f"[clean] removed {name}", flush=True)


def add_sun_sphere(scene):
    old = bpy.data.objects.get("BR_SunSphere")
    if old:
        bpy.data.objects.remove(old, do_unlink=True)
    me = bpy.data.meshes.new("BR_SunSphere_mesh")
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=24, v_segments=16, radius=8.0)
    bm.to_mesh(me); bm.free()
    obj = bpy.data.objects.new("BR_SunSphere", me)
    obj.location = (-80.0, -480.0, 65.0)
    coll = bpy.data.collections.get("BR_Lighting") or scene.collection
    coll.objects.link(obj)
    mat = bpy.data.materials.get("BR_mat_SunSphere") or bpy.data.materials.new("BR_mat_SunSphere")
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial"); out.location = (300, 0)
    emi = nt.nodes.new("ShaderNodeEmission"); emi.location = (0, 0)
    emi.inputs["Color"].default_value = (1.0, 0.92, 0.78, 1.0)
    emi.inputs["Strength"].default_value = 25.0
    nt.links.new(emi.outputs["Emission"], out.inputs["Surface"])
    obj.data.materials.clear()
    obj.data.materials.append(mat)
    if hasattr(obj, "visible_shadow"):
        obj.visible_shadow = False
    return obj


def boost_sun(scene):
    sun = bpy.data.objects.get("BR_Sun")
    if sun and sun.type == "LIGHT" and sun.data.type == "SUN":
        sun.data.energy = 3.0
        sun.data.color = (1.0, 0.94, 0.82)
        sun.rotation_euler = (math.radians(78), 0, math.radians(85))


def main():
    bpy.ops.wm.open_mainfile(filepath=BLEND_IN)
    scene = bpy.context.scene

    remove_cloud_volumetrics(scene)
    swap_hdri_in_world(scene)
    add_sun_sphere(scene)
    boost_sun(scene)

    # No volumetrics needed now -> disable for speed
    ev = scene.eevee
    if hasattr(ev, "use_volumetric_lights"):
        ev.use_volumetric_lights = False
    if hasattr(ev, "use_volumetric_shadows"):
        ev.use_volumetric_shadows = False

    scene.render.engine = "BLENDER_EEVEE"
    if hasattr(ev, "taa_render_samples"):
        ev.taa_render_samples = 32
    if hasattr(ev, "use_raytracing"):
        ev.use_raytracing = True
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.look = "AgX - Medium High Contrast"
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 720
    scene.render.image_settings.file_format = "PNG"

    cam = bpy.data.objects.get("HeroCam_Anim")
    if cam:
        scene.camera = cam

    # 4 keyframes first
    for fn in (1, 80, 160, 240):
        scene.frame_set(fn)
        out_p = os.path.join(OUT_DIR, f"anim_v8.0_keyframe_f{fn:03d}.png")
        scene.render.filepath = out_p
        bpy.ops.render.render(write_still=True)
        print(f"[render] keyframe f{fn}", flush=True)

    bpy.ops.wm.save_as_mainfile(filepath=BLEND_OUT)
    print(f"[save] {BLEND_OUT}", flush=True)

    # Full animation (no volumetrics so much faster)
    os.makedirs(SEQ_DIR, exist_ok=True)
    scene.render.filepath = os.path.join(SEQ_DIR, "f")
    scene.frame_start = 1
    scene.frame_end = 240
    print("[render] starting full animation", flush=True)
    bpy.ops.render.render(animation=True)
    print("ALL_DONE", flush=True)


if __name__ == "__main__":
    main()
