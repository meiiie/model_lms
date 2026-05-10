"""Phase 3b: Assemble console interiors using BR_Kit_Library pieces.
Also builds wheelhouse structure (deck, ceiling, side walls, front bulkhead with window cut-out).
Replaces wireframe envelopes with real geometry, suitable for VR.
"""
import bpy
import bmesh
import math


WH_WIDTH = 10.0
WH_DEPTH = 6.0
WH_HEIGHT = 2.25

PASSAGE_FRONT = 1.00
CONSOLE_D = 0.80
CONSOLE_FRONT_Y = -PASSAGE_FRONT - CONSOLE_D / 2  # = -1.40

WIN_LOWER = 1.00
WIN_UPPER = 2.00
WIN_INCLINE_DEG = 15.0


def link_instance(name, source_obj, collection, location=(0, 0, 0),
                  rotation=(0, 0, 0)):
    """Create a new object sharing source_obj's mesh data (GPU instancing-friendly)."""
    obj = bpy.data.objects.new(name, source_obj.data)
    obj.location = location
    obj.rotation_euler = rotation
    collection.objects.link(obj)
    return obj


def remove_envelope_refs():
    """Hide the wireframe envelope guides (keep them in REFERENCE for now,
    just mark hide_render and hide_viewport=False so user can toggle)."""
    for name in ("REF_Console_Helm_envelope",
                 "REF_Console_ECDIS_envelope",
                 "REF_Console_Radar_envelope",
                 "REF_Wheelhouse_Envelope"):
        obj = bpy.data.objects.get(name)
        if obj:
            obj.hide_render = True
            obj.hide_viewport = False  # keep visible in viewport as guide


def build_wheelhouse_structure(struct_col, glass_col):
    """Build deck, ceiling, side walls, aft bulkhead, and front bulkhead with
    cut-out for windows. Window glass plane goes in glass_col."""
    # ------- Deck floor -------
    me = bpy.data.meshes.new("WH_Deck_mesh")
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co.x *= WH_WIDTH * 0.5
        v.co.y *= WH_DEPTH * 0.5
        v.co.z = (v.co.z + 0.5) * 0.05  # 50mm thick deck
        v.co.z -= 0.05  # bottom face below z=0 floor reference
    bm.to_mesh(me); bm.free()
    deck = bpy.data.objects.new("WH_Deck", me)
    deck.location = (0, -WH_DEPTH / 2, 0)
    struct_col.objects.link(deck)

    # ------- Ceiling -------
    me = bpy.data.meshes.new("WH_Ceiling_mesh")
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co.x *= WH_WIDTH * 0.5
        v.co.y *= WH_DEPTH * 0.5
        v.co.z = (v.co.z + 0.5) * 0.05
        v.co.z += WH_HEIGHT  # ceiling top at WH_HEIGHT + thickness
    bm.to_mesh(me); bm.free()
    ceiling = bpy.data.objects.new("WH_Ceiling", me)
    ceiling.location = (0, -WH_DEPTH / 2, 0)
    struct_col.objects.link(ceiling)

    # ------- Aft bulkhead (back wall) -------
    me = bpy.data.meshes.new("WH_AftBulkhead_mesh")
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co.x *= WH_WIDTH * 0.5
        v.co.y *= 0.04  # 40mm wall thickness
        v.co.z = (v.co.z + 0.5) * WH_HEIGHT
    bm.to_mesh(me); bm.free()
    aft = bpy.data.objects.new("WH_AftBulkhead", me)
    aft.location = (0, -WH_DEPTH, 0)
    struct_col.objects.link(aft)

    # ------- Side walls (port + starboard) -------
    for x_sign, side in ((1, "STBD"), (-1, "PORT")):
        me = bpy.data.meshes.new(f"WH_SideWall_{side}_mesh")
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        for v in bm.verts:
            v.co.x *= 0.04
            v.co.y *= WH_DEPTH * 0.5
            v.co.z = (v.co.z + 0.5) * WH_HEIGHT
        bm.to_mesh(me); bm.free()
        wall = bpy.data.objects.new(f"WH_SideWall_{side}", me)
        wall.location = (x_sign * WH_WIDTH * 0.5, -WH_DEPTH / 2, 0)
        struct_col.objects.link(wall)

    # ------- Front bulkhead with window opening -------
    # Build as 4 strips: bottom (under window), top (over window), and 2 thin
    # vertical strips at port/starboard ends. Approximate front face is flat
    # vertical; the window glass with incline 15° will sit slightly forward.
    me = bpy.data.meshes.new("WH_FrontBulkhead_mesh")
    bm = bmesh.new()

    def add_strip(width, height, cx, cz, depth=0.04):
        b2 = bmesh.new()
        bmesh.ops.create_cube(b2, size=1.0)
        for v in b2.verts:
            v.co.x *= width * 0.5
            v.co.y *= depth * 0.5
            v.co.z = (v.co.z + 0.5) * height + cz
            v.co.x += cx
        tm = bpy.data.meshes.new("_tmp")
        b2.to_mesh(tm); b2.free()
        bm.from_mesh(tm)
        bpy.data.meshes.remove(tm)

    # Bottom strip: full width × WIN_LOWER tall (0 → 1.0m)
    add_strip(WH_WIDTH, WIN_LOWER, 0, 0)
    # Top strip: full width × (WH_HEIGHT - WIN_UPPER) tall (2.0 → 2.25m)
    top_h = WH_HEIGHT - WIN_UPPER
    if top_h > 0.001:
        add_strip(WH_WIDTH, top_h, 0, WIN_UPPER)
    # Side strips at the X edges of the window opening (last 0.5m of each side)
    side_w = 0.5
    add_strip(side_w, WIN_UPPER - WIN_LOWER,
              -WH_WIDTH / 2 + side_w / 2, WIN_LOWER)
    add_strip(side_w, WIN_UPPER - WIN_LOWER,
              WH_WIDTH / 2 - side_w / 2, WIN_LOWER)

    # 2 mullions at x = ±(WH_WIDTH/2 - side_w - 2.5) — divide window into 5 panes
    # (4 vertical mullions, 5 panes)
    pane_count = 5
    span = WH_WIDTH - 2 * side_w
    mullion_thick = 0.12  # ABS allows up to 150mm, use 120 for visual lighter
    pane_width = (span - (pane_count - 1) * mullion_thick) / pane_count
    for i in range(1, pane_count):
        cx = -span / 2 + i * pane_width + (i - 0.5) * mullion_thick
        add_strip(mullion_thick, WIN_UPPER - WIN_LOWER, cx, WIN_LOWER)

    bm.to_mesh(me); bm.free()
    front = bpy.data.objects.new("WH_FrontBulkhead", me)
    front.location = (0, 0, 0)
    struct_col.objects.link(front)

    # ------- Front window glass (single inclined plane spanning the opening) -------
    me = bpy.data.meshes.new("WH_FrontWindow_Glass_mesh")
    bm = bmesh.new()
    glass_w = WH_WIDTH - 2 * side_w
    glass_h = WIN_UPPER - WIN_LOWER
    # Build a simple plane the size we want, then rotate/translate
    bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=0.5)
    # By default plane is in XY at z=0 with extent ±0.5
    for v in bm.verts:
        v.co.x *= glass_w
        v.co.y *= glass_h
    bm.to_mesh(me); bm.free()
    glass = bpy.data.objects.new("WH_FrontWindow_Glass", me)
    # Rotate so plane stands vertical with top inclined out (X axis horizontal,
    # Z axis vertical). Initial plane is in XY plane; rotate +90° around X
    # makes it XZ plane (vertical, facing -Y). Then incline top out by
    # WIN_INCLINE_DEG (top tilts toward +Y).
    glass.rotation_euler = (math.radians(90 - WIN_INCLINE_DEG), 0, 0)
    # Place at center of opening, slightly forward (+Y) of bulkhead front face
    glass_cz = (WIN_LOWER + WIN_UPPER) * 0.5
    glass.location = (0, 0.05, glass_cz)
    glass_col.objects.link(glass)


