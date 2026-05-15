# Local-First Pivot & Router Modularization

This plan details the implementation of a massive engine refactor for Terra, focusing on local-first deterministic execution, router modularization via the Command Dispatcher pattern, and Z-axis transition mechanics. It will eliminate cloud dependencies, ensure strict deterministic operations, and introduce basic heuristic-based AI with telemetry logging.

## User Review Required

> [!WARNING]
> We will completely remove the current `if/elif` structure in `cli_router.py` in favor of a Command Dispatcher pattern. Any custom scripts relying on the exact internal structure of `process_command` beyond its external signature will need to be updated.
> 
> `SimTest.py` will be created in the root directory and will act as a headless simulation loop.

## Open Questions

> [!IMPORTANT]
> 1. **Unit Stats:** I will use generic default stats for Warrior, Archer, and Sentinel (e.g., Warrior: 10 HP, 2 ATK, 2 DEF, Range 1, native_z 0; Archer: 8 HP, 2 ATK, 1 DEF, Range 2, native_z 0; Sentinel: 15 HP, 1 ATK, 3 DEF, Range 1, native_z 1). Please confirm if these are acceptable or provide specific stats.
> 2. **Tile Features:** For Z-axis transitions, should `"cave_mouth"` and `"high_peak"` be treated as the tile's `biome`, `resource`, or `building`? I will check if they match any of these three fields by default.

## Proposed Changes

---

### Models (Local AI Brains)

#### [MODIFY] [models.py](file:///c:/Users/diego/OneDrive/Desktop/Terra%20SSOT/backend/models.py)
- Create `TribeHeuristics` Pydantic BaseModel with `float` fields: `expansion_weight`, `aggression_weight`, `faith_weight` (defaulting to 0.5).
- Add `heuristics: TribeHeuristics` field to the `Player` model (with default empty heuristics).

---

### Command Dispatcher & Z-Axis (Router Refactor)

#### [MODIFY] [cli_router.py](file:///c:/Users/diego/OneDrive/Desktop/Terra%20SSOT/backend/cli_router.py)
- **Unit Registry:** Add `UNIT_STATS` dictionary mapping "warrior", "archer", and "sentinel" to their HP, ATK, DEF, Range, and `native_z` (Sky=1, Surface=0, Mantle=-1).
- **Command Dispatcher:** Refactor `process_command` to use a `COMMAND_REGISTRY` mapping string commands to dedicated helper functions (`_handle_spawn`, `_handle_move`, `_handle_attack`, `_handle_end_turn`, `_handle_research`).
- **Z-Axis Validation:** In `_handle_move`, add logic to check Z-axis differences.
  - Check for `"cave_mouth"` in the target or source tile when transitioning between Surface (0) and Mantle (-1).
  - Check for `"high_peak"` in the target or source tile when transitioning between Surface (0) and Sky (1).
  - Allow drop-pod transitions from Sky (1) to Surface (0) natively.
- Ensure deepcopy mutation logic using `current_state.model_copy(deep=True)`.

---

### Heuristic Engine & Telemetry

#### [NEW] [SimTest.py](file:///c:/Users/diego/OneDrive/Desktop/Terra%20SSOT/SimTest.py)
- Create a local standalone test loop script.
- **Telemetry:** Implement `log_transition(command, old_state, new_state)` to calculate player economy deltas and write timestamped JSON logs to `sim_history.jsonl`.
- **Heuristics:** Implement `HeuristicEngine` to evaluate utility based on tribe heuristics (`expansion_weight`, `aggression_weight`, `faith_weight`) and return simple CLI actions (e.g., spawn, research, end_turn).
- **Execution Loop:** Build a `main()` loop that initializes a mock state, asks the `HeuristicEngine` for actions, routes them through `process_command`, logs transitions, and repeats deterministically. No `google.cloud` imports used.

## Verification Plan

### Automated Tests
- Run `pytest` to ensure all existing functionality in `test_router.py` remains intact with the new Dispatcher pattern.
- Execute `python SimTest.py` to ensure it successfully generates `sim_history.jsonl` with multiple turns of AI actions without crashing.

### Manual Verification
- Review `sim_history.jsonl` to ensure proper JSON serialization and telemetry structure (deltas are correct).
