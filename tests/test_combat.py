import pytest
from backend.models import GameState, Unit
from backend.combat import calculate_damage, resolve_combat
from backend.cli_router import process_command

def test_calculate_damage():
    attacker = Unit(id="a", type="Warrior", tribe="A", hp=10, max_hp=10, atk=2, def_stat=2, q=0, r=0, z=0)
    defender = Unit(id="b", type="Warrior", tribe="B", hp=10, max_hp=10, atk=2, def_stat=2, q=1, r=0, z=0)
    
    damage = calculate_damage(attacker, defender, 1.0)
    assert damage == 1 # (2 * 1) / (2 * 1) = 1

    # Damaged attacker
    attacker.hp = 6
    damage_weak = calculate_damage(attacker, defender, 1.0)
    assert damage_weak == 1 # (2 * 0.6) / 2 = 0.6 -> round(0.6) = 1

def test_retaliation_damage():
    state = GameState(turn=1, tiles={}, units={}, cities={}, players={})
    state.units["a"] = Unit(id="a", type="Attacker", tribe="A", hp=10, max_hp=10, atk=10, def_stat=2, q=0, r=0, z=0, range=1)
    state.units["b"] = Unit(id="b", type="Defender", tribe="B", hp=10, max_hp=10, atk=10, def_stat=2, q=1, r=0, z=0, range=1)
    
    new_state = resolve_combat(state, "a", "b")
    # Base damage: (10 * 1) / 2 = 5. Defender HP = 5.
    # Retaliation base: (10 * 0.5) / 2 = 2.5. Halved = 1.25. Round = 1.
    assert new_state.units["b"].hp == 5
    assert new_state.units["a"].hp == 9
    assert new_state.units["a"].has_attacked == True

def test_melee_sweep():
    state = GameState(turn=1, tiles={}, units={}, cities={}, players={})
    state.units["a"] = Unit(id="a", type="Melee", tribe="A", hp=10, max_hp=10, atk=20, def_stat=2, q=0, r=0, z=0, range=1)
    state.units["b"] = Unit(id="b", type="Victim", tribe="B", hp=1, max_hp=10, atk=2, def_stat=2, q=1, r=0, z=0, range=1)
    
    new_state = resolve_combat(state, "a", "b")
    assert "b" not in new_state.units
    assert new_state.units["a"].kills == 1
    # Melee sweep: 'a' should be at 'b's coordinates (1,0,0)
    assert new_state.units["a"].q == 1
    assert new_state.units["a"].r == 0

def test_veterancy():
    state = GameState(turn=1, tiles={}, units={}, cities={}, players={})
    state.units["a"] = Unit(id="a", type="Melee", tribe="A", hp=10, max_hp=10, atk=20, def_stat=2, q=0, r=0, z=0, range=1, kills=2)
    state.units["b"] = Unit(id="b", type="Victim", tribe="B", hp=1, max_hp=10, atk=2, def_stat=2, q=1, r=0, z=0, range=1)
    
    new_state = resolve_combat(state, "a", "b")
    assert "b" not in new_state.units
    # 3rd kill -> veteran
    assert new_state.units["a"].kills == 3
    assert new_state.units["a"].is_veteran == True
    assert new_state.units["a"].max_hp == 15
    assert new_state.units["a"].hp == 15 # Because 10 + 5.

def test_router_attack_command():
    state = GameState(turn=1, tiles={}, units={}, cities={}, players={})
    state.units["a"] = Unit(id="a", type="Attacker", tribe="A", hp=10, max_hp=10, atk=10, def_stat=2, q=0, r=0, z=0, range=1)
    state.units["b"] = Unit(id="b", type="Defender", tribe="B", hp=10, max_hp=10, atk=10, def_stat=2, q=1, r=0, z=0, range=1)
    
    new_state = process_command(state, "attack a b")
    assert new_state.units["a"].has_attacked == True
    assert new_state.units["b"].hp == 5
    
    # Second attack should be ignored
    new_state_2 = process_command(new_state, "attack a b")
    assert new_state_2.units["b"].hp == 5
