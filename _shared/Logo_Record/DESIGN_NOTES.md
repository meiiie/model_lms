# Logo Record — Design Notes

**Designer:** Maritime VR LMS project (Claude collaboration)
**Date:** 2026-05-11
**Brief:** Replace generic "play" icon with a sophisticated, mathematically rigorous record button. Red center indicates active recording.

## Design Philosophy

Thay vì play-icon (tam giác) generic, logo này thuộc trường phái **flat geometric / sacred geometry** giống NASA insignia, Twitter rebrand, Mercedes-Benz star. Hai key principles:

1. **Cấu trúc toán học chặt chẽ** — không "by eye"
2. **Multi-layer meaning** — hình thức không chỉ trang trí mà mang ý nghĩa

## Composition & Math

### Layer stack (concentric, top-down ortho view)

```
L5  Solid red disc      (record signal)        ← center, eye-catch
L4  Red 8-petal rosette (compass cardinal)     ← maritime/navigation
L3  Navy negative space (breathing ring)       ← contrast separator
L2  White 12-petal rosette (clock/zodiac)      ← time, cycle, rhythm
L1  Navy square         (authority frame)      ← formal context
```

### Rotational symmetry (intentional choice)

- **Outer ring: 12-fold** — clock hours / zodiac signs / time / completeness
- **Inner ring: 8-fold** — compass cardinal + intercardinal directions (N, NE, E, SE, S, SW, W, NW)
- The 12/8 contrast creates **subtle visual rhythm** without competing — both are highly composite numbers (12 = 2²·3, 8 = 2³), so they're stable and read as "ordered" not "random"

### Golden ratio nesting (φ = 1.618)

```
total_outer_extent = canvas * 0.92             (margin breathing room)
outer_R     = total_outer_extent / (1 + sin(π/12))
outer_lobe  = outer_R · sin(π/12)              (tangent-touching lobes)
inner_navy_R = (outer_R - outer_lobe) / φ      (golden ratio gap)
red_rose_R   = inner_navy_R · 0.92
red_lobe     = red_rose_R · sin(π/8)
red_disc_R   = red_rose_R / φ                  (golden ratio inner dot)
```

Lobes touch tangentially trên ring (not overlap, not gap) — produces clean scallop edge.

## Color palette

Each color chosen for **semantic + technical** reasons:

| Color | Hex | Linear RGB | Semantic |
|-------|-----|-----------|----------|
| Maritime Navy | `#0A2540` | 0.005, 0.022, 0.054 | Ocean depth, authority, professionalism. |
| Broadcast Red | `#C8102E` | 0.580, 0.005, 0.026 | Pantone 186 - TV/film "record on" since 1960s. |
| Pure White | `#FFFFFF` | 1.0, 1.0, 1.0 | Navigation lights, clarity. |

## Dual-scale recognition

| Size | Reads as |
|------|----------|
| 1024px | Maritime authority seal / naval record stamp |
| 256px | Compass rose / formal record button |
| 64px | Record button with flower motif |
| 32px | Red dot with subtle ornament (recognizable record icon) |

## Output formats

| File | Use |
|---|---|
| `logo_record_1024.png` | hero / website header |
| `logo_record_512.png` | social media |
| `logo_record_256.png` | thumbnail |
| `logo_record_128.png` | macOS dock |
| `logo_record_64.png` | toolbar |
| `logo_record_32.png` | favicon |
| `logo_record_transparent_*.png` | overlay on dark/light bg |
| `logo_design.blend` | re-edit |

## Reproducibility

```bash
"C:/Program Files/Blender Foundation/Blender 5.1/blender.exe" \
  --background --factory-startup --python "_design_logo.py"
```

Tinh chỉnh: edit `n_outer`, `n_inner`, hex codes ở đầu script.
