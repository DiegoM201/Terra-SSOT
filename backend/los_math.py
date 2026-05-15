from backend.models import GameState
from backend.hex_math import hex_distance

def cube_lerp(a: tuple[float, float, float], b: tuple[float, float, float], t: float) -> tuple[float, float, float]:
    return (a[0] + (b[0] - a[0]) * t,
            a[1] + (b[1] - a[1]) * t,
            a[2] + (b[2] - a[2]) * t)

def cube_round(c: tuple[float, float, float]) -> tuple[int, int]:
    rx = round(c[0])
    ry = round(c[1])
    rz = round(c[2])
    x_diff = abs(rx - c[0])
    y_diff = abs(ry - c[1])
    z_diff = abs(rz - c[2])
    if x_diff > y_diff and x_diff > z_diff:
        rx = -ry - rz
    elif y_diff > z_diff:
        ry = -rx - rz
    else:
        rz = -rx - ry
    return (int(rx), int(ry))

def get_hex_line(q1: int, r1: int, q2: int, r2: int) -> list[tuple[int, int]]:
    dist = hex_distance(q1, r1, q2, r2)
    if dist == 0:
        return [(q1, r1)]
    
    results = []
    # Nudge to avoid exact integer coordinates causing inconsistent rounding
    a = (q1 + 1e-6, r1 + 1e-6, -q1 - r1 - 2e-6)
    b = (q2 + 1e-6, r2 + 1e-6, -q2 - r2 - 2e-6)
    
    for i in range(dist + 1):
        t = i / max(1, dist)
        c = cube_lerp(a, b, t)
        results.append(cube_round(c))
    return results

def check_line_of_sight(state: GameState, q1: int, r1: int, z1: int, q2: int, r2: int, z2: int) -> bool:
    dist = hex_distance(q1, r1, q2, r2)
    
    # Adjacent units can always see each other (assuming layer vision allows it)
    is_adjacent_or_same = dist <= 1

    # Cross-layer rules
    if z1 != z2:
        if z1 == 1 and z2 == 0:
            return True
        if z1 == 0 and z2 == -1:
            tile_key = f"{q1},{r1},{z1}"
            tile = state.tiles.get(tile_key)
            if tile and tile.biome == "Cave Mouth":
                pass # continue to evaluate horizontal line of sight below
            else:
                return False
        if z1 == -1 and (z2 == 0 or z2 == 1):
            return False
            
    # Same layer or valid cross-layer observation into that layer
    # For horizontal LOS, we evaluate obstacles on target's layer z2.
    line = get_hex_line(q1, r1, q2, r2)
    
    # Exclude the start tile and the target tile (target tile doesn't block vision to itself)
    if len(line) > 2:
        intermediate_hexes = line[1:-1]
        for hq, hr in intermediate_hexes:
            tile_key = f"{hq},{hr},{z2}"
            tile = state.tiles.get(tile_key)
            if tile:
                if tile.biome in ["High Peak", "Forest"]:
                    return False
    return True