def populate_console(name_prefix, base_x, collection, kit, layout="ECDIS"):
    """Build one console at base_x using kit linked instances."""
    panel_src = kit["Kit_PanelBase_v1"]
    bezel_med = kit["Kit_Bezel_Medium_ECDIS_v1"]
    bezel_sml = kit["Kit_Bezel_Small_v1"]
    bezel_lrg = kit["Kit_Bezel_Large_v1"]
    sw_src = kit["Kit_ToggleSwitch_v1"]
    pb_src = kit["Kit_PushButton_v1"]
    kn_src = kit["Kit_Knob_v1"]
    led_src = kit["Kit_LED_v1"]
    gr_src = kit["Kit_GrabRail_1.4m_v1"]

    # Panel base placed so its bottom sits at z=0, front face at y=CONSOLE_FRONT_Y - D/2
    panel = link_instance(f"{name_prefix}_PanelBase", panel_src, collection,
                          location=(base_x, CONSOLE_FRONT_Y, 0))

    # Top surface z = 1.18 (panel height)
    top_z = 1.18
    top_inset = 0.012
    # Top is recessed to z = 1.18 - 0.012 = 1.168 (panel inset top)
    surface_z = top_z - top_inset
    # Front fascia front face Y = CONSOLE_FRONT_Y - D/2 = -1.40 - 0.40 = -1.80
    front_y = CONSOLE_FRONT_Y - CONSOLE_D / 2

    # Layout-specific instrument placement on TOP surface (slightly tilted forward)
    if layout == "ECDIS" or layout == "RADAR":
        # ECDIS/Radar: 1 large medium bezel centered + 4 buttons row underneath
        bezel = link_instance(f"{name_prefix}_Bezel_Display", bezel_med,
                              collection,
                              location=(base_x, CONSOLE_FRONT_Y - 0.05,
                                        surface_z + 0.025),
                              rotation=(math.radians(70), 0, 0))
        # row of 6 buttons in front of bezel (lower edge of top)
        for i, dx in enumerate([-0.18, -0.108, -0.036, 0.036, 0.108, 0.18]):
            link_instance(f"{name_prefix}_Btn_{i}", pb_src, collection,
                          location=(base_x + dx, CONSOLE_FRONT_Y + 0.18,
                                    surface_z + 0.005),
                          rotation=(0, 0, 0))
        # 2 knobs at corners
        for i, dx in enumerate([-0.32, 0.32]):
            link_instance(f"{name_prefix}_Knob_{i}", kn_src, collection,
                          location=(base_x + dx, CONSOLE_FRONT_Y + 0.18,
                                    surface_z + 0.010),
                          rotation=(0, 0, 0))
        # 2 LED indicators
        for i, dx in enumerate([-0.40, 0.40]):
            link_instance(f"{name_prefix}_LED_{i}", led_src, collection,
                          location=(base_x + dx, CONSOLE_FRONT_Y + 0.20,
                                    surface_z + 0.002),
                          rotation=(0, 0, 0))
    elif layout == "HELM":
        # Helm: 1 small heading display top-center + array of switches/buttons/knobs
        link_instance(f"{name_prefix}_Bezel_Heading", bezel_sml,
                      collection,
                      location=(base_x, CONSOLE_FRONT_Y - 0.05,
                                surface_z + 0.01),
                      rotation=(math.radians(70), 0, 0))
        # 1 large bezel for autopilot panel
        link_instance(f"{name_prefix}_Bezel_AP", bezel_lrg,
                      collection,
                      location=(base_x, CONSOLE_FRONT_Y - 0.20,
                                surface_z + 0.025),
                      rotation=(math.radians(70), 0, 0))
        # 6 toggle switches (auto/manual modes etc.)
        for i, dx in enumerate([-0.30, -0.18, -0.06, 0.06, 0.18, 0.30]):
            link_instance(f"{name_prefix}_Sw_{i}", sw_src, collection,
                          location=(base_x + dx, CONSOLE_FRONT_Y + 0.10,
                                    surface_z + 0.001),
                          rotation=(0, 0, 0))
        # 4 push buttons (course +/-, take command)
        for i, dx in enumerate([-0.12, -0.04, 0.04, 0.12]):
            link_instance(f"{name_prefix}_Btn_{i}", pb_src, collection,
                          location=(base_x + dx, CONSOLE_FRONT_Y + 0.22,
                                    surface_z + 0.005),
                          rotation=(0, 0, 0))
        # 2 knobs (course, rudder limit)
        for i, dx in enumerate([-0.42, 0.42]):
            link_instance(f"{name_prefix}_Knob_{i}", kn_src, collection,
                          location=(base_x + dx, CONSOLE_FRONT_Y + 0.16,
                                    surface_z + 0.010),
                          rotation=(0, 0, 0))

    # Grab rail along front, at z ~ 1.0m (waist height for standing operator)
    link_instance(f"{name_prefix}_GrabRail", gr_src, collection,
                  location=(base_x, front_y - 0.025, 1.00),
                  rotation=(0, 0, 0))


