"""Phase 11 - Build front-bulkhead console cabinet + wood kick-plates +
ocean foreplane, then render Cycles hero shots at 1920x1080.

Major visual upgrades targeted:
  - Front-bulkhead horizontal console cabinet so equipment looks "mounted"
  - Wood teak kick-plate strip at floor level
  - Ocean horizontal plane visible through windows (sea horizon)
  - Cycles GPU + denoise + 1920x1080 + 128 samples
  - 3 hero angles + final GLB export
"""
import bpy
import bmesh
import os
import math
import mathutils


HDRI = r"E:\Sach\Sua\test\VR\model_lms\_shared\HDRIs\kloppenheim_06_puresky_2k.hdr"
BLEND_IN = r"E:\Sach\Sua\test\VR\model_lms\13_Bridge_VR_HardSurface\source\bridge_v3.0_hdri_cycles.blend"
OUT_DIR = r"E:\Sach\Sua\test\VR\model_lms\13_Bridge_VR_HardSurface\research"
EXP_DIR = r"E:\Sach\Sua\test\VR\model_lms\13_Bridge_VR_HardSurface\exports"
BLEND_OUT = r"E:\Sach\Sua\test\VR\model_lms\13_Bridge_VR_HardSurface\source\bridge_v4.0_console_array.blend"


# ----------------------------- mesh helpers ---------------------------------

def beveled_box(name, w, d, h, location, rotation=(0, 0, 0), bevel=0.012,
                segments=2, exclude_bottom=True, collection=None):
    me = bpy.data.meshes.new(name + "_mesh")
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co.x *= w * 0.5
        v.co.y *= d * 0.5
        v.co.z = (v.co.z + 0.5) * h
    bm.edges.ensure_lookup_table()
    if exclude_bottom:
        edges = [e for e in bm.edges
                 if not (abs(e.verts[0].co.z) < 0.001 and abs(e.verts[1].co.z) < 0.001)]
    else:
        edges = list(bm.edges)
    bmesh.ops.bevel(bm, geom=edges, offset=bevel, segments=segments,
                    profile=0.5, affect="EDGES")
    bm.to_mesh(me)
    bm.free()
    obj = bpy.data.objects.new(name, me)
    obj.location = location
    obj.rotation_euler = rotation
    if collection is None:
        collection = bpy.context.scene.collection
    collection.objects.link(obj)
    return obj


def add_plane(name, w, h, location, rotation=(0, 0, 0), collection=None):
    me = bpy.data.meshes.new(name + "_mesh")
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=0.5)
    for v in bm.verts:
        v.co.x *= w
        v.co.y *= h
    bm.to_mesh(me)
    bm.free()
    obj = bpy.data.objects.new(name, me)
    obj.location = location
    obj.rotation_euler = rotation
    if collection is None:
        collection = bpy.context.scene.collection
    collection.objects.link(obj)
    return obj


# ----------------------------- material helpers -----------------------------

def principled(name, base, metallic=0.0, roughness=0.5, emission=None,
               emission_strength=0.0, ior=1.45, transmission=0.0, alpha=1.0):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial"); out.location = (400, 0)
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled"); bsdf.location = (0, 0)
    bsdf.inputs["Base Color"].default_value = (*base, 1.0)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    if "IOR" in bsdf.inputs:
        bsdf.inputs["IOR"].default_value = ior
    if "Transmission Weight" in bsdf.inputs:
        bsdf.inputs["Transmission Weight"].default_value = transmission
    if "Alpha" in bsdf.inputs:
        bsdf.inputs["Alpha"].default_value = alpha
    if emission is not None:
        if "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = (*emission, 1.0)
        if "Emission Strength" in bsdf.inputs:
            bsdf.inputs["Emission Strength"].default_value = emission_strength
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return mat


def assign(obj, mat):
    if obj.data is None or not hasattr(obj.data, "materials"):
        return
    obj.data.materials.clear()
    obj.data.materials.append(mat)


