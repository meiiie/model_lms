"""Apply Poly Haven HDRI to world + switch to Cycles + GPU + render hero.
Top-tier techniques: real environment lighting, denoising, AgX color management.
"""
import bpy
import os


HDRI_PATH = r"E:\Sach\Sua\test\VR\model_lms\_shared\HDRIs\kloppenheim_06_puresky_2k.hdr"


def setup_hdri_world(scene):
    world = scene.world or bpy.data.worlds.new("World")
    scene.world = world
    world.use_nodes = True
    nt = world.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputWorld"); out.location = (600, 0)
    bg = nt.nodes.new("ShaderNodeBackground"); bg.location = (400, 0)
    bg.inputs["Strength"].default_value = 1.2
    env = nt.nodes.new("ShaderNodeTexEnvironment"); env.location = (100, 0)
    env.image = bpy.data.images.load(HDRI_PATH, check_existing=True)
    mapping = nt.nodes.new("ShaderNodeMapping"); mapping.location = (-150, 0)
    mapping.inputs["Rotation"].default_value[2] = 1.5
    tc = nt.nodes.new("ShaderNodeTexCoord"); tc.location = (-400, 0)
    nt.links.new(tc.outputs["Generated"], mapping.inputs["Vector"])
    nt.links.new(mapping.outputs["Vector"], env.inputs["Vector"])
    nt.links.new(env.outputs["Color"], bg.inputs["Color"])
    nt.links.new(bg.outputs["Background"], out.inputs["Surface"])


def setup_cycles_gpu(scene):
    prefs = bpy.context.preferences.addons.get("cycles")
    used_gpu = False
    if prefs:
        cyprefs = prefs.preferences
        for backend in ("OPTIX", "CUDA", "HIP", "ONEAPI", "METAL"):
            try:
                cyprefs.compute_device_type = backend
                try:
                    cyprefs.refresh_devices()
                except Exception:
                    pass
                gpu_devs = [d for d in cyprefs.devices
                            if d.type != "CPU" and d.type == backend]
                if gpu_devs:
                    for d in cyprefs.devices:
                        d.use = True
                    used_gpu = True
                    break
            except (TypeError, AttributeError):
                continue
    scene.render.engine = "CYCLES"
    scene.cycles.device = "GPU" if used_gpu else "CPU"
    scene.cycles.samples = 96 if used_gpu else 48
    scene.cycles.use_denoising = True
    if hasattr(scene.cycles, "denoiser"):
        try:
            scene.cycles.denoiser = "OPTIX" if used_gpu else "OPENIMAGEDENOISE"
        except Exception:
            try: scene.cycles.denoiser = "OPENIMAGEDENOISE"
            except Exception: pass
    if hasattr(scene.cycles, "use_adaptive_sampling"):
        scene.cycles.use_adaptive_sampling = True
        try: scene.cycles.adaptive_threshold = 0.02
        except Exception: pass
    return used_gpu


def reduce_competing_lights():
    """Reduce internal lights so HDRI is the dominant illumination."""
    for n in ("BR_Sun", "BR_CeilingLight_0", "BR_CeilingLight_1",
              "BR_CeilingLight_2", "BR_CeilingLight_3"):
        o = bpy.data.objects.get(n)
        if o and o.type == "LIGHT":
            if o.data.type == "SUN":
                o.data.energy = 0.5
            else:
                o.data.energy = 6.0


def main():
    scene = bpy.context.scene
    if not os.path.exists(HDRI_PATH):
        return {"error": f"HDRI not found at {HDRI_PATH}"}

    setup_hdri_world(scene)
    used_gpu = setup_cycles_gpu(scene)
    reduce_competing_lights()

    # Color management
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.look = "AgX - Medium High Contrast"
    scene.view_settings.exposure = 0.0

    # Use existing helmsman wide camera
    cam = bpy.data.objects.get("HeroCam_v2_HelmWide")
    if cam is None:
        # Fallback to LowWide
        cam = bpy.data.objects.get("HeroCam_v2_LowWide")
    if cam:
        scene.camera = cam

    scene.render.resolution_x = 1280
    scene.render.resolution_y = 720
    scene.render.image_settings.file_format = "PNG"
    out_path = r"E:\Sach\Sua\test\VR\model_lms\13_Bridge_VR_HardSurface\research\hero_v3.0_cycles_hdri.png"
    scene.render.filepath = out_path
    bpy.ops.render.render(write_still=True)

    # Save
    bpy.ops.wm.save_mainfile()

    return {
        "used_gpu": used_gpu,
        "render_engine": scene.render.engine,
        "device": scene.cycles.device,
        "samples": scene.cycles.samples,
        "output": out_path,
        "size_kb": os.path.getsize(out_path) // 1024 if os.path.exists(out_path) else None,
        "camera": cam.name if cam else None,
    }


result = main()
