"""Phase 3a: Build modeling kit library for VR maritime bridge.
Run inside Blender via the MCP TCP bridge (port 9876).
Adds parametric kit pieces to BR_Kit_Library collection: panel base,
screen bezels (3 sizes), switch, button, knob, LED, grab rail.
"""
import bpy
import bmesh
import math


def setup_kit_collection(scene):
    if "BR_Kit_Library" not in bpy.data.collections:
        col = bpy.data.collections.new("BR_Kit_Library")
        scene.collection.children.link(col)
    return bpy.data.collections["BR_Kit_Library"]


def new_obj(name, mesh, collection, location=(0, 0, 0)):
    obj = bpy.data.objects.new(name, mesh)
    obj.location = location
    collection.objects.link(obj)
    return obj


def beveled_box_mesh(name, w, d, h, bevel=0.008, segments=2, exclude_bottom=True):
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
    return me


def panel_base():
    W, D, H = 1.55, 0.80, 1.18
    me = beveled_box_mesh("Kit_PanelBase", W, D, H, bevel=0.010, segments=2)
    bm = bmesh.new()
    bm.from_mesh(me)
    bm.faces.ensure_lookup_table()
    top_faces = [f for f in bm.faces if f.normal.z > 0.7]
    if top_faces:
        bmesh.ops.inset_individual(bm, faces=top_faces, thickness=0.025,
                                   depth=-0.012, use_even_offset=True)
    bm.faces.ensure_lookup_table()
    front_faces = [f for f in bm.faces
                   if f.normal.y < -0.7 and f.calc_center_median().z > 0.4]
    if front_faces:
        bmesh.ops.inset_individual(bm, faces=front_faces, thickness=0.020,
                                   depth=-0.008, use_even_offset=True)
    bm.to_mesh(me)
    bm.free()
    return me


def screen_bezel_mesh(name, screen_w, screen_h, bezel=0.025, depth=0.045):
    outer_w = screen_w + 2 * bezel
    outer_h = screen_h + 2 * bezel
    me = bpy.data.meshes.new(name + "_mesh")
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co.x *= outer_w * 0.5
        v.co.z *= outer_h * 0.5
        v.co.y *= depth * 0.5
    bm.faces.ensure_lookup_table()
    front_face = max(bm.faces, key=lambda f: f.normal.y)
    res = bmesh.ops.inset_individual(bm, faces=[front_face], thickness=bezel,
                                     depth=0, use_even_offset=True)
    inner_face = res["faces"][0]
    ext = bmesh.ops.extrude_face_region(bm, geom=[inner_face])
    new_face = [g for g in ext["geom"] if isinstance(g, bmesh.types.BMFace)][0]
    bmesh.ops.translate(bm, verts=new_face.verts, vec=(0, depth * 0.5, 0))
    bm.edges.ensure_lookup_table()
    front_edges = [e for e in bm.edges
                   if all(abs(v.co.y - (-depth * 0.5)) < 0.01 for v in e.verts)]
    bmesh.ops.bevel(bm, geom=front_edges, offset=0.004, segments=2, affect="EDGES")
    bm.to_mesh(me)
    bm.free()
    return me


def toggle_switch_mesh(name):
    me = bpy.data.meshes.new(name + "_mesh")
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co.x *= 0.011
        v.co.y *= 0.011
        v.co.z = (v.co.z + 0.5) * 0.006

    paddle = bmesh.new()
    bmesh.ops.create_cone(paddle, segments=8, radius1=0.0035, radius2=0.0055,
                          depth=0.018, cap_ends=True)
    rot = math.radians(25)
    cos_r, sin_r = math.cos(rot), math.sin(rot)
    for v in paddle.verts:
        y, z = v.co.y, v.co.z
        v.co.y = y * cos_r - z * sin_r
        v.co.z = y * sin_r + z * cos_r
        v.co.z += 0.006 + 0.009

    pmesh = bpy.data.meshes.new("_tmp_paddle")
    paddle.to_mesh(pmesh)
    paddle.free()
    bm.from_mesh(pmesh)
    bpy.data.meshes.remove(pmesh)
    bm.to_mesh(me)
    bm.free()
    return me


def push_button_mesh(name, dia=0.022, height=0.008):
    me = bpy.data.meshes.new(name + "_mesh")
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, segments=16, radius1=dia * 0.5, radius2=dia * 0.5,
                          depth=height, cap_ends=True)
    bm.edges.ensure_lookup_table()
    top_edges = [e for e in bm.edges if all(v.co.z > height * 0.45 for v in e.verts)]
    bmesh.ops.bevel(bm, geom=top_edges, offset=0.0015, segments=2, affect="EDGES")
    bm.to_mesh(me)
    bm.free()
    return me


