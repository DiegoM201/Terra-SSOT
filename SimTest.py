import json
import sys
import os
import random
from typing import Dict, Any, List, Tuple
from models import GameState, GameMetadata, Layer, Tile, TileType, TileProperty, Tribe

class TerraSimulation:
    def __init__(self, state_path: str):
        self.state_path = state_path
        self.state: GameState = self.load_state()

    def load_state(self) -> GameState:
        if not os.path.exists(self.state_path):
            print(f"Error: State file not found at {self.state_path}")
            sys.exit(1)
        with open(self.state_path, 'r') as f:
            data = json.load(f)
            return GameState(**data)

    def save_state(self):
        with open(self.state_path, 'w') as f:
            # Use model_dump_json or model_dump for Pydantic v2
            f.write(self.state.model_dump_json(indent=2, by_alias=True))

    def get_hex_grid(self, radius: int) -> List[Tuple[int, int]]:
        """Generates axial (q, r) coordinates for a hexagonal grid of a given radius."""
        coords = []
        for q in range(-radius, radius + 1):
            r1 = max(-radius, -q - radius)
            r2 = min(radius, -q + radius)
            for r in range(r1, r2 + 1):
                coords.append((q, r))
        return coords

    def generate_world(self, radius: int, seed: int):
        """Procedural generation for the three layers based on noise thresholds."""
        print(f"Generating world with radius {radius} and seed {seed}...")
        random.seed(seed)
        coords = self.get_hex_grid(radius)
        
        # Reset layers using Pydantic models
        self.state.layers = {
            "sky": Layer(z=1, tiles={}),
            "crust": Layer(z=0, tiles={}),
            "mantle": Layer(z=-1, tiles={})
        }

        # 1. Generate Surface (L0) and Sky (L1)
        for q, r in coords:
            key = f"{q},{r}"
            noise_val = random.random()
            
            # Sky (L1) - Sparse Islands
            if noise_val >= 0.8:
                self.state.layers["sky"].tiles[key] = Tile(type=TileType.FLOATING_ISLAND)
            
            # Crust (L0) - Surface Land
            l0_noise = random.random()
            is_land = l0_noise >= 0.45
            tile_type = TileType.LAND if is_land else TileType.WATER
            self.state.layers["crust"].tiles[key] = Tile(type=tile_type, properties=[])
            
            # Mantle (L-1) - Cavern Paths (10% threshold)
            l_minus1_noise = random.random()
            if l_minus1_noise >= 0.9:
                self.state.layers["mantle"].tiles[key] = Tile(type=TileType.CAVERN_PATH)
            else:
                self.state.layers["mantle"].tiles[key] = Tile(type=TileType.SOLID_ROCK)

        # 2. Alignment and Transitions
        for q, r in coords:
            key = f"{q},{r}"
            
            # Shadowing: L1 land creates shadow on L0
            if key in self.state.layers["sky"].tiles:
                self.state.layers["crust"].tiles[key].properties.append(TileProperty.SHADOWED)
                # L0 ↔ L1 Transition: High Peak
                if self.state.layers["crust"].tiles[key].type == TileType.LAND:
                    self.state.layers["crust"].tiles[key].type = TileType.HIGH_PEAK

            # L0 ↔ L-1 Transition: Cave Mouth
            if self.state.layers["mantle"].tiles[key].type == TileType.CAVERN_PATH:
                if self.state.layers["crust"].tiles[key].type == TileType.LAND:
                    self.state.layers["crust"].tiles[key].type = TileType.CAVE_MOUTH

        self.save_state()
        print("World generation complete.")

    def print_map(self, layer_key: str):
        """Prints a basic ASCII representation of a layer."""
        if layer_key not in self.state.layers:
            print(f"Invalid layer: {layer_key}")
            return
        
        tiles = self.state.layers[layer_key].tiles
        # Find bounds for printing
        qs = [int(k.split(',')[0]) for k in tiles.keys()]
        rs = [int(k.split(',')[1]) for k in tiles.keys()]
        
        if not qs: return
        
        print(f"\n--- Layer: {layer_key.upper()} ---")
        for r in range(min(rs), max(rs) + 1):
            line = " " * (r - min(rs)) # Hex offset
            for q in range(min(qs), max(qs) + 1):
                key = f"{q},{r}"
                if key in tiles:
                    t = tiles[key].type
                    if t == TileType.WATER: line += "~ "
                    elif t == TileType.LAND: line += ". "
                    elif t == TileType.HIGH_PEAK: line += "^ "
                    elif t == TileType.CAVE_MOUTH: line += "o "
                    elif t == TileType.FLOATING_ISLAND: line += "# "
                    elif t == TileType.CAVERN_PATH: line += "+ "
                    elif t == TileType.SOLID_ROCK: line += "X "
                    else: line += "? "
                else:
                    line += "  "
            print(line)

    def validate_move(self, unit_id: str, target_q: int, target_r: int, target_z: int) -> bool:
        print(f"Validating move: unit {unit_id} to ({target_q}, {target_r}, {target_z})")
        return True

    def execute_command(self, cmd_args: List[str]):
        if not cmd_args:
            return

        cmd = cmd_args[0].lower()
        if cmd == "move" and len(cmd_args) == 5:
            unit_id, q, r, z = cmd_args[1], int(cmd_args[2]), int(cmd_args[3]), int(cmd_args[4])
            if self.validate_move(unit_id, q, r, z):
                print(f"Move executed: {unit_id} to ({q}, {r}, {z})")
                self.save_state()
        elif cmd == "generate" and len(cmd_args) == 3:
            radius, seed = int(cmd_args[1]), int(cmd_args[2])
            self.generate_world(radius, seed)
            for layer in ["sky", "crust", "mantle"]:
                self.print_map(layer)
        else:
            print(f"Unknown or malformed command: {' '.join(cmd_args)}")

if __name__ == "__main__":
    state_file = os.path.join(os.path.dirname(__file__), "game_state.json")
    
    # Check if game_state.json exists, if not create a minimal valid one for Pydantic to load
    if not os.path.exists(state_file):
        initial_state = {
            "game_metadata": {
                "name": "Project Terra",
                "version": "0.1.0",
                "turn": 1,
                "active_tribe": "Tribe_A"
            },
            "layers": {},
            "units": {},
            "cities": {},
            "tribes": {
                "Tribe_A": {
                    "score": 0,
                    "techs": [],
                    "resources": {"stars": 5, "faith": 0}
                }
            }
        }
        with open(state_file, 'w') as f:
            json.dump(initial_state, f)

    sim = TerraSimulation(state_file)
    
    if len(sys.argv) > 1:
        sim.execute_command(sys.argv[1:])
    else:
        print("Project Terra Headless Simulation")
        print("Usage: python SimTest.py generate radius seed")
        print("       python SimTest.py move unit_id q r z")
