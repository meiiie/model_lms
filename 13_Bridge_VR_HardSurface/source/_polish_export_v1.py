"""Phase 5: Add emissive screens, VR grab anchors, polish lighting,
re-render hero, and export FBX + GLB for Unity import.
"""
import bpy
import bmesh
import math
import os


# ---------- 1. Emissive screen plates inside bezels ----------

def make_screen_plate_mesh(name, w, h):
    me = bpy.data.meshes.new(name + "_mesh")
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=0.5)
    for v in bm.verts:
        v.co.x *= w
        v.co.y *= h
    bm.to_mesh(me)
    bm.free()
    return me


def add_screen_plates():
    screen_mat = bpy.data.materials.get("BR_mat_ScreenEmissive")
    plates_added = []
    for obj in list(bpy.data.objects):
        n = obj.name
        if "Bezel_Display" in n or "Bezel_AP" in n or "Bezel_Heading" in n:
            # Get bezel size from mesh
            data = obj.data
            if data is None:
                continue
            # Determine plate size from bezel mesh bounding box (X span and Z span)
            xs = [v.co.x for v in data.vertices]
            zs = [v.co.z for v in data.vertices]
            ys = [v.co.y for v in data.vertices]
            if not xs:
                continue
            plate_w = (max(xs) - min(xs)) * 0.85
            plate_h = (max(zs) - min(zs)) * 0.85
            plate_mesh = make_screen_plate_mesh(n + "_Screen", plate_w, plate_h)
            plate = bpy.data.objects.new(n + "_Screen", plate_mesh)
            # Place INSIDE the bezel, at recess depth
            plate.location = obj.location.copy()
            # Offset slightly forward (along bezel normal which after rotation is +Y world)
            plate.rotation_euler = obj.rotation_euler.copy()
            # Bezel rotation tilts about X axis (math.radians(70)). Plate flush.
            plate.parent = obj
            plate.matrix_parent_inverse = obj.matrix_world.inverted()
            # Move plate slightly forward (along local +Y) inside bezel
            for c in obj.users_collection:
                c.objects.link(plate)
                break
            if screen_mat:
                if plate.data.materials:
                    plate.data.materials[0] = screen_mat
                else:
                    plate.data.materials.append(screen_mat)
            # Re-orient: original grid is XY. To match the bezel which is rotated 70° about X,
            # we want the plate facing front (-Y in world after bezel rotation).
            # Easiest: keep plate aligned with parent bezel via parenting and just tweak local pos.
            plate.location.y -= 0.012  # local -Y offset to sit inside bezel cavity
            plates_added.append(plate.name)
    return plates_added


# ---------- 2. VR grab anchors for interactive items ----------

def add_grab_anchor(name, location, rotation, parent=None, collection=None):
    e = bpy.data.objects.new(name, None)
    e.empty_display_type = "ARROWS"
    e.empty_display_size = 0.04
    e.location = location
    e.rotation_euler = rotation
    if collection:
        collection.objects.link(e)
    if parent:
        e.parent = parent
        e.matrix_parent_inverse = parent.matrix_world.inverted()
    return e


def add_vr_anchors():
    anchor_col = bpy.data.collections["BR_VR_Anchors"]
    added = []
    for obj in bpy.data.objects:
        n = obj.name
        if "_Knob_" in n or "_Sw_" in n or "_Btn_" in n or "GrabRail" in n:
            e = add_grab_anchor(n + "__GrabAnchor",
                                obj.location.copy() + bpy.types.Vector((0, 0, 0.02)) if False else obj.location,
                                (0, 0, 0),
                                parent=obj, collection=anchor_col)
            added.append(e.name)
    return added


# ---------- 3. Lighting polish ----------

def polish_lighting(scene):
    sun = bpy.data.objects.get("BR_Sun")
    if sun and sun.data.type == "SUN":
        sun.data.energy = 2.2
    for i in range(4):
        ld = bpy.data.objects.get(f"BR_CeilingLight_{i}")
        if ld:
            ld.data.energy = 18.0
    sky = scene.world.node_tree.nodes.get("Sky Texture")
    if sky:
        if hasattr(sky, "sun_intensity"):
            try:
                sky.sun_intensity = 0.4
            except Exception:
                pass
    bg = scene.world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs["Strength"].default_value = 0.55


# ---------- 4. Render hero ----------

