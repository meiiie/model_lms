"""Headless render script: open bridge_v2.0_pivot.blend, apply HDRI,
render with EEVEE Next from helmsman wide POV, save hero_v3.0.

Run with:
  blender --background "<blend>" --python "<this script>"

OR (preferred for our case): just run with --python passing args via env.
"""
import bpy
import os
import sys


HDRI = r"E:\Sach\Sua\test\VR\model_lms\_shared\HDRIs\kloppenheim_06_puresky_2k.hdr"
BLEND_IN = r"E:\Sach\Sua\test\VR\model_lms\13_Bridge_VR_HardSurface\source\bridge_v2.0_pivot.blend"
OUT = r"E:\Sach\Sua\test\VR\model_lms\13_Bridge_VR_HardSurface\research\hero_v3.0_eevee_hdri.png"


def main():
    bpy.ops.wm.open_mainfile(filepath=BLEND_IN)
    scene = bpy.context.scene

    # World HDRI
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

    # Reduce internal lights so HDRI dominates
    for n in ("BR_Sun", "BR_CeilingLight_0", "BR_CeilingLight_1",
              "BR_CeilingLight_2", "BR_CeilingLight_3"):
        o = bpy.data.objects.get(n)
        if o and o.type == "LIGHT":
            o.data.energy = 0.5 if o.data.type == "SUN" else 6.0

    # EEVEE render
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 720
    scene.render.image_settings.file_format = "PNG"
    if hasattr(scene, "eevee"):
        if hasattr(scene.eevee, "taa_render_samples"):
            scene.eevee.taa_render_samples = 128
        if hasattr(scene.eevee, "use_raytracing"):
            scene.eevee.use_raytracing = True

    scene.view_settings.view_transform = "AgX"
    scene.view_settings.look = "AgX - Medium High Contrast"

    # Use HelmWide camera if present, else first available camera
    cam = bpy.data.objects.get("HeroCam_v2_HelmWide")
    if cam is None:
        cam = bpy.data.objects.get("HeroCam_v2_LowWide")
    if cam is None:
        for o in bpy.data.objects:
            if o.type == "CAMERA":
                cam = o
                break
    if cam:
        scene.camera = cam

    scene.render.filepath = OUT
    bpy.ops.render.render(write_still=True)
    print(f"RENDER_DONE {OUT}", flush=True)


if __name__ == "__main__":
    main()
