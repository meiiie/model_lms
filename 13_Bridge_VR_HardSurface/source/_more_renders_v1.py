"""Additional render angles for visual review of bridge_v4.0_console_array.blend.
Renders 5 more angles to complement the 3 already produced.
"""
import bpy
import os
import math
import mathutils


BLEND_IN = r"E:\Sach\Sua\test\VR\model_lms\13_Bridge_VR_HardSurface\source\bridge_v4.0_console_array.blend"
OUT_DIR = r"E:\Sach\Sua\test\VR\model_lms\13_Bridge_VR_HardSurface\research"


def look_at(cam, target):
    direction = mathutils.Vector(target) - cam.location
    cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def make_cam(name, lens, location, target):
    cd = bpy.data.cameras.new(name); cd.lens = lens
    cam = bpy.data.objects.new(name, cd)
    bpy.context.scene.collection.objects.link(cam)
    cam.location = location
    look_at(cam, target)
    return cam


def setup_cycles_gpu(scene):
    used_gpu = False
    prefs = bpy.context.preferences.addons.get("cycles")
    if prefs:
        cy = prefs.preferences
        for backend in ("OPTIX", "CUDA", "HIP", "ONEAPI"):
            try:
                cy.compute_device_type = backend
                try: cy.refresh_devices()
                except Exception: pass
                if any(d.type == backend for d in cy.devices):
                    for d in cy.devices: d.use = True
                    used_gpu = True
                    break
            except (TypeError, AttributeError):
                continue
    scene.render.engine = "CYCLES"
    scene.cycles.device = "GPU" if used_gpu else "CPU"
    scene.cycles.samples = 64 if used_gpu else 24
    scene.cycles.use_denoising = True
    if hasattr(scene.cycles, "denoiser"):
        try: scene.cycles.denoiser = "OPTIX" if used_gpu else "OPENIMAGEDENOISE"
        except Exception:
            try: scene.cycles.denoiser = "OPENIMAGEDENOISE"
            except Exception: pass
    return used_gpu


def main():
    bpy.ops.wm.open_mainfile(filepath=BLEND_IN)
    scene = bpy.context.scene
    setup_cycles_gpu(scene)

    scene.render.resolution_x = 1600
    scene.render.resolution_y = 900
    scene.render.image_settings.file_format = "PNG"
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.look = "AgX - Medium High Contrast"

    BULK_Y = -2.50
    SCR_Z = 1.05 * 0.62

    angles = [
        # name, lens, location, target
        ("v4.1_topdown_map", 35, (0.0, -1.0, 5.5), (0.0, -1.0, 0.0)),
        ("v4.1_wheel_closeup", 50, (0.0, 1.0, 1.50), (0.0, -0.05, 1.20)),
        ("v4.1_console_ECDIS_port", 35, (-2.4, -0.6, 1.55), (-2.4, BULK_Y, SCR_Z)),
        ("v4.1_helm_lower_eye", 18, (0.0, 0.8, 1.45), (0.0, BULK_Y, 1.00)),
        ("v4.1_side_layout", 20, (3.5, 0.5, 1.65), (-1.0, -1.5, 1.00)),
        ("v4.1_corner_aft_port", 22, (-3.5, 1.5, 1.95), (1.0, -2.0, 0.80)),
    ]

    for name, lens, loc, tgt in angles:
        cam = make_cam("HeroCam_" + name, lens, loc, tgt)
        scene.camera = cam
        out = os.path.join(OUT_DIR, f"hero_{name}.png")
        scene.render.filepath = out
        bpy.ops.render.render(write_still=True)
        print(f"[render] {name} -> {out}", flush=True)

    print("ALL_DONE", flush=True)


if __name__ == "__main__":
    main()
