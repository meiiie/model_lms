"""Phase 21 - Quick HDRI rotation test to find cloud-visible angle.

The HDRI has cumulus clouds in some directions and clear sky in others.
We render 4 test images at Z rotation 0, pi/2, pi, 3pi/2 from
HeroCam_v4_Overview camera (which sees a window). User picks the best.
"""
import bpy
import math
import os


BLEND_IN = r"E:\Sach\Sua\test\VR\model_lms\13_Bridge_VR_HardSurface\source\bridge_v8.0_partly_cloudy.blend"
OUT_DIR = r"E:\Sach\Sua\test\VR\model_lms\13_Bridge_VR_HardSurface\research"


def set_hdri_rotation_z(scene, rad):
    world = scene.world
    nt = world.node_tree
    for n in nt.nodes:
        if n.type == "MAPPING":
            cur = list(n.inputs["Rotation"].default_value)
            cur[2] = rad
            n.inputs["Rotation"].default_value = cur
            return True
    return False


def main():
    bpy.ops.wm.open_mainfile(filepath=BLEND_IN)
    scene = bpy.context.scene
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

    # Use the original v4 overview camera (3/4 view of full bridge) so we
    # see windows AND interior at the same time
    cam = bpy.data.objects.get("HeroCam_v4_Overview") or bpy.data.objects.get("HeroCam_Anim")
    scene.camera = cam

    angles = [
        ("0deg", 0.0),
        ("90deg", math.radians(90)),
        ("180deg", math.radians(180)),
        ("270deg", math.radians(270)),
    ]

    scene.frame_set(1)
    for tag, rad in angles:
        set_hdri_rotation_z(scene, rad)
        out_p = os.path.join(OUT_DIR, f"hdri_rotation_test_{tag}.png")
        scene.render.filepath = out_p
        bpy.ops.render.render(write_still=True)
        print(f"[render] HDRI Z={tag} -> {out_p}", flush=True)

    print("ALL_DONE", flush=True)


if __name__ == "__main__":
    main()
