import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps


def parse_size(value: str) -> tuple[int, int]:
    if "x" not in value.lower():
        raise argparse.ArgumentTypeError("Size must be WIDTHxHEIGHT, for example 2048x1152")
    width, height = value.lower().split("x", 1)
    return int(width), int(height)


def save_depth_assets(input_image: Path, output_dir: Path, size: tuple[int, int]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    source = Image.open(input_image).convert("RGB")
    albedo = ImageOps.fit(source, size, method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))

    gray = ImageOps.grayscale(albedo)
    gray_arr = np.asarray(gray, dtype=np.float32) / 255.0

    edge = gray.filter(ImageFilter.FIND_EDGES)
    edge = ImageEnhance.Contrast(edge).enhance(2.2).filter(ImageFilter.GaussianBlur(radius=1.2))
    edge_arr = np.asarray(edge, dtype=np.float32) / 255.0

    h, w = gray_arr.shape
    vertical_near = np.linspace(0.08, 1.0, h, dtype=np.float32)[:, None]
    dark_foreground = 1.0 - gray_arr
    local_detail = np.clip(edge_arr * 1.25, 0.0, 1.0)

    # A robust fallback depth prior for cockpit images:
    # bottom/foreground console is nearer, high-contrast edges carry relief,
    # bright sky/window regions are suppressed to avoid protruding glass.
    height_arr = 0.52 * vertical_near + 0.30 * local_detail + 0.18 * dark_foreground
    height_arr = np.clip(height_arr, 0.0, 1.0)
    height_img = Image.fromarray(np.uint8(height_arr * 255.0), mode="L")
    height_img = ImageOps.autocontrast(height_img, cutoff=1).filter(ImageFilter.GaussianBlur(radius=0.65))

    height_final = np.asarray(height_img, dtype=np.float32) / 255.0
    dy, dx = np.gradient(height_final)
    normal_strength = 5.0
    nx = -dx * normal_strength
    ny = -dy * normal_strength
    nz = np.ones_like(height_final)
    length = np.sqrt(nx * nx + ny * ny + nz * nz)
    nx /= length
    ny /= length
    nz /= length
    normal = np.stack(
        [
            (nx * 0.5 + 0.5) * 255.0,
            (ny * 0.5 + 0.5) * 255.0,
            (nz * 0.5 + 0.5) * 255.0,
        ],
        axis=-1,
    ).astype(np.uint8)

    albedo_path = output_dir / "bridge_cockpit_albedo_2048.png"
    height_path = output_dir / "bridge_cockpit_height_2048.png"
    normal_path = output_dir / "bridge_cockpit_normal_2048.png"

    albedo.save(albedo_path)
    height_img.save(height_path)
    Image.fromarray(normal, mode="RGB").save(normal_path)

    print(f"Saved {albedo_path}")
    print(f"Saved {height_path}")
    print(f"Saved {normal_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate albedo/height/normal texture set from a cockpit reference image.")
    parser.add_argument("input_image", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--size", type=parse_size, default=(2048, 1152))
    args = parser.parse_args()

    save_depth_assets(args.input_image.resolve(), args.output_dir.resolve(), args.size)


if __name__ == "__main__":
    main()
