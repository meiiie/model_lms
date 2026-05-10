"""Headless Cycles render: HDRI + GPU OptiX/CUDA/CPU + multiple angles.
Renders 3 hero angles for the final comparison sheet.
"""
import bpy
import os
import sys
import math
import mathutils


HDRI = r"E:\Sach\Sua\test\VR\model_lms\_shared\HDRIs\kloppenheim_06_puresky_2k.hdr"
BLEND_IN = r"E:\Sach\Sua\test\VR\model_lms\13_Bridge_VR_HardSurface\source\bridge_v2.0_pivot.blend"
OUT_DIR = r"E:\Sach\Sua\test\VR\model_lms\13_Bridge_VR_HardSurface\research"


def setup_hdri(scene):
    world = scene.world
    world.use_nodes = True
    nt = world.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputWorld"); out.location = (600, 0)
    bg = nt.nodes.new("ShaderNodeBackground"); bg.location = (400, 0)
    bg.inputs["Strength"].default_value = 1.2
    env = nt.nodes.new("ShaderNodeTexEnvironment"); env.location = (100, 0)
    env.image = bpy.data.images.load(HDRI, check_existing=True)
    mapping = nt.nodes.new("ShaderNodeMapping"); mapping.location = (-150, 0)
    mapping.inputs["Rotation"].default_value[2] = 1.5
    tc = nt.nodes.new("ShaderNodeTexCoord"); tc.location = (-400, 0)
    nt.links.new(tc.outputs["Generated"], mapping.inputs["Vector"])
    nt.links.new(mapping.outputs["Vector"], env.inputs["Vector"])
    nt.links.new(env.outputs["Color"], bg.inputs["Color"])
    nt.links.new(bg.outputs["Background"], out.inputs["Surface"])


def setup_cycles_gpu(scene):
    used_gpu = False
    prefs = bpy.context.preferences.addons.get("cycles")
    if prefs:
        cyprefs = prefs.preferences
        for backend in ("OPTIX", "CUDA", "HIP", "ONEAPI"):
            try:
                cyprefs.compute_device_type = backend
                try: cyprefs.refresh_devices()
                except Exception: pass
                gpu_devs = [d for d in cyprefs.devices if d.type == backend]
                if gpu_devs:
                    for d in cyprefs.devices:
                        d.use = True
                    used_gpu = True
                    break
            except (TypeError, AttributeError):
                continue
    scene.render.engine = "CYCLES"
    scene.cycles.device = "GPU" if used_gpu else "CPU"
    scene.cycles.samples = 64 if used_gpu else 32
    scene.cycles.use_denoising = True
    if hasattr(scene.cycles, "denoiser"):
        try: scene.cycles.denoiser = "OPTIX" if used_gpu else "OPENIMAGEDENOISE"
        except Exception:
            try: scene.cycles.denoiser = "OPENIMAGEDENOISE"
            except Exception: pass
    if hasattr(scene.cycles, "use_adaptive_sampling"):
        scene.cycles.use_adaptive_sampling = True
    print(f"[setup] used_gpu={used_gpu} engine={scene.render.engine} device={scene.cycles.device} samples={scene.cycles.samples}", flush=True)
    return used_gpu


def look_at(cam_obj, target):
    direction = mathutils.Vector(target) - cam_obj.location
    cam_obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def make_cam(name, lens, location, target):
    cd = bpy.data.cameras.new(name)
    cd.lens = lens
    cam = bpy.data.objects.new(name, cd)
    bpy.context.scene.collection.objects.link(cam)
    cam.location = location
    look_at(cam, target)
    return cam


def render(scene, cam, out_path):
    scene.camera = cam
    scene.render.filepath = out_path
    bpy.ops.render.render(write_still=True)
    print(f"[render] -> {out_path}", flush=True)


def main():
    bpy.ops.wm.open_mainfile(filepath=BLEND_IN)
    scene = bpy.context.scene
    setup_hdri(scene)
    used_gpu = setup_cycles_gpu(scene)

    # Reduce competing lights
    for n in ("BR_Sun", "BR_CeilingLight_0", "BR_CeilingLight_1",
              "BR_CeilingLight_2", "BR_CeilingLight_3"):
        o = bpy.data.objects.get(n)
        if o and o.type == "LIGHT":
            o.data.energy = 0.5 if o.data.type == "SUN" else 6.0

    scene.render.resolution_x = 1280
    scene.render.resolution_y = 720
    scene.render.image_settings.file_format = "PNG"
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.look = "AgX - Medium High Contrast"

    # Camera A: Helmsman wide (existing or new)
    camA = bpy.data.objects.get("HeroCam_v2_HelmWide")
    if camA is None:
        camA = make_cam("HeroCam_HelmWide_v3", 14, (0.0, 0.5, 1.65), (0.0, -2.0, 1.30))
    render(scene, camA, os.path.join(OUT_DIR, "hero_v3.1_cycles_helmsman.png"))

    # Camera B: 3/4 overview from upper aft starboard
    camB = make_cam("HeroCam_Overview_v3", 24, (3.0, 2.5, 2.0), (0.0, -1.5, 1.0))
    render(scene, camB, os.path.join(OUT_DIR, "hero_v3.1_cycles_overview.png"))

    # Camera C: Approaching front console (between wheel and ECDIS)
    camC = make_cam("HeroCam_FrontApproach_v3", 18, (0.0, -0.7, 1.55), (0.0, -2.5, 1.0))
    render(scene, camC, os.path.join(OUT_DIR, "hero_v3.1_cycles_front_approach.png"))

    # Save with HDRI applied
    bpy.ops.wm.save_as_mainfile(
        filepath=r"E:\Sach\Sua\test\VR\model_lms\13_Bridge_VR_HardSurface\source\bridge_v3.0_hdri_cycles.blend"
    )

    # Export FBX + GLB now in headless (avoiding MCP timeouts)
    out_export = r"E:\Sach\Sua\test\VR\model_lms\13_Bridge_VR_HardSurface\exports"
    os.makedirs(out_export, exist_ok=True)
    bpy.ops.object.select_all(action="DESELECT")
    n = 0
    for o in bpy.data.objects:
        if o.type in ("MESH", "EMPTY", "LIGHT"):
            o.select_set(True)
            n += 1
    fbx_path = os.path.join(out_export, "BridgeVR_v3.0_pivot.fbx")
    bpy.ops.export_scene.fbx(
        filepath=fbx_path, use_selection=True, global_scale=1.0,
        apply_unit_scale=True, object_types={"EMPTY", "MESH", "LIGHT"},
        use_mesh_modifiers=True, mesh_smooth_type="OFF", path_mode="COPY",
        embed_textures=True, axis_forward="-Z", axis_up="Y")
    print(f"[export] FBX -> {fbx_path}", flush=True)
    glb_path = os.path.join(out_export, "BridgeVR_v3.0_pivot.glb")
    bpy.ops.export_scene.gltf(
        filepath=glb_path, export_format="GLB", use_selection=True,
        export_apply=True, export_yup=True, export_lights=True,
        export_cameras=False, export_extras=True, export_materials="EXPORT")
    print(f"[export] GLB -> {glb_path}", flush=True)

    print("ALL_DONE", flush=True)


if __name__ == "__main__":
    main()
