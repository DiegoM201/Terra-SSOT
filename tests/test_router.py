import pytest
from backend.models import GameState, Tile
from backend.cli_router import process_command

def create_mock_state() -> GameState:
    state = GameState(
        turn=1,
        tiles={},
        units={},
        cities={},
        players={}
    )
    # Add some tiles for movement
    state.tiles["0,0,0"] = Tile(q=0, r=0, z=0, biome="Plains")
    state.tiles["1,0,0"] = Tile(q=1, r=0, z=0, biome="Plains")
    state.tiles["2,0,0"] = Tile(q=2, r=0, z=0, biome="Plains")
    return state

def test_spawn_and_move():
    initial_state = create_mock_state()
    
    # 1. Spawn unit
    state_after_spawn = process_command(initial_state, "spawn Archer Tribe_A 0 0 0")
    assert len(state_after_spawn.units) == 1
    
    # Ensure immutability of initial_state
    assert len(initial_state.units) == 0
    
    unit_id = list(state_after_spawn.units.keys())[0]
    unit = state_after_spawn.units[unit_id]
    assert unit.type == "Archer"
    assert unit.tribe == "Tribe_A"
    assert unit.q == 0 and unit.r == 0 and unit.z == 0
    
    # 2. Valid move
    state_after_move = process_command(state_after_spawn, f"move {unit_id} 1 0 0")
    moved_unit = state_after_move.units[unit_id]
    assert moved_unit.q == 1 and moved_unit.r == 0 and moved_unit.z == 0
    
    # Ensure immutability of state_after_spawn
    assert state_after_spawn.units[unit_id].q == 0
    
    # 3. Invalid move (occupied)
    state_after_spawn_2 = process_command(state_after_move, "spawn Warrior Tribe_B 2 0 0")
    warrior_id = list(state_after_spawn_2.units.keys())[1] # The new one
    
    # Move archer to warrior's spot
    state_failed_move = process_command(state_after_spawn_2, f"move {unit_id} 2 0 0")
    assert state_failed_move.units[unit_id].q == 1 # Did not move
    
    # 4. Invalid move (no tile)
    state_no_tile_move = process_command(state_after_move, f"move {unit_id} 10 10 0")
    assert state_no_tile_move.units[unit_id].q == 1 # Did not move