def screen_material_with_image(name, image_path, emission_strength=4.0):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial"); out.location = (600, 0)
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled"); bsdf.location = (200, 0)
    bsdf.inputs["Base Color"].default_value = (0.02, 0.03, 0.05, 1.0)
    bsdf.inputs["Metallic"].default_value = 0.0
    bsdf.inputs["Roughness"].default_value = 0.10
    tex = nt.nodes.new("ShaderNodeTexImage"); tex.location = (-200, 0)
    tex.image = bpy.data.images.load(image_path, check_existing=True)
    if "Emission Color" in bsdf.inputs:
        nt.links.new(tex.outputs["Color"], bsdf.inputs["Emission Color"])
    if "Emission Strength" in bsdf.inputs:
        bsdf.inputs["Emission Strength"].default_value = emission_strength
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return mat


# ----------------------------- HDRI -----------------------------------------

def setup_hdri(scene):
    world = scene.world or bpy.data.worlds.new("World")
    scene.world = world
    world.use_nodes = True
    nt = world.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputWorld"); out.location = (600, 0)
    bg = nt.nodes.new("ShaderNodeBackground"); bg.location = (400, 0)
    bg.inputs["Strength"].default_value = 1.1
    env = nt.nodes.new("ShaderNodeTexEnvironment"); env.location = (100, 0)
    env.image = bpy.data.images.load(HDRI, check_existing=True)
    mapping = nt.nodes.new("ShaderNodeMapping"); mapping.location = (-150, 0)
    mapping.inputs["Rotation"].default_value[2] = 1.5
    tc = nt.nodes.new("ShaderNodeTexCoord"); tc.location = (-400, 0)
    nt.links.new(tc.outputs["Generated"], mapping.inputs["Vector"])
    nt.links.new(mapping.outputs["Vector"], env.inputs["Vector"])
    nt.links.new(env.outputs["Color"], bg.inputs["Color"])
    nt.links.new(bg.outputs["Background"], out.inputs["Surface"])


# ----------------------------- Cycles GPU -----------------------------------

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
                if any(d.type == backend for d in cyprefs.devices):
                    for d in cyprefs.devices:
                        d.use = True
                    used_gpu = True
                    break
            except (TypeError, AttributeError):
                continue
    scene.render.engine = "CYCLES"
    scene.cycles.device = "GPU" if used_gpu else "CPU"
    scene.cycles.samples = 96 if used_gpu else 32
    scene.cycles.use_denoising = True
    if hasattr(scene.cycles, "denoiser"):
        try: scene.cycles.denoiser = "OPTIX" if used_gpu else "OPENIMAGEDENOISE"
        except Exception:
            try: scene.cycles.denoiser = "OPENIMAGEDENOISE"
            except Exception: pass
    if hasattr(scene.cycles, "use_adaptive_sampling"):
        scene.cycles.use_adaptive_sampling = True
    print(f"[cycles] gpu={used_gpu} dev={scene.cycles.device} samples={scene.cycles.samples}",
          flush=True)
    return used_gpu


# ----------------------------- camera helpers -------------------------------

def look_at(cam_obj, target):
    direction = mathutils.Vector(target) - cam_obj.location
    cam_obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def make_cam(name, lens, location, target):
    cd = bpy.data.cameras.new(name); cd.lens = lens
    cam = bpy.data.objects.new(name, cd)
    bpy.context.scene.collection.objects.link(cam)
    cam.location = location
    look_at(cam, target)
    return cam


# ----------------------------- main work ------------------------------------

