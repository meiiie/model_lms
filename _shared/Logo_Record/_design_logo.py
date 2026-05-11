"""Design "Compass Record" logo via Blender.

Mathematical principles (like NASA / Apple / Twitter logo design):
  - 8-fold rotational symmetry (compass cardinal + intercardinal points)
  - Golden ratio proportions for nested circles
  - Square canvas with rounded geometry centered at origin

Color palette (semantic):
  - Maritime navy   #0A2540   = authority, ocean depth, professionalism
  - Recording red   #C8102E   = standard broadcast "record" red (Pantone 186)
  - Pure white      #FFFFFF   = clarity, navigation light, separation

Layers (concentric, from outside in):
  L1  Background square (navy) - frame
  L2  Outer compass-rose ring (white) - 8 large lobes at 45deg steps
  L3  Inner ring breathing space (navy) - golden-ratio sized gap
  L4  Recording dot (red solid disc) - the "record" signal

Proportions (canvas = 1000 x 1000 units, all in mm):
  Canvas        1000   (1.0)
  Outer-rose R   460   (canvas / phi*2 * 2 = ~460)
  Inner-rose R   285   (outer R / phi)
  Red disc R     176   (inner R / phi)
  Lobe radius     90   (outer R * sin(pi/8))
  Stroke         24    (canvas / 41.66 ~= 2.4%)

8 petals are circles arranged on a ring; their radii sum to fit ~ 2*pi*R / 8.
"""
import bpy
import bmesh
import math
import os


PROJECT = r"E:\Sach\Sua\test\VR\model_lms\_shared\Logo_Record"


PHI = (1 + 5 ** 0.5) / 2     # 1.618
CANVAS = 1.0                  # work in Blender units (1.0 = canvas)


def _srgb_to_linear(c):
    if c <= 0.04045:
        return c / 12.92
    return ((c + 0.055) / 1.055) ** 2.4


def hex_lin(hex_str):
    """#RRGGBB sRGB -> linear RGBA tuple Blender Emission expects."""
    h = hex_str.lstrip("#")
    r, g, b = int(h[0:2], 16) / 255.0, int(h[2:4], 16) / 255.0, int(h[4:6], 16) / 255.0
    return (_srgb_to_linear(r), _srgb_to_linear(g), _srgb_to_linear(b), 1.0)


# Professional palette: hex codes from established design systems.
# After sRGB->linear conversion these render as the exact target hex in PNG.
NAVY = hex_lin("#0A2540")          # deep maritime navy (authority, ocean depth)
RECORD_RED = hex_lin("#C8102E")    # Pantone 186 - broadcast-standard "record"
WHITE = hex_lin("#FFFFFF")


def _ensure_collection(name, scene):
    c = bpy.data.collections.get(name)
    if c is None:
        c = bpy.data.collections.new(name)
        scene.collection.children.link(c)
    return c


def _mat(name, color, emission_strength=0.0):
    """Pure Emission shader - guarantees exact pixel color in framebuffer
    regardless of lighting / view transform. Standard practice for logo art."""
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial"); out.location = (400, 0)
    emi = nt.nodes.new("ShaderNodeEmission"); emi.location = (0, 0)
    emi.inputs["Color"].default_value = color
    emi.inputs["Strength"].default_value = 1.0
    nt.links.new(emi.outputs["Emission"], out.inputs["Surface"])
    return mat


def make_disc(name, radius, z, segments=128, collection=None, material=None):
    me = bpy.data.meshes.new(name + "_mesh")
    bm = bmesh.new()
    bmesh.ops.create_circle(bm, segments=segments, radius=radius, cap_ends=True)
    bm.to_mesh(me); bm.free()
    obj = bpy.data.objects.new(name, me)
    obj.location.z = z
    if collection:
        collection.objects.link(obj)
    if material:
        obj.data.materials.append(material)
    return obj


def make_square(name, half_size, z, collection=None, material=None):
    me = bpy.data.meshes.new(name + "_mesh")
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=half_size)
    bm.to_mesh(me); bm.free()
    obj = bpy.data.objects.new(name, me)
    obj.location.z = z
    if collection:
        collection.objects.link(obj)
    if material:
        obj.data.materials.append(material)
    return obj