def knob_mesh(name, dia=0.040, height=0.020, ridges=12):
    me = bpy.data.meshes.new(name + "_mesh")
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, segments=ridges * 2, radius1=dia * 0.5,
                          radius2=dia * 0.5 * 0.95, depth=height, cap_ends=True)
    bm.edges.ensure_lookup_table()
    top_edges = [e for e in bm.edges if all(v.co.z > height * 0.45 for v in e.verts)]
    bmesh.ops.bevel(bm, geom=top_edges, offset=0.0025, segments=2, affect="EDGES")
    bm.to_mesh(me)
    bm.free()
    return me


def led_mesh(name, dia=0.008, height=0.004):
    me = bpy.data.meshes.new(name + "_mesh")
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, segments=10, radius1=dia * 0.5, radius2=dia * 0.5,
                          depth=height, cap_ends=True)
    bm.to_mesh(me)
    bm.free()
    return me


def grab_rail_mesh(name, length=1.4, dia=0.036, segments=12):
    me = bpy.data.meshes.new(name + "_mesh")
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, segments=segments, radius1=dia * 0.5,
                          radius2=dia * 0.5, depth=length, cap_ends=True)
    for v in bm.verts:
        v.co.x, v.co.z = v.co.z, v.co.x
    for x in (-length * 0.45, length * 0.45):
        bracket = bmesh.new()
        bmesh.ops.create_cube(bracket, size=1.0)
        for vv in bracket.verts:
            vv.co.x *= 0.020
            vv.co.y *= 0.040
            vv.co.z = (vv.co.z + 0.5) * 0.080
            vv.co.x += x
            vv.co.z -= 0.040
        tm = bpy.data.meshes.new("_tmp")
        bracket.to_mesh(tm)
        bracket.free()
        bm.from_mesh(tm)
        bpy.data.meshes.remove(tm)
    bm.to_mesh(me)
    bm.free()
    return me


def main():
    scene = bpy.context.scene
    kit_col = setup_kit_collection(scene)

    items = []
    items.append(new_obj("Kit_PanelBase_v1", panel_base(), kit_col, (-6, 5, 0)))
    items.append(new_obj("Kit_Bezel_Small_v1",
                         screen_bezel_mesh("Kit_Bezel_Small", 0.15, 0.10),
                         kit_col, (-4.0, 5, 0.6)))
    items.append(new_obj("Kit_Bezel_Medium_ECDIS_v1",
                         screen_bezel_mesh("Kit_Bezel_Medium_ECDIS", 0.30, 0.30),
                         kit_col, (-3.0, 5, 0.6)))
    items.append(new_obj("Kit_Bezel_Large_v1",
                         screen_bezel_mesh("Kit_Bezel_Large", 0.50, 0.30),
                         kit_col, (-1.5, 5, 0.6)))
    items.append(new_obj("Kit_ToggleSwitch_v1",
                         toggle_switch_mesh("Kit_ToggleSwitch"),
                         kit_col, (0.0, 5, 0.6)))
    items.append(new_obj("Kit_PushButton_v1",
                         push_button_mesh("Kit_PushButton"),
                         kit_col, (0.5, 5, 0.6)))
    items.append(new_obj("Kit_Knob_v1", knob_mesh("Kit_Knob"),
                         kit_col, (1.0, 5, 0.6)))
    items.append(new_obj("Kit_LED_v1", led_mesh("Kit_LED"),
                         kit_col, (1.5, 5, 0.6)))
    items.append(new_obj("Kit_GrabRail_1.4m_v1",
                         grab_rail_mesh("Kit_GrabRail_1.4m"),
                         kit_col, (-6, 5.5, 1.1)))

    for obj in items:
        obj.hide_render = True

    bpy.ops.wm.save_mainfile()

    return {
        "kit_objects": [o.name for o in kit_col.objects],
        "kit_count": len(kit_col.objects),
        "kit_total_polys": sum(len(o.data.polygons) for o in kit_col.objects
                                if o.data and hasattr(o.data, "polygons")),
        "kit_total_verts": sum(len(o.data.vertices) for o in kit_col.objects
                                if o.data and hasattr(o.data, "vertices")),
    }


result = main()
