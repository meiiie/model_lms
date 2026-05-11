"""Phase 22 - Pro cloud setup.

Approach used by VFX/film studios when a scene has narrow window views
where HDRI clouds wouldn't show:

  A) Use a real-photo OCEAN HDRI (aristea_wreck) for natural sky+horizon
     instead of puresky which is sky-only
  B) Add 5 CLOUD BILLBOARD planes positioned 60-150 m forward, scattered
     laterally, with procedural alpha cumulus shapes
  C) Billboards drift slowly sideways over 8 sec for parallax
  D) Slight rotation animation gives more life
"""
import bpy
import bmesh
import math
import os
import random


BLEND_IN = r"E:\Sach\Sua\test\VR\model_lms\13_Bridge_VR_HardSurface\source\bridge_v6.0_real_waves.blend"
BLEND_OUT = r"E:\Sach\Sua\test\VR\model_lms\13_Bridge_VR_HardSurface\source\bridge_v9.0_pro_clouds.blend"
HDRI_NEW = r"E:\Sach\Sua\test\VR\model_lms\_shared\HDRIs\aristea_wreck_2k.hdr"
OUT_DIR = r"E:\Sach\Sua\test\VR\model_lms\13_Bridge_VR_HardSurface\research"
SEQ_DIR = os.path.join(OUT_DIR, "anim_v9.0_frames")


def swap_world_hdri(scene):
    """Use aristea wreck HDRI - real photo with ocean horizon visible."""
    world = scene.world
    world.use_nodes = True
    nt = world.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputWorld"); out.location = (600, 0)
    bg = nt.nodes.new("ShaderNodeBackground"); bg.location = (400, 0)
    bg.inputs["Strength"].default_value = 1.2
    env = nt.nodes.new("ShaderNodeTexEnvironment"); env.location = (100, 0)
    env.image = bpy.data.images.load(HDRI_NEW, check_existing=True)
    mapping = nt.nodes.new("ShaderNodeMapping"); mapping.location = (-150, 0)
    mapping.inputs["Rotation"].default_value[2] = 0.0
    tc = nt.nodes.new("ShaderNodeTexCoord"); tc.location = (-400, 0)
    nt.links.new(tc.outputs["Generated"], mapping.inputs["Vector"])
    nt.links.new(mapping.outputs["Vector"], env.inputs["Vector"])
    nt.links.new(env.outputs["Color"], bg.inputs["Color"])
    nt.links.new(bg.outputs["Background"], out.inputs["Surface"])
    print(f"[world] HDRI -> {os.path.basename(HDRI_NEW)}", flush=True)
    return mapping