def render_hero(scene, suffix="v1.0"):
    cam = bpy.data.objects.get("HeroCam")
    if not cam:
        cd = bpy.data.cameras.new("HeroCam")
        cam = bpy.data.objects.new("HeroCam", cd)
        scene.collection.objects.link(cam)
    cam.data.lens = 22
    cam.data.sensor_width = 36
    cam.location = (0.0, -2.10, 1.55)
    cam.rotation_euler = (math.radians(82), 0, 0)
    scene.camera = cam

    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = 1600
    scene.render.resolution_y = 900
    scene.render.image_settings.file_format = "PNG"
    if hasattr(scene.eevee, "taa_render_samples"):
        scene.eevee.taa_render_samples = 96
    if hasattr(scene.eevee, "use_raytracing"):
        scene.eevee.use_raytracing = True

    out = r"E:\Sach\Sua\test\VR\model_lms\13_Bridge_VR_HardSurface\research\hero_" + suffix + ".png"
    scene.render.filepath = out
    bpy.ops.render.render(write_still=True)
    return out


# ---------- 5. Export FBX + GLB ----------

def select_export_set():
    bpy.ops.object.select_all(action="DESELECT")
    export_collections = [
        "BR_Structure", "BR_Glass",
        "BR_Console_Helm", "BR_Console_ECDIS", "BR_Console_Radar",
        "BR_Console_Engine", "BR_Console_Comms", "BR_Compass_Binnacle",
        "BR_VR_Anchors", "BR_Lighting",
    ]
    for cn in export_collections:
        col = bpy.data.collections.get(cn)
        if not col:
            continue
        for o in col.objects:
            o.select_set(True)


def export_fbx_glb(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    select_export_set()

    fbx_path = os.path.join(out_dir, "BridgeVR_HardSurface_v1.0.fbx")
    bpy.ops.export_scene.fbx(
        filepath=fbx_path,
        use_selection=True,
        global_scale=1.0,
        apply_unit_scale=True,
        use_space_transform=True,
        bake_space_transform=False,
        object_types={"EMPTY", "MESH", "LIGHT"},
        use_mesh_modifiers=True,
        mesh_smooth_type="OFF",
        path_mode="COPY",
        embed_textures=True,
        axis_forward="-Z",
        axis_up="Y",
    )

    glb_path = os.path.join(out_dir, "BridgeVR_HardSurface_v1.0.glb")
    bpy.ops.export_scene.gltf(
        filepath=glb_path,
        export_format="GLB",
        use_selection=True,
        export_apply=True,
        export_yup=True,
        export_lights=True,
        export_cameras=False,
        export_extras=True,
        export_materials="EXPORT",
    )

    return {
        "fbx": (fbx_path, os.path.getsize(fbx_path) if os.path.exists(fbx_path) else 0),
        "glb": (glb_path, os.path.getsize(glb_path) if os.path.exists(glb_path) else 0),
    }


# ---------- 6. Main ----------

def main():
    scene = bpy.context.scene
    plates = add_screen_plates()
    # Disable add_vr_anchors for now (Vector import edge case) — add via simpler loop
    anchor_col = bpy.data.collections["BR_VR_Anchors"]
    anchors_added = []
    for obj in list(bpy.data.objects):
        n = obj.name
        if "_Knob_" in n or "_Sw_" in n or "_Btn_" in n or "GrabRail" in n:
            e = bpy.data.objects.new(n + "__Grab", None)
            e.empty_display_type = "ARROWS"
            e.empty_display_size = 0.03
            e.location = (0, 0, 0)
            anchor_col.objects.link(e)
            e.parent = obj
            e.matrix_parent_inverse = obj.matrix_world.inverted()
            anchors_added.append(e.name)

    polish_lighting(scene)

    hero_path = render_hero(scene, suffix="v1.0")

    out_dir = r"E:\Sach\Sua\test\VR\model_lms\13_Bridge_VR_HardSurface\exports"
    export_results = export_fbx_glb(out_dir)

    bpy.ops.wm.save_as_mainfile(
        filepath=r"E:\Sach\Sua\test\VR\model_lms\13_Bridge_VR_HardSurface\source\bridge_v1.0_release.blend"
    )

    return {
        "screen_plates_added": plates,
        "vr_grab_anchors_added": len(anchors_added),
        "hero_render": hero_path,
        "hero_size_kb": os.path.getsize(hero_path) // 1024 if os.path.exists(hero_path) else None,
        "exports": {k: {"path": v[0], "size_kb": v[1] // 1024} for k, v in export_results.items()},
        "saved_blend": "bridge_v1.0_release.blend",
    }


result = main()
