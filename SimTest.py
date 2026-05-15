import json
import time
from backend.models import GameState, Player, TribeHeuristics, Tile
from backend.cli_router import process_command

def log_transition(command: str, old_state: GameState, new_state: GameState):
    """Logs the transition between states and tracks economy deltas."""
    # Find the tribe executing the command (simplistic assumption for telemetry)
    parts = command.strip().split()
    if not parts: return
    
    tribe = None
    if parts[0] == "spawn" and len(parts) >= 3: tribe = parts[2]
    elif parts[0] == "end_turn" and len(parts) >= 2: tribe = parts[1]
    elif parts[0] == "research" and len(parts) >= 3: tribe = parts[1]
    elif parts[0] in ["move", "attack"]:
        # Infer from unit
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

class HeuristicEngine:
    def __init__(self, state: GameState, tribe: str):
        self.state = state
        self.tribe = tribe
        
    def evaluate(self) -> str:
        player = self.state.players.get(self.tribe)
        if not player:
            return "end_turn unknown"
            
        weights = player.heuristics
        
        # Calculate utility scores based on TribeHeuristics and stars
        # Settle: expansion_weight * (1 if empty land, 0 otherwise) (Mock: True if turn < 5)
        score_settle = weights.expansion_weight * (1 if self.state.turn < 5 else 0)
        
        # Recruit: aggression_weight * (1 if stars >= 2, 0 otherwise)
        score_recruit = weights.aggression_weight * (1 if player.stars >= 2 else 0)
        
        # Temple: faith_weight * (1 if stars >= 20, 0 otherwise)
        score_temple = weights.faith_weight * (1 if player.stars >= 20 else 0)
        
        utilities = {
            "settle": score_settle,
            "recruit": score_recruit,
            "temple": score_temple,
            "end_turn": 0.1 # Always a slight preference to end turn if nothing else is good
        }
        
        best_action = max(utilities.items(), key=lambda x: x[1])[0]
        
        if best_action == "recruit":
            return f"spawn warrior {self.tribe} 0 0 0" # simplistic default
        elif best_action == "temple":
            # Assume temple is researched or simulated via some action
            return f"research {self.tribe} temple" 
        elif best_action == "settle":
            # Assume settling is done via moving or specific command, for now simulate move
            return f"move placeholder 1 1 0"
            
        return f"end_turn {self.tribe}"

def create_mock_state() -> GameState:
    players = {
        "Romani": Player(tribe="Romani", stars=5, total_cities=1, heuristics=TribeHeuristics(aggression_weight=0.8, expansion_weight=0.6, faith_weight=0.2))
    }
    tiles = {
        "0,0,0": Tile(q=0, r=0, z=0, biome="plains"),
        "1,0,0": Tile(q=1, r=0, z=0, biome="plains"),
        "0,1,0": Tile(q=0, r=1, z=0, biome="plains")
    }
    return GameState(turn=1, tiles=tiles, units={}, cities={}, players=players)

def main():
    state = create_mock_state()
    tribe = "Romani"
    
    print("Starting Headless Simulation Loop...")
    
    for _ in range(5):
        engine = HeuristicEngine(state, tribe)
        action = engine.evaluate()
        
        print(f"Turn {state.turn} - AI evaluated action: {action}")
        
        new_state = process_command(state, action)
        log_transition(action, state, new_state)
        
        # State mutation for the loop, we simulate turn progressing
        state = new_state
        state.turn += 1

if __name__ == "__main__":
    main()
