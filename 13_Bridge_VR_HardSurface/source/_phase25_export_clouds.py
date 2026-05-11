"""Phase 25 - Export BR_Sky_Clouds collection as standalone reusable asset.

Output:
  clouds/BridgeVR_Sky_Clouds_v1.0.blend  - clean blend with only clouds
  clouds/BridgeVR_Sky_Clouds_v1.0.glb    - Unity-importable
  clouds/cloud_preview.png               - what they look like

Includes all 5 cloud billboards + cloud material + drift keyframes.
"""
import bpy
import os
import math
import mathutils


BLEND_IN = r"E:\Sach\Sua\test\VR\model_lms\13_Bridge_VR_HardSurface\source\bridge_v9.0_pro_clouds.blend"
OUT_DIR = r"E:\Sach\Sua\test\VR\model_lms\13_Bridge_VR_HardSurface\clouds"


def main():
    bpy.ops.wm.open_mainfile(filepath=BLEND_IN)
    scene = bpy.context.scene

    # Collect names BEFORE deletion (avoid stale refs)
    clouds_col = bpy.data.collections.get("BR_Sky_Clouds")
    if not clouds_col:
        print("[err] BR_Sky_Clouds collection not found", flush=True)
        return
    cloud_names = [o.name for o in clouds_col.objects]
    print(f"[clouds] keeping: {cloud_names}", flush=True)

    # Delete everything that's NOT in BR_Sky_Clouds
    keep_set = set(cloud_names)
    for o in list(bpy.data.objects):
        if o.name not in keep_set:
            try:
                bpy.data.objects.remove(o, do_unlink=True)
            except Exception:
                pass

    # Clear orphan data
    for me in list(bpy.data.meshes):
        if me.users == 0:
            bpy.data.meshes.remove(me)
    for mat in list(bpy.data.materials):
        if mat.users == 0:
            bpy.data.materials.remove(mat)
    for ld in list(bpy.data.lights):
        bpy.data.lights.remove(ld)
    for ca in list(bpy.data.cameras):
        bpy.data.cameras.remove(ca)

    # Remove empty collections (keep BR_Sky_Clouds)
    for c in list(bpy.data.collections):
        if c.name != "BR_Sky_Clouds" and len(c.objects) == 0:
            try:
                bpy.data.collections.remove(c)
            except Exception:
                pass

    # Move clouds to root if not already direct child of scene
    if clouds_col.name not in [c.name for c in scene.collection.children]:
        scene.collection.children.link(clouds_col)

    # Reposition clouds for standalone preview: center them around origin
    # (currently they're at y=-90..-200; shift to y=-50..0 for compact preview)
    for o in bpy.data.objects:
        if o.name in keep_set:
            o.location.y += 100   # shift forward by 100m so center is around origin

    # Add a preview camera + light for the cloud-only render
    cam_data = bpy.data.cameras.new("CloudPreviewCam")
    cam_data.lens = 35
    cam = bpy.data.objects.new("CloudPreviewCam", cam_data)
    scene.collection.objects.link(cam)
    cam.location = (60, 80, 40)
    direction = mathutils.Vector((0, -50, 25)) - cam.location
    cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    scene.camera = cam

    ld = bpy.data.lights.new("CloudKey", type="SUN")
    ld.energy = 5.0
    ld.color = (1.0, 0.94, 0.82)
    lo = bpy.data.objects.new("CloudKey", ld)
    lo.rotation_euler = (math.radians(72), 0, math.radians(75))
    scene.collection.objects.link(lo)

    # World: simple light blue sky for context
    w = scene.world
    if w:
        w.use_nodes = True
        nt = w.node_tree
        nt.nodes.clear()
        out = nt.nodes.new("ShaderNodeOutputWorld"); out.location = (300, 0)
        bg = nt.nodes.new("ShaderNodeBackground"); bg.location = (0, 0)
        bg.inputs["Color"].default_value = (0.55, 0.72, 0.95, 1.0)
        bg.inputs["Strength"].default_value = 0.8
        nt.links.new(bg.outputs["Background"], out.inputs["Surface"])

    # Render preview at frame 1 then save
    os.makedirs(OUT_DIR, exist_ok=True)
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 720
    scene.render.image_settings.file_format = "PNG"
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.look = "AgX - Medium High Contrast"
    if hasattr(scene.eevee, "taa_render_samples"):
        scene.eevee.taa_render_samples = 32
    preview_path = os.path.join(OUT_DIR, "cloud_preview.png")
    scene.render.filepath = preview_path
    bpy.ops.render.render(write_still=True)
    print(f"[preview] {preview_path}", flush=True)

    # Save as standalone blend
    blend_out = os.path.join(OUT_DIR, "BridgeVR_Sky_Clouds_v1.0.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend_out)
    print(f"[blend] {blend_out}", flush=True)

    # Export as GLB
    bpy.ops.object.select_all(action="DESELECT")
    for o in bpy.data.objects:
        if o.name in keep_set:
            o.select_set(True)
    glb_path = os.path.join(OUT_DIR, "BridgeVR_Sky_Clouds_v1.0.glb")
    try:
        bpy.ops.export_scene.gltf(
            filepath=glb_path, export_format="GLB", use_selection=True,
            export_apply=True, export_yup=True, export_animations=True,
            export_materials="EXPORT")
        print(f"[glb] {glb_path} ({os.path.getsize(glb_path)} bytes)", flush=True)
    except Exception as e:
        print(f"[glb] export failed: {e}", flush=True)

    print("ALL_DONE", flush=True)


if __name__ == "__main__":
    main()
