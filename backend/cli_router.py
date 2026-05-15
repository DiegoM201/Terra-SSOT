from backend.models import GameState, Unit
from backend.hex_math import hex_distance
from backend.economy import calculate_spt, calculate_tech_cost
from backend.combat import resolve_combat
import uuid

def process_command(current_state: GameState, command_string: str) -> GameState:
    """
    Pure router function processing a CLI command.
    Returns a new GameState with the mutations applied.
    """
    parts = command_string.strip().split()
    if not parts:
        return current_state
        
    action = parts[0].lower()
    
    # Use deep copy to ensure immutability and purity
    new_state = current_state.model_copy(deep=True)
    
    if action == "spawn" and len(parts) >= 6:
        unit_type = parts[1]
        tribe = parts[2]
        try:
            q = int(parts[3])
            r = int(parts[4])
            z = int(parts[5])
        except ValueError:
            return new_state
            
        unit_id = f"unit_{str(uuid.uuid4())[:8]}"
        hp, atk, def_stat = 10, 2, 2
        
        new_unit = Unit(**{
            "id": unit_id,
            "type": unit_type,
            "tribe": tribe,
            "hp": hp,
            "max_hp": hp,
            "atk": atk,
            "def": def_stat,
            "q": q,
            "r": r,
            "z": z,
            "is_veteran": False,
            "range": 1,
            "kills": 0,
            "has_attacked": False
        })
        new_state.units[unit_id] = new_unit
        
    elif action == "move" and len(parts) >= 5:
        unit_id = parts[1]
        try:
            q = int(parts[2])
            r = int(parts[3])
            z = int(parts[4])
        except ValueError:
            return new_state
            
        unit = new_state.units.get(unit_id)
        if not unit:
            return new_state
            
        target_key = f"{q},{r},{z}"
        
        if target_key not in new_state.tiles:
            return new_state
            
        is_occupied = any(u.q == q and u.r == r and u.z == z for u in new_state.units.values())
        if is_occupied:
            return new_state
            
        dist = hex_distance(unit.q, unit.r, q, r)
        if unit.z == z and dist <= 1:
            unit.q = q
            unit.r = r
            unit.z = z

    elif action == "attack" and len(parts) >= 3:
        attacker_id = parts[1]
        defender_id = parts[2]
        
        attacker = new_state.units.get(attacker_id)
        defender = new_state.units.get(defender_id)
        
        if attacker and defender and not attacker.has_attacked:
            dist = hex_distance(attacker.q, attacker.r, defender.q, defender.r)
            if dist <= attacker.range and attacker.z == defender.z:
                new_state = resolve_combat(new_state, attacker_id, defender_id)

    elif action == "end_turn" and len(parts) >= 2:
        tribe = parts[1]
        player = new_state.players.get(tribe)
        if player:
            player.total_cities = sum(1 for city in new_state.cities.values() if city.tribe == tribe)
            spt = calculate_spt(new_state, tribe)
            player.stars += spt
            
            # Reset attacks for tribe
            for unit in new_state.units.values():
                if unit.tribe == tribe:
                    unit.has_attacked = False

    elif action == "research" and len(parts) >= 3:
        tribe = parts[1]
        tech_name = parts[2]
        player = new_state.players.get(tribe)
        
        if player and tech_name not in player.techs:
            player.total_cities = sum(1 for city in new_state.cities.values() if city.tribe == tribe)
            base_cost = 5 # Mock tier 1 base cost
            cost = calculate_tech_cost(base_cost, player.total_cities)
            
            if player.stars >= cost:
                player.stars -= cost
                player.techs.append(tech_name)
            
    return new_state
