"""Phase 14 - Add demo animations to bridge scene.

Animations added (Blender keyframes; Unity will animate at runtime in VR):
  A) Ship wheel rotation (loops 360 deg every 4 sec)
  B) Compass card oscillation (mimics ship swaying +/- 12 deg yaw)
  C) Engine telegraph (EOT) lever swing between positions
  D) Captain "sit-down" camera animation (entrance -> seated POV)
  E) Bridge alarm panel LEDs blinking (emission strength keyframed)
  F) An overview camera orbit for the cinematic preview

Renders an EEVEE MP4 (1280x720, 30 fps, 8 sec = 240 frames) showing all
animations playing simultaneously, plus 4 keyframe preview PNGs.
"""
import bpy
import math
import os


BLEND_IN = r"E:\Sach\Sua\test\VR\model_lms\13_Bridge_VR_HardSurface\source\bridge_v4.0_console_array.blend"
BLEND_OUT = r"E:\Sach\Sua\test\VR\model_lms\13_Bridge_VR_HardSurface\source\bridge_v5.0_animated.blend"
OUT_DIR = r"E:\Sach\Sua\test\VR\model_lms\13_Bridge_VR_HardSurface\research"
MP4_OUT = os.path.join(OUT_DIR, "anim_v5.0_bridge_demo.mp4")


def find_obj_by(part_names):
    """Return the first object whose name contains any of the given substrings."""
    for o in bpy.data.objects:
        ln = o.name.lower()
        for p in part_names:
            if p in ln:
                return o
    return None


def kf(obj, frame, **prop_value):
    for prop, val in prop_value.items():
        setattr(obj, prop, val)
        obj.keyframe_insert(data_path=prop, frame=frame)


def _iter_fcurves(obj):
    """Yield fcurves across Blender 4.x (action.fcurves) and 5.x (layered)."""
    if not (obj.animation_data and obj.animation_data.action):
        return
    act = obj.animation_data.action
    fcurves = getattr(act, "fcurves", None)
    if fcurves:
        for fc in fcurves:
            yield fc
        return
    # Blender 5.x layered animation
    for layer in getattr(act, "layers", []):
        for strip in getattr(layer, "strips", []):
            for ch in getattr(strip, "channelbags", []):
                for fc in getattr(ch, "fcurves", []):
                    yield fc
            channels = getattr(strip, "channels", None)
            if channels:
                for fc in channels:
                    yield fc


def set_linear_interp(obj):
    for fc in _iter_fcurves(obj):
        for k in fc.keyframe_points:
            k.interpolation = "LINEAR"


def set_bezier_interp(obj):
    for fc in _iter_fcurves(obj):
        for k in fc.keyframe_points:
            k.interpolation = "BEZIER"