def build_cloud_billboard_material():
    """Procedural cumulus cloud with alpha. White diffuse + emission + noise alpha."""
    name = "BR_mat_CloudBillboard"
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.use_nodes = True
    mat.blend_method = "BLEND"
    if hasattr(mat, "shadow_method"):
        mat.shadow_method = "NONE"
    nt = mat.node_tree
    nt.nodes.clear()

    out = nt.nodes.new("ShaderNodeOutputMaterial"); out.location = (900, 0)
    mix_shader = nt.nodes.new("ShaderNodeMixShader"); mix_shader.location = (700, 0)
    transp = nt.nodes.new("ShaderNodeBsdfTransparent"); transp.location = (500, 100)
    diffuse = nt.nodes.new("ShaderNodeBsdfDiffuse"); diffuse.location = (500, -100)
    diffuse.inputs["Color"].default_value = (1.0, 0.98, 0.95, 1.0)

    # Alpha shape: Voronoi for cumulus blobs, multiplied by radial gradient
    # for soft edges, then thresholded
    tc = nt.nodes.new("ShaderNodeTexCoord"); tc.location = (-600, 0)
    # Use generated coords centered around (0.5, 0.5) for the plane
    mapping = nt.nodes.new("ShaderNodeMapping"); mapping.location = (-400, 0)
    mapping.inputs["Location"].default_value = (-0.5, -0.5, 0.0)

    # Voronoi mask
    voronoi = nt.nodes.new("ShaderNodeTexVoronoi"); voronoi.location = (-150, 200)
    voronoi.feature = "F1"
    voronoi.inputs["Scale"].default_value = 4.0

    # Noise detail
    noise = nt.nodes.new("ShaderNodeTexNoise"); noise.location = (-150, -100)
    noise.inputs["Scale"].default_value = 10.0
    noise.inputs["Detail"].default_value = 8.0
    noise.inputs["Roughness"].default_value = 0.65

    # Multiply voronoi x noise
    mul = nt.nodes.new("ShaderNodeMath"); mul.location = (100, 0)
    mul.operation = "MULTIPLY"

    # Map range to harden
    mr = nt.nodes.new("ShaderNodeMapRange"); mr.location = (300, 0)
    mr.inputs["From Min"].default_value = 0.20
    mr.inputs["From Max"].default_value = 0.50
    mr.inputs["To Min"].default_value = 0.0
    mr.inputs["To Max"].default_value = 1.0
    mr.clamp = True

    # Radial falloff: distance from center, invert -> fade at edges
    sep = nt.nodes.new("ShaderNodeSeparateXYZ"); sep.location = (-150, -350)
    sq_x = nt.nodes.new("ShaderNodeMath"); sq_x.location = (50, -300)
    sq_x.operation = "POWER"; sq_x.inputs[1].default_value = 2.0
    sq_y = nt.nodes.new("ShaderNodeMath"); sq_y.location = (50, -400)
    sq_y.operation = "POWER"; sq_y.inputs[1].default_value = 2.0
    add_sq = nt.nodes.new("ShaderNodeMath"); add_sq.location = (250, -350)
    add_sq.operation = "ADD"
    sqrt = nt.nodes.new("ShaderNodeMath"); sqrt.location = (400, -350)
    sqrt.operation = "SQRT"
    mr_radial = nt.nodes.new("ShaderNodeMapRange"); mr_radial.location = (550, -350)
    mr_radial.inputs["From Min"].default_value = 0.20
    mr_radial.inputs["From Max"].default_value = 0.50
    mr_radial.inputs["To Min"].default_value = 1.0
    mr_radial.inputs["To Max"].default_value = 0.0
    mr_radial.clamp = True

    # Final alpha = cumulus_shape * radial_falloff
    alpha = nt.nodes.new("ShaderNodeMath"); alpha.location = (700, -200)
    alpha.operation = "MULTIPLY"

    # Links
    nt.links.new(tc.outputs["Generated"], mapping.inputs["Vector"])
    nt.links.new(mapping.outputs["Vector"], voronoi.inputs["Vector"])
    nt.links.new(mapping.outputs["Vector"], noise.inputs["Vector"])
    nt.links.new(mapping.outputs["Vector"], sep.inputs["Vector"])
    nt.links.new(voronoi.outputs["Distance"], mul.inputs[0])
    nt.links.new(noise.outputs["Fac"], mul.inputs[1])
    nt.links.new(mul.outputs["Value"], mr.inputs["Value"])

    nt.links.new(sep.outputs["X"], sq_x.inputs[0])
    nt.links.new(sep.outputs["Y"], sq_y.inputs[0])
    nt.links.new(sq_x.outputs["Value"], add_sq.inputs[0])
    nt.links.new(sq_y.outputs["Value"], add_sq.inputs[1])
    nt.links.new(add_sq.outputs["Value"], sqrt.inputs[0])
    nt.links.new(sqrt.outputs["Value"], mr_radial.inputs["Value"])

    nt.links.new(mr.outputs["Result"], alpha.inputs[0])
    nt.links.new(mr_radial.outputs["Result"], alpha.inputs[1])

    nt.links.new(alpha.outputs["Value"], mix_shader.inputs["Fac"])
    nt.links.new(transp.outputs["BSDF"], mix_shader.inputs[1])
    nt.links.new(diffuse.outputs["BSDF"], mix_shader.inputs[2])
    nt.links.new(mix_shader.outputs["Shader"], out.inputs["Surface"])
    return mat


