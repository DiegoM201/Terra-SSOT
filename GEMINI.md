# Project Terra: GEMINI.md

## Core Mandates
- **Tech Stack:** Python 3.11+, JSON for Game State, Vertex AI for Tribal Reasoning, BigQuery for analytics.
- **Architectural Pattern:** Logic-First, Headless Simulation.
- **State Management:** All state is a single JSON object.
- **Communication:** CLI-based command input.
- **Validation:** Always run `SimTest.py` (when created) to verify deterministic outcomes before committing logic changes.

## Development Workflow
- **Research -> Strategy -> Execution** lifecycle for all tasks.
- Use `enter_plan_mode` for any significant architectural changes or new feature designs.
- Maintain the "Three-Layer Verticality" (Heavens, Crust, Mantle) as a primary design constraint.
- Ensure deterministic combat logic (0% RNG).

## Coding Standards
- **Python:** Follow PEP 8. Use type hints for all functions.
- **JSON:** Maintain a strictly defined schema for the Game State.
- **Documentation:** Keep `TERRA_MASTER_DOC.md` updated with any major changes.

## Verification
- Reproduce bugs with a script before fixing.
- Add unit tests for every new feature.
