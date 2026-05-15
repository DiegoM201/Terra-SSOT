# Engine Refactor Tasks

- [x] Update `models.py`
  - [x] Add `TribeHeuristics` Pydantic BaseModel.
  - [x] Add `heuristics: TribeHeuristics` to `Player` model.
- [x] Refactor `cli_router.py`
  - [x] Define `UNIT_STATS` dictionary.
  - [x] Rewrite `process_command` using a Command Dispatcher Pattern.
  - [x] Implement `_handle_spawn`, `_handle_move`, `_handle_attack`, `_handle_end_turn`, `_handle_research`.
  - [x] Implement Z-Axis transition logic based on "transitory tiles" (`biome` == `"cave_mouth"` or `"high_peak"`).
- [x] Create `SimTest.py`
  - [x] Implement `log_transition` for telemetry.
  - [x] Implement `HeuristicEngine` for AI.
  - [x] Construct main execution loop.
- [x] Validate and summarize
  - [x] Test logic with pytest.
  - [x] Verify `SimTest.py` telemetry generation.
  - [x] Create Walkthrough artifact.
