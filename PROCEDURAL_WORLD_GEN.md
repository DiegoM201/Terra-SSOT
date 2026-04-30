# TECHNICAL SPEC: TRIPLE-LAYER GENERATION
**Geometry**: Flat Axial Hex Grid.

## 1. THE STACKED STATE
State is stored as: `Grid[(q, r)] = { -1: MantleTile, 0: SurfaceTile, 1: SkyTile }`.

## 2. BIOME GENERATION
- **Layer 0 (Surface)**: Simplex Noise ($N \geq 0.45$ = Land).
- **Layer 1 (Sky)**: Sparse Noise ($N \geq 0.8$ = Floating Island).
- **Layer -1 (Mantle)**: Cellular Automata generated tunnels. 90% "Solid Rock" (Blocked), 10% "Cavern Path."

## 3. ALIGNMENT RULES
- **Shadows**: If Layer 1 is Land, Layer 0 below is "Shadowed" (-1 SPT).
- **Entrances**: "Cave Mouths" spawn on Layer 0 where Layer -1 paths exist. "High Peaks" spawn on Layer 0 where Layer 1 islands exist.