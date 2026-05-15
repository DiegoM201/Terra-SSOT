from backend.models import GameState, Unit
from backend.hex_math import hex_distance

def get_terrain_bonus(state: GameState, unit: Unit) -> float:
    # A simple mock for terrain bonus; later this can read from state.tiles
    # Example: tile.building == "Fortress" -> 1.5
    return 1.0

def calculate_damage(attacker: Unit, defender: Unit, defense_bonus: float) -> int:
    """
    Damage = (Attacker_ATK * (Current_HP / Max_HP)) / (Defender_DEF * Terrain_Bonus)
    """
    attacker_hp_ratio = attacker.hp / attacker.max_hp
    raw_damage = (attacker.atk * attacker_hp_ratio) / (defender.def_stat * defense_bonus)
    return round(raw_damage)

def resolve_combat(state: GameState, attacker_id: str, defender_id: str) -> GameState:
    new_state = state.model_copy(deep=True)
    attacker = new_state.units.get(attacker_id)
    defender = new_state.units.get(defender_id)
    
    if not attacker or not defender:
        return new_state
        
    attacker.has_attacked = True

    # 1. Base Attack
    def_bonus = get_terrain_bonus(new_state, defender)
    base_damage = calculate_damage(attacker, defender, def_bonus)
    
    defender.hp -= base_damage
    defender_survived = defender.hp > 0
    
    # 2. Retaliation
    if defender_survived:
        dist = hex_distance(attacker.q, attacker.r, defender.q, defender.r)
        # Check if attacker is within defender's range and same layer
        if dist <= defender.range and attacker.z == defender.z:
            att_bonus = get_terrain_bonus(new_state, attacker)
            retal_damage_raw = calculate_damage(defender, attacker, att_bonus)
            retal_damage = round(retal_damage_raw * 0.5)
            attacker.hp -= retal_damage
            
    # 3. Resolve Deaths and Veterancy
    attacker_dead = attacker.hp <= 0
    defender_dead = defender.hp <= 0
    
    if defender_dead:
        if not attacker_dead:
            attacker.kills += 1
            if attacker.kills == 3 and not attacker.is_veteran:
                attacker.is_veteran = True
                attacker.max_hp += 5
                attacker.hp += 5
                
            # Melee Sweep
            if attacker.range == 1:
                attacker.q = defender.q
                attacker.r = defender.r
                attacker.z = defender.z
                
        del new_state.units[defender_id]
        
    if attacker_dead:
        if not defender_dead:
            defender.kills += 1
            if defender.kills == 3 and not defender.is_veteran:
                defender.is_veteran = True
                defender.max_hp += 5
                defender.hp += 5
        del new_state.units[attacker_id]

    return new_state
