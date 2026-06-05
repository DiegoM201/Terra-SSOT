import json
import time
import os
from backend.models import GameState, Tile, Unit, City, Player, TribeHeuristics
from backend.cli_router import process_command

def load_game_state(path: str) -> tuple[GameState, dict]:
    with open(path, "r") as f:
        raw_data = json.load(f)
        
    turn = raw_data["game_metadata"]["turn"]
    
    # Load tiles
    tiles = {}
    for layer_name, layer_data in raw_data["layers"].items():
        z = layer_data["z"]
        for coordinate_str, tile_data in layer_data["tiles"].items():
            q, r = map(int, coordinate_str.split(","))
            key = f"{q},{r},{z}"
            tiles[key] = Tile(
                q=q,
                r=r,
                z=z,
                biome=tile_data["type"],
                resource=tile_data.get("resource"),
                building=tile_data.get("building")
            )
            
    # Load units
    units = {}
    for unit_id, unit_data in raw_data.get("units", {}).items():
        # Handle field alias for def
        if "def" in unit_data:
            unit_data["def_stat"] = unit_data.pop("def")
        units[unit_id] = Unit(**unit_data)
        
    # Load cities
    cities = {}
    for city_id, city_data in raw_data.get("cities", {}).items():
        cities[city_id] = City(**city_data)
        
    # Load players
    players = {}
    for tribe_name, tribe_data in raw_data.get("tribes", {}).items():
        # Count cities owned by this tribe
        total_cities = sum(1 for city in cities.values() if city.tribe == tribe_name)
        players[tribe_name] = Player(
            tribe=tribe_name,
            stars=tribe_data["resources"]["stars"],
            techs=tribe_data["techs"],
            total_cities=max(1, total_cities),
            heuristics=TribeHeuristics()
        )
        
    state = GameState(
        turn=turn,
        tiles=tiles,
        units=units,
        cities=cities,
        players=players
    )
    return state, raw_data

def save_game_state(state: GameState, original_raw_data: dict, output_path: str):
    original_raw_data["game_metadata"]["turn"] = state.turn
    
    # Save tiles
    for key, tile in state.tiles.items():
        q, r, z = map(int, key.split(","))
        layer_name = None
        for name, layer_data in original_raw_data["layers"].items():
            if layer_data["z"] == z:
                layer_name = name
                break
        if layer_name:
            coord_key = f"{q},{r}"
            if coord_key in original_raw_data["layers"][layer_name]["tiles"]:
                original_raw_data["layers"][layer_name]["tiles"][coord_key]["type"] = tile.biome
                if tile.resource:
                    original_raw_data["layers"][layer_name]["tiles"][coord_key]["resource"] = tile.resource
                else:
                    original_raw_data["layers"][layer_name]["tiles"][coord_key].pop("resource", None)
                if tile.building:
                    original_raw_data["layers"][layer_name]["tiles"][coord_key]["building"] = tile.building
                else:
                    original_raw_data["layers"][layer_name]["tiles"][coord_key].pop("building", None)
            else:
                tile_dict = {"type": tile.biome, "properties": []}
                if tile.resource:
                    tile_dict["resource"] = tile.resource
                if tile.building:
                    tile_dict["building"] = tile.building
                original_raw_data["layers"][layer_name]["tiles"][coord_key] = tile_dict

    # Save units
    original_raw_data["units"] = {}
    for unit_id, unit in state.units.items():
        original_raw_data["units"][unit_id] = unit.model_dump(by_alias=True)

    # Save cities
    original_raw_data["cities"] = {}
    for city_id, city in state.cities.items():
        original_raw_data["cities"][city_id] = city.model_dump()

    # Save players/tribes
    original_raw_data["tribes"] = {}
    for tribe_name, player in state.players.items():
        original_raw_data["tribes"][tribe_name] = {
            "score": original_raw_data.get("tribes", {}).get(tribe_name, {}).get("score", 0),
            "techs": player.techs,
            "resources": {
                "stars": player.stars,
                "faith": original_raw_data.get("tribes", {}).get(tribe_name, {}).get("resources", {}).get("faith", 0)
            }
        }
        
    with open(output_path, "w") as f:
        json.dump(original_raw_data, f, indent=2)

def log_transition(command: str, old_state: GameState, new_state: GameState):
    parts = command.strip().split()
    if not parts: return
    
    tribe = None
    if parts[0] == "spawn" and len(parts) >= 3: tribe = parts[2]
    elif parts[0] == "end_turn" and len(parts) >= 2: tribe = parts[1]
    elif parts[0] == "research" and len(parts) >= 3: tribe = parts[1]
    elif parts[0] in ["move", "attack"]:
        if len(parts) >= 2:
            unit_id = parts[1]
            unit = old_state.units.get(unit_id)
            if unit: tribe = unit.tribe
            
    delta_stars = 0
    if tribe:
        old_player = old_state.players.get(tribe)
        new_player = new_state.players.get(tribe)
        if old_player and new_player:
            delta_stars = new_player.stars - old_player.stars
            
    payload = {
        "timestamp": time.time(),
        "command": command,
        "delta_stars": delta_stars
    }
    
    with open("sim_history.jsonl", "a") as f:
        f.write(json.dumps(payload) + "\n")

def main():
    print("Loading current game state...")
    state, raw_data = load_game_state("game_state.json")
    
    # 1. Mutate a baseline resource node at a safe axial coordinate (e.g. 1,1,0)
    target_coord = "1,1,0"
    print(f"Mutating resource node at safe coordinate: {target_coord}")
    assert target_coord in state.tiles, f"Tile {target_coord} not found in state!"
    state.tiles[target_coord].resource = "Fruit"
    
    # 2. Programmatically execute cli_router with a raw Turn 1 transaction command
    # E.g. spawning a warrior for Tribe_A at 1,1,0 (which has the Fruit resource now)
    command = "spawn warrior Tribe_A 1 1 0"
    print(f"Executing command: {command}")
    
    mutated_state = process_command(state, command)
    
    # Assert unit is spawned successfully
    assert len(mutated_state.units) == len(state.units) + 1, "Failed to spawn unit!"
    spawned_unit_id = [uid for uid in mutated_state.units if uid not in state.units][0]
    spawned_unit = mutated_state.units[spawned_unit_id]
    assert spawned_unit.q == 1 and spawned_unit.r == 1 and spawned_unit.z == 0
    print(f"Successfully spawned unit {spawned_unit_id} of type warrior for Tribe_A at {target_coord}")
    
    # Save mutated state back to game_state.json
    print("Saving mutated game state to game_state.json...")
    save_game_state(mutated_state, raw_data, "game_state.json")
    
    # Append to sim_history.jsonl
    print("Logging transition to sim_history.jsonl...")
    log_transition(command, state, mutated_state)
    
    print("Verification complete! Delta updated successfully inside game_state.json and sim_history.jsonl.")

if __name__ == "__main__":
    main()
