import pytest
from backend.hex_math import hex_distance, get_hex_ring, get_hex_spiral

def test_hex_distance():
    # Same tile
    assert hex_distance(0, 0, 0, 0) == 0
    # Adjacent tiles
    assert hex_distance(0, 0, 1, 0) == 1
    assert hex_distance(0, 0, 0, 1) == 1
    assert hex_distance(0, 0, -1, 1) == 1
    assert hex_distance(0, 0, -1, 0) == 1
    assert hex_distance(0, 0, 0, -1) == 1
    assert hex_distance(0, 0, 1, -1) == 1
    # Distant tiles
    assert hex_distance(-2, 1, 2, -1) == 4
    assert hex_distance(1, 1, -1, -1) == 4

def test_get_hex_ring():
    ring_0 = get_hex_ring(0, 0, 0)
    assert len(ring_0) == 1
    assert ring_0 == [(0, 0)]
    
    ring_1 = get_hex_ring(0, 0, 1)
    assert len(ring_1) == 6
    expected_ring_1 = {(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)}
    assert set(ring_1) == expected_ring_1
    
    ring_2 = get_hex_ring(0, 0, 2)
    assert len(ring_2) == 12

def test_get_hex_spiral():
    spiral_0 = get_hex_spiral(0, 0, 0)
    assert len(spiral_0) == 1
    
    spiral_1 = get_hex_spiral(0, 0, 1)
    assert len(spiral_1) == 7 # center + 6
    expected_spiral_1 = {(0, 0), (1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)}
    assert set(spiral_1) == expected_spiral_1
    
    spiral_2 = get_hex_spiral(0, 0, 2)
    assert len(spiral_2) == 19 # center + 6 + 12