def main():
    # 1. Load v3.0 base
    bpy.ops.wm.open_mainfile(filepath=BLEND_IN)
    scene = bpy.context.scene

    # 2. Make sure HDRI is set up (it should be from v3.0, re-apply for safety)
    setup_hdri(scene)

    # 3. Establish dedicated collection for Phase 11 additions
    p11 = bpy.data.collections.get("Phase11_Additions")
    if p11 is None:
        p11 = bpy.data.collections.new("Phase11_Additions")
        scene.collection.children.link(p11)

    # 4. Materials for new pieces
    mat_console_steel = principled("BR_mat_ConsoleSteel_Dark",
                                    base=(0.06, 0.07, 0.085), metallic=0.10, roughness=0.42)
    mat_kickplate_teak = principled("BR_mat_Teak_KickPlate",
                                     base=(0.18, 0.09, 0.04), metallic=0.0, roughness=0.55)
    mat_console_top = principled("BR_mat_ConsoleTop_Matte",
                                  base=(0.04, 0.045, 0.05), metallic=0.0, roughness=0.78)
    mat_ocean = principled("BR_mat_Ocean",
                            base=(0.012, 0.025, 0.045), metallic=0.0, roughness=0.18,
                            ior=1.33)
    mat_skirt = principled("BR_mat_BulkheadSkirt",
                            base=(0.40, 0.42, 0.43), metallic=0.0, roughness=0.55)

    handoff = r"E:\Sach\Sua\test\VR\model_lms\_shared\Bridge_Reference_Handoff_2026-05-10\02_screen_ui_static"
    ecdis_path = os.path.join(handoff, "generic_training_ecdis_chart_v1.png")
    radar_path = os.path.join(handoff, "generic_training_radar_ppi_v1.png")
    mat_screen_ecdis = screen_material_with_image(
        "BR_mat_ScreenEmissive_ECDIS", ecdis_path, emission_strength=4.0)
    mat_screen_radar = screen_material_with_image(
        "BR_mat_ScreenEmissive_RADAR", radar_path, emission_strength=4.0)

    # 5. Build console cabinet against front bulkhead
    # Bridge cabin is 8x5m (per 06 README); front bulkhead at y ~ -2.5
    BULK_Y = -2.50
    CONSOLE_W = 7.0           # spans most of cabin width
    CONSOLE_D = 0.70
    CONSOLE_H = 1.05
    cabinet_y = BULK_Y + CONSOLE_D / 2 + 0.05  # slightly aft of bulkhead
    cabinet = beveled_box("BR_FrontConsoleCabinet",
                          CONSOLE_W, CONSOLE_D, CONSOLE_H,
                          location=(0.0, cabinet_y, CONSOLE_H / 2),
                          collection=p11)
    assign(cabinet, mat_console_steel)

    # 6. Console TOP slab (slightly larger than cabinet, dark matte)
    top_slab = beveled_box("BR_ConsoleTopSlab",
                           CONSOLE_W + 0.12, CONSOLE_D + 0.10, 0.04,
                           location=(0.0, cabinet_y, CONSOLE_H + 0.02),
                           collection=p11)
    assign(top_slab, mat_console_top)

    # 7. Wood kick-plate strip at console base front
    kick = beveled_box("BR_KickPlate_Teak",
                       CONSOLE_W, 0.04, 0.16,
                       location=(0.0, cabinet_y - CONSOLE_D / 2 - 0.02, 0.08),
                       collection=p11)
    assign(kick, mat_kickplate_teak)

    # 8. Bulkhead skirt below windows (between window lower edge ~1.0m and console top ~1.05m)
    # Just a slim band at z=1.05 to 1.30 on front bulkhead, ABOVE console
    skirt = beveled_box("BR_BulkheadSkirt",
                        CONSOLE_W + 0.6, 0.05, 0.25,
                        location=(0.0, BULK_Y + 0.025, 1.18),
                        collection=p11)
    assign(skirt, mat_skirt)

    # 9. Screen panels embedded in console front face
    # Place 4 screens along the cabinet front, 0.30 wide x 0.30 tall (ECDIS minimum)
    SCR_W = 0.32
    SCR_H = 0.30
    SCR_Z = CONSOLE_H * 0.62   # roughly at upper-third of cabinet front
    SCR_Y = cabinet_y - CONSOLE_D / 2 - 0.005   # right at front face
    layouts = [
        ("ECDIS_PORT_v4", -2.40, mat_screen_ecdis),
        ("RADAR_PORTMID_v4", -0.80, mat_screen_radar),
        ("RADAR_STBDMID_v4", 0.80, mat_screen_radar),
        ("ECDIS_STBD_v4", 2.40, mat_screen_ecdis),
    ]
    for nm, x, mat in layouts:
        # Bezel frame (small dark border)
        bezel = beveled_box(f"{nm}_Bezel", SCR_W + 0.04, 0.018, SCR_H + 0.04,
                            location=(x, SCR_Y - 0.002, SCR_Z),
                            collection=p11)
        assign(bezel, mat_console_top)
        # Inner screen plane, slightly recessed
        plane = add_plane(f"{nm}_ScreenPlane", SCR_W, SCR_H,
                          location=(x, SCR_Y - 0.008, SCR_Z),
                          rotation=(math.radians(90), 0, 0),
                          collection=p11)
        assign(plane, mat_screen_ecdis if "ECDIS" in nm else mat_screen_radar)

    # 10. Ocean plane visible through windows
    ocean = add_plane("BR_OceanPlane", 200.0, 200.0,
                      location=(0.0, -50.0, -0.45),
                      rotation=(0, 0, 0), collection=p11)
    assign(ocean, mat_ocean)
    # Make ocean slightly wavy is overkill; simple flat dark blue plane is fine.

    # 11. Cycles GPU
    used_gpu = setup_cycles_gpu(scene)

    # 12. Reduce competing internal lights
    for n in ("BR_Sun", "BR_CeilingLight_0", "BR_CeilingLight_1",
              "BR_CeilingLight_2", "BR_CeilingLight_3"):
        o = bpy.data.objects.get(n)
        if o and o.type == "LIGHT":
            o.data.energy = 0.6 if o.data.type == "SUN" else 8.0

    # 13. Color management
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.look = "AgX - Medium High Contrast"

    # 14. Resolution + cameras
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.image_settings.file_format = "PNG"

    # Camera A: Helmsman wide POV (most important)
    camA = make_cam("HeroCam_v4_Helm", 16, (0.0, 0.4, 1.65), (0.0, BULK_Y, 1.10))
    scene.camera = camA
    scene.render.filepath = os.path.join(OUT_DIR, "hero_v4.0_helmsman_wide.png")
    bpy.ops.render.render(write_still=True)
    print("[render] helmsman_wide done", flush=True)

    # Camera B: 3/4 overview from upper aft
    camB = make_cam("HeroCam_v4_Overview", 22, (3.0, 1.8, 2.0), (0.0, -2.0, 1.0))
    scene.camera = camB
    scene.render.filepath = os.path.join(OUT_DIR, "hero_v4.0_overview.png")
    bpy.ops.render.render(write_still=True)
    print("[render] overview done", flush=True)

    # Camera C: Operator close-up at one of the screens (ECDIS port)
    camC = make_cam("HeroCam_v4_ScreenCloseup", 35, (-2.4, -1.0, 1.55),
                    (-2.4, BULK_Y, SCR_Z))
    scene.camera = camC
    scene.render.filepath = os.path.join(OUT_DIR, "hero_v4.0_screen_closeup.png")
    bpy.ops.render.render(write_still=True)
    print("[render] screen_closeup done", flush=True)

    # 15. Save .blend
    bpy.ops.wm.save_as_mainfile(filepath=BLEND_OUT)
    print(f"[save] {BLEND_OUT}", flush=True)

    # 16. Export GLB (no embedded HDRI, normal size)
    os.makedirs(EXP_DIR, exist_ok=True)
    bpy.ops.object.select_all(action="DESELECT")
    n = 0
    for o in bpy.data.objects:
        if o.type in ("MESH", "EMPTY", "LIGHT"):
            o.select_set(True); n += 1
    glb_path = os.path.join(EXP_DIR, "BridgeVR_v4.0_console_array.glb")
    bpy.ops.export_scene.gltf(
        filepath=glb_path, export_format="GLB", use_selection=True,
        export_apply=True, export_yup=True, export_lights=True,
        export_cameras=False, export_extras=True, export_materials="EXPORT")
    print(f"[export] GLB -> {glb_path}", flush=True)
    print("ALL_DONE", flush=True)


if __name__ == "__main__":
    main()
