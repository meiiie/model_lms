# Bridge Reference Handoff - 2026-05-10

Purpose: answer the current VR bridge asset request with a project-local reference
pack for modeling/import review.

## 1. Bridge Photos / References

Real photos of a specific VIMARU or partner vessel are not present in this
workspace. The files in `01_bridge_ai_references/` are AI-generated
photorealistic concept references made with the built-in `image_gen` tool, so
they should be treated as modeling direction, not as real vessel evidence.

Generated bridge angles:

- `bridge_front_console_ai_reference.png`
- `bridge_side_layout_ai_reference.png`
- `bridge_ceiling_detail_ai_reference.png`
- `bridge_floor_console_bases_ai_reference.png`
- `bridge_window_detail_ai_reference.png`
- `existing_imagegen_bridge_cockpit_reference_v1.png`

Quick review sheet:

- `bridge_ai_references_contact_sheet.png`

If VIMARU or a partner supplies real bridge photos later, place them next to
these files and mark the AI files as secondary concept references.

## 2. Static ECDIS / Radar UI

Recommended label choice for the current prototype: generic training UI, no
Transas/Furuno/JRC/Kongsberg branding. This avoids implying certified equipment
or using vendor UI screenshots without permission.

Static screen textures copied from the active cockpit asset:

- `02_screen_ui_static/generic_training_ecdis_chart_v1.png`
- `02_screen_ui_static/generic_training_radar_ppi_v1.png`
- `screen_ui_static_contact_sheet.png`

## 3. Existing Model Previews

Preview images copied from existing model render folders so the VR/import team
can verify quality before import:

- `03_existing_model_previews/02_Ship_Wheel_preview.png`
- `03_existing_model_previews/03_Magnetic_Compass_preview.png`
- `03_existing_model_previews/04_Engine_Telegraph_preview.png`
- `03_existing_model_previews/11_Bridge_Alarm_Panel_preview.png`
- `03_existing_model_previews/06_Bridge_Cabin_helmsman_POV_preview.png`
- `03_existing_model_previews/06_Bridge_Cabin_topdown_layout_preview.png`
- `03_existing_model_previews/12_Modern_Bridge_Cockpit_preview.png`
- `existing_model_previews_contact_sheet.png`

Source model folders:

- `02_Ship_Wheel/`
- `03_Magnetic_Compass/`
- `04_Engine_Telegraph/`
- `11_Bridge_Alarm_Panel/`

## 4. Vessel Type

Use the current project vessel type: Handysize Bulk Carrier / cargo bulker.

Project evidence:

- `10_Ship_Hull/README.md` identifies the ship class as Handysize Bulk Carrier.
- The master library README lists `10_Ship_Hull` as a Handysize Bulk Carrier.
- Bridge layout should therefore be a commercial cargo bridge, not container,
  tanker, cruise, or luxury yacht styling.

## ImageGen Prompt Summary

The generated bridge references used these constraints:

- Commercial cargo ship wheelhouse for a Handysize bulk carrier training
  simulator.
- Angles: front-on console, side layout, ceiling detail, floor/console bases,
  and forward window detail.
- No people, no real vessel name, no vendor logos, no proprietary readable UI,
  no watermark, and no luxury yacht styling.
