def hex_distance(q1: int, r1: int, q2: int, r2: int) -> int:
    """
    Calculates the distance between two axial hex coordinates.
    """
    return (abs(q1 - q2) + abs(q1 + r1 - q2 - r2) + abs(r1 - r2)) // 2

def get_hex_ring(center_q: int, center_r: int, radius: int) -> list[tuple[int, int]]:
    """
    Returns a list of axial hex coordinates that form a ring at a given radius around a center hex.
    """
    if radius <= 0:
        return [(center_q, center_r)]
    
    results = []
    
    # Directions in axial coordinates
    # Ordered clockwise starting from East
    directions = [
        (1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)
    ]
    
    # Start by moving to the outer ring in one direction (e.g., direction 4)
    q = center_q + directions[4][0] * radius
    r = center_r + directions[4][1] * radius
    
    for dq, dr in directions:
        for _ in range(radius):
            results.append((q, r))
            q += dq
            r += dr
            
    return results

def get_hex_spiral(center_q: int, center_r: int, radius: int) -> list[tuple[int, int]]:
    """
    Returns a list of axial hex coordinates that form a solid spiral out to a given radius.
    """
    results = [(center_q, center_r)]
    for k in range(1, radius + 1):
        results.extend(get_hex_ring(center_q, center_r, k))
    return results
