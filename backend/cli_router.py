from backend.models import GameState, Unit
from backend.hex_math import hex_distance
from backend.economy import calculate_spt, calculate_tech_cost
from backend.combat import resolve_combat
import uuid

UNIT_STATS = {
    "warrior": {"hp": 10, "atk": 2, "def": 2, "range": 1, "native_z": 0},
    "archer": {"hp": 8, "atk": 2, "def": 1, "range": 2, "native_z": 0},
    "sentinel": {"hp": 15, "atk": 1, "def": 3, "range": 1, "native_z": 1},
}

def _handle_spawn(state: GameState, parts: list[str]) -> GameState:
    if len(parts) < 6: return state
    unit_type = parts[1]
    tribe = parts[2]
    try:
        q, r, z = int(parts[3]), int(parts[4]), int(parts[5])
    except ValueError:
        return state
        
    stats = UNIT_STATS.get(unit_type, UNIT_STATS["warrior"])
    
    unit_id = f"unit_{str(uuid.uuid4())[:8]}"
    new_unit = Unit(**{
        "id": unit_id,
        "type": unit_type,
        "tribe": tribe,
        "hp": stats["hp"],
        "max_hp": stats["hp"],
        "atk": stats["atk"],
        "def": stats["def"],
        "q": q,
        "r": r,
        "z": z,
        "is_veteran": False,
        "range": stats["range"],
        "kills": 0,
        "has_attacked": False
    })
    state.units[unit_id] = new_unit
    return state

def _handle_move(state: GameState, parts: list[str]) -> GameState:
    if len(parts) < 5: return state
    unit_id = parts[1]
    try:
        q, r, z = int(parts[2]), int(parts[3]), int(parts[4])
    except ValueError:
        return state
        
    unit = state.units.get(unit_id)
    if not unit: return state
    
    target_key = f"{q},{r},{z}"
    if target_key not in state.tiles: return state
    
    is_occupied = any(u.q == q and u.r == r and u.z == z for u in state.units.values())
    if is_occupied: return state
    
    dist = hex_distance(unit.q, unit.r, q, r)
    if dist > 1: return state
    
    if unit.z != z:
        source_key = f"{unit.q},{unit.r},{unit.z}"
        source_tile = state.tiles.get(source_key)
        target_tile = state.tiles.get(target_key)
        
        if {unit.z, z} == {0, -1}:
            if not ((source_tile and source_tile.biome == "cave_mouth") or (target_tile and target_tile.biome == "cave_mouth")):
                return state
        elif unit.z == 0 and z == 1:
            if not ((source_tile and source_tile.biome == "high_peak") or (target_tile and target_tile.biome == "high_peak")):
                return state
        elif unit.z == 1 and z == 0:
            pass # Drop-pod action, always allowed
        else:
            return state # Invalid z transition
            
    unit.q, unit.r, unit.z = q, r, z
    return state

def _handle_attack(state: GameState, parts: list[str]) -> GameState:
    if len(parts) < 3: return state
    attacker_id = parts[1]
    defender_id = parts[2]
    
    attacker = state.units.get(attacker_id)
    defender = state.units.get(defender_id)
    
    if attacker and defender and not attacker.has_attacked:
        dist = hex_distance(attacker.q, attacker.r, defender.q, defender.r)
        if dist <= attacker.range and attacker.z == defender.z:
            state = resolve_combat(state, attacker_id, defender_id)
            
    return state

def _handle_end_turn(state: GameState, parts: list[str]) -> GameState:
    if len(parts) < 2: return state
    tribe = parts[1]
    player = state.players.get(tribe)
    if player:
        player.total_cities = sum(1 for city in state.cities.values() if city.tribe == tribe)
        spt = calculate_spt(state, tribe)
        player.stars += spt
        
        for unit in state.units.values():
            if unit.tribe == tribe:
                unit.has_attacked = False
    return state

def _handle_research(state: GameState, parts: list[str]) -> GameState:
    if len(parts) < 3: return state
    tribe = parts[1]
    tech_name = parts[2]
    player = state.players.get(tribe)
    
    if player and tech_name not in player.techs:
        player.total_cities = sum(1 for city in state.cities.values() if city.tribe == tribe)
        base_cost = 5
        cost = calculate_tech_cost(base_cost, player.total_cities)
        
        if player.stars >= cost:
            player.stars -= cost
            player.techs.append(tech_name)
    return state

COMMAND_REGISTRY = {
    "spawn": _handle_spawn,
    "move": _handle_move,
    "attack": _handle_attack,
    "end_turn": _handle_end_turn,
    "research": _handle_research
}

def process_command(current_state: GameState, command_string: str) -> GameState:
    """
    Pure router function processing a CLI command using a Dispatcher Pattern.
    Returns a new GameState with the mutations applied.
    """
    parts = command_string.strip().split()
    if not parts:
        return current_state
        
    action = parts[0].lower()
    
    new_state = current_state.model_copy(deep=True)
    
    handler = COMMAND_REGISTRY.get(action)
    if handler:
        new_state = handler(new_state, parts)
            
    return new_state