def make_compass_rose(name, ring_radius, lobe_radius, n=8, z=0.0,
                     collection=None, material=None):
    """Create one rosette layer:
       - central disc of radius ring_radius
       - n lobe circles placed on the ring at radius (ring_radius - lobe_radius/2)
       This produces the classic scalloped circle look.
    """
    # Use bmesh union of central + lobes
    me = bpy.data.meshes.new(name + "_mesh")
    bm = bmesh.new()
    # Central solid disc
    center = bmesh.ops.create_circle(
        bm, segments=128, radius=ring_radius, cap_ends=True)
    # Lobes
    on_ring_R = ring_radius
    for i in range(n):
        angle = 2 * math.pi * i / n
        cx = on_ring_R * math.cos(angle)
        cy = on_ring_R * math.sin(angle)
        # Create temp bmesh, then merge into main bm
        lobe_bm = bmesh.new()
        bmesh.ops.create_circle(lobe_bm, segments=48, radius=lobe_radius,
                                cap_ends=True)
        # Translate verts of lobe_bm
        for v in lobe_bm.verts:
            v.co.x += cx
            v.co.y += cy
        # Append into bm via temp mesh
        tmp = bpy.data.meshes.new("_tmp")
        lobe_bm.to_mesh(tmp); lobe_bm.free()
        bm.from_mesh(tmp)
        bpy.data.meshes.remove(tmp)
    bm.to_mesh(me); bm.free()
    obj = bpy.data.objects.new(name, me)
    obj.location.z = z
    if collection:
        collection.objects.link(obj)
    if material:
        obj.data.materials.append(material)
    return obj


def clear_scene():
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    for me in list(bpy.data.meshes):
        bpy.data.meshes.remove(me)
    for c in list(bpy.data.collections):
        try:
            bpy.context.scene.collection.children.unlink(c)
        except Exception:
            pass


