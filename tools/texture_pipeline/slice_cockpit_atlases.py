from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image


SCREEN_QUADRANTS = {
    "screen_radar_v1.png": (0, 0),
    "screen_ecdis_chart_v1.png": (1, 0),
    "screen_engine_monitor_v1.png": (0, 1),
    "screen_comms_status_v1.png": (1, 1),
}

SURFACE_QUADRANTS = {
    "surface_carpet_navy_v1.png": (0, 0),
    "surface_ceiling_panels_v1.png": (1, 0),
    "surface_black_metal_v1.png": (0, 1),
    "surface_warm_wood_v1.png": (1, 1),
}

INTERACTIVE_QUADRANTS = {
    "interactive_black_rubber_v1.png": (0, 0),
    "interactive_brushed_stainless_v1.png": (1, 0),
    "interactive_red_bakelite_v1.png": (0, 1),
    "interactive_telegraph_dial_v1.png": (1, 1),
}

STRUCTURE_QUADRANTS = {
    "structure_nonslip_floor_v1.png": (0, 0),
    "structure_ceiling_panels_v1.png": (1, 0),
    "structure_dark_steel_pillar_v1.png": (0, 1),
    "structure_brushed_rail_wiper_v1.png": (1, 1),
}


def crop_quadrants(source: Path, target_dir: Path, mapping: dict[str, tuple[int, int]]) -> None:
    image = Image.open(source).convert("RGB")
    width, height = image.size
    half_w = width // 2
    half_h = height // 2
    target_dir.mkdir(parents=True, exist_ok=True)

    for filename, (col, row) in mapping.items():
        left = col * half_w
        upper = row * half_h
        crop = image.crop((left, upper, left + half_w, upper + half_h))
        crop = crop.resize((1024, 1024), Image.Resampling.LANCZOS)
        crop.save(target_dir / filename, optimize=True)


def main(repo_root: Path) -> None:
    model_dir = repo_root / "12_Modern_Bridge_Cockpit"
    source_dir = model_dir / "textures" / "source"
    output_dir = model_dir / "textures"

    crop_quadrants(
        source_dir / "screen_ui_atlas_v1.png",
        output_dir / "screens",
        SCREEN_QUADRANTS,
    )
    crop_quadrants(
        source_dir / "surface_material_atlas_v1.png",
        output_dir / "surfaces",
        SURFACE_QUADRANTS,
    )
    crop_quadrants(
        source_dir / "interactive_material_atlas_v1.png",
        output_dir / "interactive",
        INTERACTIVE_QUADRANTS,
    )
    crop_quadrants(
        source_dir / "structure_material_atlas_v1.png",
        output_dir / "structure",
        STRUCTURE_QUADRANTS,
    )


if __name__ == "__main__":
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[2]
    main(root)
