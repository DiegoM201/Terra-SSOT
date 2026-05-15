import pytest
from backend.models import GameState, Player, City
from backend.cli_router import process_command
from backend.economy import calculate_spt, calculate_tech_cost

def test_calculate_tech_cost():
    assert calculate_tech_cost(5, 1) == 7
    assert calculate_tech_cost(10, 3, 3) == 19

def test_calculate_spt():
    state = GameState(turn=1, tiles={}, units={}, cities={}, players={})
    state.players["Tribe_A"] = Player(tribe="Tribe_A", stars=0, total_cities=1)
    
    # Base is 2
    assert calculate_spt(state, "Tribe_A") == 2
    
    # Add a level 2 city
    state.cities["city_1"] = City(id="city_1", name="Rome", tribe="Tribe_A", q=0, r=0, z=0, level=2, population=1, max_population=2)
    assert calculate_spt(state, "Tribe_A") == 4

def test_end_turn_and_research():
    state = GameState(turn=1, tiles={}, units={}, cities={}, players={})
    state.players["Tribe_A"] = Player(tribe="Tribe_A", stars=5, total_cities=1)
    state.cities["city_1"] = City(id="city_1", name="Rome", tribe="Tribe_A", q=0, r=0, z=0, level=1, population=1, max_population=2)
    
    # end_turn Tribe_A -> +3 SPT (base 2 + 1 level). Starts with 5, becomes 8.
    new_state = process_command(state, "end_turn Tribe_A")
    assert new_state.players["Tribe_A"].stars == 8
    
    # research Tribe_A Farming
    # cost = 5 + (1 * 2) = 7. 8 >= 7.
    new_state_2 = process_command(new_state, "research Tribe_A Farming")
    assert "Farming" in new_state_2.players["Tribe_A"].techs
    assert new_state_2.players["Tribe_A"].stars == 1 # 8 - 7
    
    # try researching without enough stars
    # Cost again 7. Only 1 star.
    new_state_3 = process_command(new_state_2, "research Tribe_A Mining")
    assert "Mining" not in new_state_3.players["Tribe_A"].techs
    assert new_state_3.players["Tribe_A"].stars == 1