def main():
    clear_scene()
    scene = bpy.context.scene

    # Materials
    mat_navy = _mat("Logo_Navy", NAVY)
    mat_white = _mat("Logo_White", WHITE)
    mat_red = _mat("Logo_RecordRed", RECORD_RED, emission_strength=0.0)

    logo_col = _ensure_collection("Logo_Record", scene)

    # Mathematical proportions (golden ratio nesting)
    # Canvas: square -0.5..+0.5 in xy.
    # For an n-petal rosette where lobes tangentially touch on the ring,
    # total extent = R_center * (1 + sin(pi/n)).
    # n = 12 outer (clock/zodiac symmetry), n = 8 inner (compass cardinal).
    background_half = 0.50
    n_outer = 12
    n_inner = 8
    total_outer = 0.46                                      # 92% canvas
    outer_rose_R = total_outer / (1 + math.sin(math.pi / n_outer))
    outer_lobe_R = outer_rose_R * math.sin(math.pi / n_outer)
    # White rosette donut: inner edge of navy ring sits at outer_rose_R - 2*lobe = donut
    # Navy breathing gap (negative space): radius (outer_rose_R - outer_lobe_R) / phi
    inner_navy_R = (outer_rose_R - outer_lobe_R) / PHI
    # Red rosette occupies the inner navy disc
    total_red = inner_navy_R * 0.92
    red_rose_R = total_red / (1 + math.sin(math.pi / n_inner))
    red_lobe_R = red_rose_R * math.sin(math.pi / n_inner)
    # Solid red center dot (record signal) - golden ratio of red rosette
    red_disc_R = red_rose_R / PHI

    # Z layering (stack along +Z so camera ortho top-down sees correctly)
    z_bg = 0.000
    z_white_rose = 0.001
    z_navy_ring = 0.002
    z_red_rose = 0.003
    z_red_dot = 0.004

    # L1 Background square (navy)
    make_square("L1_Background", background_half, z_bg, logo_col, mat_navy)
    # L2 White compass rosette (12-fold = clock/zodiac symmetry)
    make_compass_rose("L2_WhiteRosette", outer_rose_R, outer_lobe_R,
                       n=n_outer, z=z_white_rose, collection=logo_col,
                       material=mat_white)
    # L3 Navy inner disc (negative space)
    make_disc("L3_NavyInnerDisc", inner_navy_R, z_navy_ring, segments=128,
              collection=logo_col, material=mat_navy)
    # L4 Red compass rosette (8-fold = compass cardinal+intercardinal)
    make_compass_rose("L4_RedRosette", red_rose_R, red_lobe_R,
                       n=n_inner, z=z_red_rose, collection=logo_col,
                       material=mat_red)
    # L5 Red solid central dot
    make_disc("L5_RedRecordDot", red_disc_R, z_red_dot, segments=128,
              collection=logo_col, material=mat_red)

    # Top-down orthographic camera
    cam_data = bpy.data.cameras.new("LogoCam")
    cam_data.type = "ORTHO"
    cam_data.ortho_scale = 1.04   # slight padding around the canvas
    cam = bpy.data.objects.new("LogoCam", cam_data)
    cam.location = (0, 0, 5)
    cam.rotation_euler = (0, 0, 0)
    scene.collection.objects.link(cam)
    scene.camera = cam

    # EEVEE flat shading - Principled BSDF base colors render correctly.
    # AgX OFF for design work (we want exact hex colors, not tonemapped).
    scene.render.engine = "BLENDER_EEVEE"
    scene.view_settings.view_transform = "Standard"
    scene.view_settings.look = "None"
    if hasattr(scene.eevee, "taa_render_samples"):
        scene.eevee.taa_render_samples = 64
    if hasattr(scene.eevee, "use_raytracing"):
        scene.eevee.use_raytracing = False
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"

    # Add a flat overhead sun light for visible coloring
    sun_data = bpy.data.lights.new("LogoSun", type="SUN")
    sun_data.energy = 3.0
    sun_data.color = (1.0, 1.0, 1.0)
    sun_obj = bpy.data.objects.new("LogoSun", sun_data)
    sun_obj.location = (0, 0, 5)
    sun_obj.rotation_euler = (0, 0, 0)
    scene.collection.objects.link(sun_obj)

    # World as pure white (no HDRI)
    world = scene.world or bpy.data.worlds.new("World")
    scene.world = world
    world.use_nodes = True
    nt_w = world.node_tree
    nt_w.nodes.clear()
    out_w = nt_w.nodes.new("ShaderNodeOutputWorld"); out_w.location = (300, 0)
    bg_w = nt_w.nodes.new("ShaderNodeBackground"); bg_w.location = (0, 0)
    bg_w.inputs["Color"].default_value = (0, 0, 0, 1)
    bg_w.inputs["Strength"].default_value = 0.0
    nt_w.links.new(bg_w.outputs["Background"], out_w.inputs["Surface"])

    os.makedirs(PROJECT, exist_ok=True)

    # Render at multiple resolutions
    for res in (1024, 512, 256, 128, 64, 32):
        scene.render.resolution_x = res
        scene.render.resolution_y = res
        scene.render.resolution_percentage = 100
        # Disable bg transparency for navy version
        scene.render.film_transparent = False
        scene.render.filepath = os.path.join(PROJECT, f"logo_record_{res}.png")
        bpy.ops.render.render(write_still=True)
        print(f"[render] {res}x{res} -> {scene.render.filepath}", flush=True)

    # Also render transparent-background variant (hide L1 background)
    bg = bpy.data.objects.get("L1_Background")
    if bg:
        bg.hide_render = True
    scene.render.film_transparent = True
    for res in (1024, 512, 256):
        scene.render.resolution_x = res
        scene.render.resolution_y = res
        scene.render.filepath = os.path.join(
            PROJECT, f"logo_record_transparent_{res}.png")
        bpy.ops.render.render(write_still=True)
        print(f"[render] transparent {res}x{res}", flush=True)
    bg.hide_render = False

    # Save .blend
    blend_path = os.path.join(PROJECT, "logo_design.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print(f"[save] {blend_path}", flush=True)
    print("ALL_DONE", flush=True)


if __name__ == "__main__":
    main()