def main():
    bpy.ops.wm.open_mainfile(filepath=BLEND_IN)
    scene = bpy.context.scene

    scene.render.fps = 30
    TOTAL_FRAMES = 240   # 8 seconds at 30 fps
    scene.frame_start = 1
    scene.frame_end = TOTAL_FRAMES

    # --- A) Ship wheel rotation (loops 360 deg over 240 frames) -----------
    wheel = find_obj_by(["wheel_pivot"])
    if wheel:
        base_rot = list(wheel.rotation_euler)
        # Ship wheel typically rotates about its forward (Y) axis when mounted
        # forward-facing. We try Y first.
        kf(wheel, 1, rotation_euler=(base_rot[0], base_rot[1], base_rot[2]))
        kf(wheel, TOTAL_FRAMES,
           rotation_euler=(base_rot[0], base_rot[1] + math.radians(720),
                           base_rot[2]))
        set_linear_interp(wheel)
        print(f"[anim] wheel rotation set on {wheel.name}", flush=True)
    else:
        print("[anim] wheel_pivot not found", flush=True)

    # --- B) Compass card oscillation (mimics ship sway) -------------------
    card = find_obj_by(["compass_card", "card", "magcompass"])
    if card and "card" in card.name.lower():
        base = card.rotation_euler.copy()
        amp = math.radians(12)
        # 4 sec period: peaks at 30, 90, 150, 210
        kf(card, 1, rotation_euler=(base.x, base.y, base.z))
        kf(card, 60, rotation_euler=(base.x, base.y, base.z + amp))
        kf(card, 120, rotation_euler=(base.x, base.y, base.z))
        kf(card, 180, rotation_euler=(base.x, base.y, base.z - amp))
        kf(card, 240, rotation_euler=(base.x, base.y, base.z))
        set_bezier_interp(card)
        print(f"[anim] compass card oscillation on {card.name}", flush=True)
    else:
        print("[anim] compass card not found", flush=True)

    # --- C) Engine telegraph pointer/handle swing -------------------------
    # In 06 scene, EOT pointer object names include 'pointer_ordered',
    # 'pointer_answered', 'eot_dome', 'eot_handle' etc.
    pointer = find_obj_by(["pointer_ordered", "eot_pointer", "eot_handle",
                            "telegraph_lever", "lever"])
    if pointer:
        base = pointer.rotation_euler.copy()
        # Swing through 4 positions: Stop -> Slow Ahead -> Half Ahead -> Stop
        positions_deg = [0, -30, -60, -30, 0]
        frame_per_pos = TOTAL_FRAMES // (len(positions_deg) - 1)
        for i, deg in enumerate(positions_deg):
            f = 1 + i * frame_per_pos
            kf(pointer, f,
               rotation_euler=(base.x, base.y + math.radians(deg), base.z))
        set_bezier_interp(pointer)
        print(f"[anim] EOT pointer swing on {pointer.name}", flush=True)
    else:
        print("[anim] EOT pointer not found", flush=True)

    # --- D) Captain sit-down camera animation -----------------------------
    # Two cameras:
    #   D1) Static cinematic overview camera (used for first 4 sec)
    #   D2) Animated "sit-down" camera (used for last 4 sec)
    #
    # We'll render the orbit + sit sequence as a single timeline using one
    # animated camera that orbits then descends into the captain chair.

    cam_data = bpy.data.cameras.new("HeroCam_Anim")
    cam_data.lens = 22
    cam = bpy.data.objects.new("HeroCam_Anim", cam_data)
    scene.collection.objects.link(cam)

    # Frame 1 (overview from upper aft-port)
    cam.location = (-3.5, 2.0, 2.05)
    cam.rotation_euler = (math.radians(72), 0, math.radians(-115))
    kf(cam, 1, location=cam.location, rotation_euler=cam.rotation_euler)

    # Frame 60 (slowly drifted to centre overview)
    cam.location = (0.0, 2.5, 1.95)
    cam.rotation_euler = (math.radians(78), 0, math.radians(-180))
    kf(cam, 60, location=cam.location, rotation_euler=cam.rotation_euler)

    # Frame 120 (approach captain chair from behind)
    cam.location = (1.6, 1.6, 1.85)
    cam.rotation_euler = (math.radians(80), 0, math.radians(-200))
    kf(cam, 120, location=cam.location, rotation_euler=cam.rotation_euler)

    # Frame 180 (sit down: lower to seated eye height ~1.45 m)
    cam.location = (1.5, 0.7, 1.45)
    cam.rotation_euler = (math.radians(85), 0, math.radians(-180))
    kf(cam, 180, location=cam.location, rotation_euler=cam.rotation_euler)

    # Frame 240 (settled in chair, looking forward to consoles)
    cam.location = (1.5, 0.7, 1.45)
    cam.rotation_euler = (math.radians(82), 0, math.radians(-180))
    kf(cam, 240, location=cam.location, rotation_euler=cam.rotation_euler)
    set_bezier_interp(cam)
    scene.camera = cam
    print(f"[anim] sit-down camera on {cam.name}", flush=True)

    # --- E) Alarm panel LED blink (if alarm panel material exists) --------
    alarm_mat = bpy.data.materials.get("mat_alert_glow")
    if alarm_mat and alarm_mat.use_nodes:
        bsdf = alarm_mat.node_tree.nodes.get("Principled BSDF")
        if bsdf and "Emission Strength" in bsdf.inputs:
            es = bsdf.inputs["Emission Strength"]
            es.default_value = 0
            es.keyframe_insert("default_value", frame=1)
            es.default_value = 8
            es.keyframe_insert("default_value", frame=15)
            es.default_value = 0
            es.keyframe_insert("default_value", frame=30)
            es.default_value = 8
            es.keyframe_insert("default_value", frame=45)
            es.default_value = 0
            es.keyframe_insert("default_value", frame=60)
            print("[anim] alarm LED blink keyframed", flush=True)

    # --- Render MP4 ------------------------------------------------------
    scene.render.engine = "BLENDER_EEVEE"
    if hasattr(scene.eevee, "taa_render_samples"):
        scene.eevee.taa_render_samples = 32
    if hasattr(scene.eevee, "use_raytracing"):
        scene.eevee.use_raytracing = True
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.look = "AgX - Medium High Contrast"
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 720

    # Blender 5.1 removed FFMPEG output; render PNG sequence and combine
    # with system ffmpeg afterwards.
    seq_dir = os.path.join(OUT_DIR, "anim_v5.0_frames")
    os.makedirs(seq_dir, exist_ok=True)
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGB"
    scene.render.filepath = os.path.join(seq_dir, "f")
    print(f"[render] starting animation render -> {seq_dir}", flush=True)
    bpy.ops.render.render(animation=True)
    print(f"[render] finished frames", flush=True)

    # Also render 4 keyframe PNGs (frame 1, 80, 160, 240) for inline preview
    scene.render.image_settings.file_format = "PNG"
    for fn in (1, 80, 160, 240):
        scene.frame_set(fn)
        scene.render.filepath = os.path.join(
            OUT_DIR, f"anim_v5.0_keyframe_f{fn:03d}.png")
        bpy.ops.render.render(write_still=True)
        print(f"[render] keyframe f{fn} saved", flush=True)

    bpy.ops.wm.save_as_mainfile(filepath=BLEND_OUT)
    print(f"[save] {BLEND_OUT}", flush=True)
    print("ALL_DONE", flush=True)


if __name__ == "__main__":
    main()
