from backend.models import GameState, Unit
from backend.hex_math import hex_distance
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
        # spawn <unit_type> <tribe> <q> <r> <z>
        unit_type = parts[1]
        tribe = parts[2]
        try:
            q = int(parts[3])
            r = int(parts[4])
            z = int(parts[5])
        except ValueError:
            return new_state # Invalid coordinates
            
        unit_id = f"unit_{str(uuid.uuid4())[:8]}"
        
        # Standard base stats for scaffolding
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
            "is_veteran": False
        })
        new_state.units[unit_id] = new_unit
        
    elif action == "move" and len(parts) >= 5:
        # move <unit_id> <q> <r> <z>
        unit_id = parts[1]
        try:
            q = int(parts[2])
            r = int(parts[3])
            z = int(parts[4])
        except ValueError:
            return new_state
            
        unit = new_state.units.get(unit_id)
        if not unit:
            return new_state # Unit not found
            
        target_key = f"{q},{r},{z}"
        
        # Validation 1: Target tile exists
        if target_key not in new_state.tiles:
            return new_state
            
        # Validation 2: Target tile unoccupied
        is_occupied = any(u.q == q and u.r == r and u.z == z for u in new_state.units.values())
        if is_occupied:
            return new_state
            
        # Validation 3: Distance bounds (base unit move is 1 hex for now)
        dist = hex_distance(unit.q, unit.r, q, r)
        
        # Assume moving on same Z layer
        if unit.z == z and dist <= 1:
            unit.q = q
            unit.r = r
            unit.z = z
            
    return new_state