def add_cloud_billboards(scene, mat):
    """Add 5 cloud billboard planes in front of windows."""
    # Bridge front bulkhead at y=-2.5. Place clouds forward (-Y direction)
    # at varying distances 60..200 m, scattered laterally x=-80..+80
    cloud_col = bpy.data.collections.get("BR_Sky_Clouds")
    if cloud_col is None:
        cloud_col = bpy.data.collections.new("BR_Sky_Clouds")
        scene.collection.children.link(cloud_col)

    # Remove any prior billboards
    for o in list(cloud_col.objects):
        bpy.data.objects.remove(o, do_unlink=True)

    random.seed(42)
    billboards = []
    cloud_specs = [
        # (cx, cy, cz, w, h)
        (-50.0, -120.0, 25.0, 80.0, 35.0),
        ( 30.0,  -90.0, 22.0, 70.0, 30.0),
        ( -5.0, -180.0, 30.0, 120.0, 45.0),
        ( 70.0, -150.0, 28.0, 90.0, 38.0),
        (-80.0, -200.0, 32.0, 100.0, 42.0),
    ]
    for i, (cx, cy, cz, w, h) in enumerate(cloud_specs):
        me = bpy.data.meshes.new(f"BR_CloudBB_{i}_mesh")
        bm = bmesh.new()
        bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=0.5)
        for v in bm.verts:
            v.co.x *= w
            v.co.y *= h
        bm.to_mesh(me); bm.free()
        obj = bpy.data.objects.new(f"BR_CloudBB_{i}", me)
        obj.location = (cx, cy, cz)
        # Stand the plane vertically facing the bridge (rotate 90 deg X)
        # so plane normal points back along +Y
        obj.rotation_euler = (math.radians(90), 0, 0)
        cloud_col.objects.link(obj)
        obj.data.materials.clear()
        obj.data.materials.append(mat)
        # Disable shadow casting (Blender 5.x: visible_shadow toggle)
        if hasattr(obj, "visible_shadow"):
            obj.visible_shadow = False
        billboards.append(obj)
    return billboards


def animate_billboards(billboards):
    """Drift each billboard slightly sideways over 240 frames."""
    for i, obj in enumerate(billboards):
        base_loc = obj.location.copy()
        obj.location = base_loc
        obj.keyframe_insert("location", frame=1)
        # Drift X by some amount, Z by tiny
        dx = 8.0 + i * 1.5
        obj.location = (base_loc.x + dx, base_loc.y, base_loc.z + 1.0)
        obj.keyframe_insert("location", frame=240)


def boost_sun_for_clouds(scene):
    sun = bpy.data.objects.get("BR_Sun")
    if sun and sun.type == "LIGHT" and sun.data.type == "SUN":
        sun.data.energy = 4.0
        sun.data.color = (1.0, 0.95, 0.85)
        sun.rotation_euler = (math.radians(75), 0, math.radians(80))


def remove_old_sky_objects():
    """Remove cloud slabs and sun spheres from prior phases."""
    for name in ("BR_CloudSlab", "BR_CloudSlab_v2", "BR_SunSphere"):
        old = bpy.data.objects.get(name)
        if old:
            bpy.data.objects.remove(old, do_unlink=True)
            print(f"[clean] removed {name}", flush=True)


def main():
    bpy.ops.wm.open_mainfile(filepath=BLEND_IN)
    scene = bpy.context.scene
    remove_old_sky_objects()
    swap_world_hdri(scene)
    mat = build_cloud_billboard_material()
    billboards = add_cloud_billboards(scene, mat)
    animate_billboards(billboards)
    print(f"[clouds] {len(billboards)} billboards added + animated", flush=True)
    boost_sun_for_clouds(scene)

    ev = scene.eevee
    if hasattr(ev, "use_volumetric_lights"):
        ev.use_volumetric_lights = False
    if hasattr(ev, "taa_render_samples"):
        ev.taa_render_samples = 32
    if hasattr(ev, "use_raytracing"):
        ev.use_raytracing = True

    scene.render.engine = "BLENDER_EEVEE"
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.look = "AgX - Medium High Contrast"
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 720
    scene.render.image_settings.file_format = "PNG"

    cam = bpy.data.objects.get("HeroCam_Anim")
    if cam:
        scene.camera = cam

    for fn in (1, 80, 160, 240):
        scene.frame_set(fn)
        out_p = os.path.join(OUT_DIR, f"anim_v9.0_keyframe_f{fn:03d}.png")
        scene.render.filepath = out_p
        bpy.ops.render.render(write_still=True)
        print(f"[render] keyframe f{fn}", flush=True)

    bpy.ops.wm.save_as_mainfile(filepath=BLEND_OUT)
    print(f"[save] {BLEND_OUT}", flush=True)

    os.makedirs(SEQ_DIR, exist_ok=True)
    scene.render.filepath = os.path.join(SEQ_DIR, "f")
    scene.frame_start = 1
    scene.frame_end = 240
    print("[render] starting full animation", flush=True)
    bpy.ops.render.render(animation=True)
    print("ALL_DONE", flush=True)


if __name__ == "__main__":
    main()
