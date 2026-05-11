# BridgeVR Sky Clouds v1.0 — Standalone Asset

Phần clouds tách riêng ra khỏi `bridge_v9.0_pro_clouds.blend`. Có thể import vào Blender scene khác hoặc Unity project khác để re-use.

## Files

| File | Mục đích |
|---|---|
| `BridgeVR_Sky_Clouds_v1.0.blend` | 5 cloud billboards + procedural alpha material + drift animations |
| `BridgeVR_Sky_Clouds_v1.0.glb` | Unity-importable glTF (20 KB) |
| `cloud_preview.png` | Preview render (mặt sau plane = trống) |

## Nội dung

- **5 cloud planes** ở các vị trí scattered laterally, kích thước 70-120m × 30-45m, cao 22-33m
- **Procedural alpha material** với Voronoi + Noise multiply mask + Radial falloff cho organic cumulus shape
- **Drift animation** keyframed 240 frames (X+8..17m, mỗi cloud hơi khác để có parallax)
- **Shadow casting OFF** — clouds không tạo bóng xuống bridge

## Sử dụng

### Blender
```
File → Append → BridgeVR_Sky_Clouds_v1.0.blend → Collection → BR_Sky_Clouds
```
Collection nguyên vẹn animations + material.

### Unity
```
Drag BridgeVR_Sky_Clouds_v1.0.glb vào Assets/Sky/
Drop prefab vào scene, position trên cao
Lưu ý: GLB không support shader alpha procedural như Blender;
Unity sẽ cần shader replacement (URP Lit Transparent + custom alpha texture)
hoặc bake cloud alpha về PNG để dùng làm decal
```

### Lưu ý kỹ thuật

- **Cloud planes có rotation X=90°** → mặt trước (visible) hướng về Y negative
- Camera phải ở **Y > cloud Y** mới thấy cloud (do mặt sau plane = alpha transparent)
- Cumulus shape là **procedural**, không có texture file đi kèm
- Trong VR Unity runtime, có thể replace bằng VFX Graph particles cho perf tốt hơn

## Engineering note

Đây là **billboard alpha approach** thay vì volumetric VDB. Tradeoff:

| | Billboard alpha (chosen) | Volumetric VDB |
|---|---|---|
| Render speed | Nhanh (vài giây/frame) | Chậm (1-10s/frame) |
| Mobile VR (Quest 3) | OK | Không khả thi |
| Visual quality | Stylized, đẹp với alpha noise | Photoreal, real lighting |
| File size | 20 KB GLB | 90+ MB VDB |

Cho VR LMS giáo dục → **billboard winning** about performance + simplicity.

## License

- Procedural material: project original
- Geometry: project original (Blender primitives)
- Free to use trong Maritime VR LMS scope.