def main():
    scene = bpy.context.scene
    struct_col = bpy.data.collections["BR_Structure"]
    glass_col = bpy.data.collections["BR_Glass"]
    helm_col = bpy.data.collections["BR_Console_Helm"]
    ecdis_col = bpy.data.collections["BR_Console_ECDIS"]
    radar_col = bpy.data.collections["BR_Console_Radar"]
    kit_col = bpy.data.collections["BR_Kit_Library"]
    kit = {o.name: o for o in kit_col.objects}

    remove_envelope_refs()
    build_wheelhouse_structure(struct_col, glass_col)

    populate_console("HELM", 0.0, helm_col, kit, layout="HELM")
    populate_console("ECDIS_PORT", -2.5, ecdis_col, kit, layout="ECDIS")
    populate_console("RADAR_STBD", 2.5, radar_col, kit, layout="RADAR")
    # Add a second ECDIS bay (port-far, common on bridges)
    populate_console("ECDIS_PORT_FAR", -4.2, ecdis_col, kit, layout="ECDIS")
    # Add a second radar bay (stbd-far)
    populate_console("RADAR_STBD_FAR", 4.2, radar_col, kit, layout="RADAR")

    bpy.ops.wm.save_as_mainfile(
        filepath=r"E:\Sach\Sua\test\VR\model_lms\13_Bridge_VR_HardSurface\source\bridge_v0.2_assembled.blend"
    )

    # Tally
    tris = sum(len(o.data.polygons) for o in bpy.data.objects
               if o.data and hasattr(o.data, "polygons") and not o.hide_render)
    return {
        "saved_to": r"bridge_v0.2_assembled.blend",
        "objects_total": len(bpy.data.objects),
        "objects_render_visible": sum(1 for o in bpy.data.objects if not o.hide_render),
        "approx_render_polys": tris,
        "console_objects_per_collection": {
            c.name: len(c.objects) for c in [helm_col, ecdis_col, radar_col, struct_col, glass_col]
        },
    }


result = main()
