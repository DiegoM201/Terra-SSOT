import pytest
from backend.models import GameState, Tile
from backend.los_math import check_line_of_sight

def create_mock_state() -> GameState:
    return GameState(
        turn=1,
        tiles={},
        units={},
        cities={},
        players={}
    )

def test_los_sky_to_surface():
    state = create_mock_state()
    # Sky (z=1) has full vision of Surface (z=0)
    assert check_line_of_sight(state, 0, 0, 1, 0, 0, 0) == True

def test_los_surface_to_mantle():
    state = create_mock_state()
    # Surface (z=0) fails to see Mantle (z=-1) without Cave Mouth
    state.tiles["0,0,0"] = Tile(q=0, r=0, z=0, biome="Plains")
    assert check_line_of_sight(state, 0, 0, 0, 0, 0, -1) == False
    
    # With Cave Mouth
    state.tiles["0,0,0"] = Tile(q=0, r=0, z=0, biome="Cave Mouth")
    assert check_line_of_sight(state, 0, 0, 0, 0, 0, -1) == True

def test_los_mantle_to_surface():
    state = create_mock_state()
    # Mantle has zero vision outside
    assert check_line_of_sight(state, 0, 0, -1, 0, 0, 0) == False
    assert check_line_of_sight(state, 0, 0, -1, 0, 0, 1) == False

def test_los_same_layer_obstacles():
    state = create_mock_state()
    # Unit at 0,0 looking at 2,0. Intermediate is 1,0.
    state.tiles["1,0,0"] = Tile(q=1, r=0, z=0, biome="High Peak")
    
    # Adjacent (dist 1) is always seen, e.g. looking at the High Peak itself
    assert check_line_of_sight(state, 0, 0, 0, 1, 0, 0) == True
    
    # Blocked by High Peak (dist 2)
    assert check_line_of_sight(state, 0, 0, 0, 2, 0, 0) == False

    # Blocked by Forest
    state.tiles["1,0,0"] = Tile(q=1, r=0, z=0, biome="Forest")
    assert check_line_of_sight(state, 0, 0, 0, 2, 0, 0) == False
    
    # Not blocked by Plains
    state.tiles["1,0,0"] = Tile(q=1, r=0, z=0, biome="Plains")
    assert check_line_of_sight(state, 0, 0, 0, 2, 0, 0) == True
