# Project Terra: Development Roadmap

This roadmap outlines the systematic development of the "Terra" 4x strategy engine. Our goal is to expand the existing mock `SimTest.py` into a robust, headless, deterministic Python simulation complying with all constraints in `GEMINI.md` and `TERRA_MASTER_DOC.md`.

## Phase 1: Engine Foundation & Data Structures
**Goal: Establish robust, strictly typed data management and correct geometry.**
- **JSON State Schema**: Define a robust Pydantic or TypedDict schema for `game_state.json`. Define precise schemas for Tiles, Units, Cities, and Player states.
- **Robust Hex Math**: Expand `SimTest.py` with fully functional Axial Hex coordinates algorithms (distance, LOS, ring generation, pathfinding).
- **CLI Router Expansion**: Migrate the CLI from raw argument parsing to a structured module to handle complex actions like `spawn`, `attack`, `build`, `research`.
- **Validation Suite Integration**: Set up test scripts explicitly to verify deterministic math and world generation edge cases.

## Phase 2: Board State & Core Economy
**Goal: Implement the core loop of the game before any tribes or complex units are added.**
- **Resource & City Management**:
  - Implement city consumption (Fruit, Game, Dark Metal, Aether) and population growth.
  - Implement Stars Per Turn (SPT) calculation based on extraction and city levels.
- **The Mint System**: Implement the overarching inflation system (Tech Cost = `Base_Cost + (Total_Cities * Multiplier)`).
- **The Temple Engine**: Implement the `Tier 1` to `Zenith (Tier 5)` automatic temple scaling logic for the Faith Economy.
- **Planar Transitions (Z-Axis)**: Fully implement drop-pods, natural cave mouth entries, and High Peak transitions, ensuring Z-axis movement consumes correct action points.

## Phase 3: Combat, Vision & Units
**Goal: Enforce the zero-RNG constraint and multi-planar awareness.**
- **Deterministic Combat Engine**:
  - Implement the combat formula: `Damage = (Attacker_ATK * (Current_HP / Max_HP)) / (Defender_DEF * Terrain_Bonus)`.
  - Implement retaliation logic.
- **Unit Veterancy & Merging**:
  - Track unit kills and apply Rank 1 (+5 HP), Rank 2 (+1 ATK/DEF), and Rank 3 (Terrain Mastery).
  - Implement the "Battalion Merge" condition (requires Military Tradition Tech + 1 kill) for 3 adjacent hex units.
- **Sensory Rules (Fog of War)**: 
  - Restrict vision correctly depending on layer (Sky -> Surface visibility, Surface -> Mantle blindness).
  - Add Sonar exception for Mantle -> Surface.

## Phase 4: Diplomacy, Tech Trees, and Tribes
**Goal: Add the strategic layers and asynchronous interactions.**
- **Diplomatic Action Controller**:
  - Implement Truces (10 turns standard).
  - Implement Embassies (Vision sharing, SPT generation).
  - Implement Vassalage system (Suzerain vision protection, 20% SPT tribute).
- **The 12 Tribes of Terra**: Implement initial class templates injecting specific traits based on the tribe selected (e.g., Aethereal Cloud-Sails, The Mercanti trade hubs).
- **Technology System**: Build the tech tree unlock requirements ensuring Tribes start with their designated Tier 1 tech.

## Phase 5: Cloud Integration & Analytics
**Goal: Wire the game to Google Cloud services handling AI actions and data aggregation.**
- **Vertex AI Tribal Reasoning Integration**: Provide Vertex AI with parsed `game_state.json` allowing it to output tactical CLI commands prioritizing specific utility weights (Diplomacy/Expansion/Faith).
- **BigQuery Logging Pipeline**: Log every CLI state transition to BigQuery to identify late-game stalemates and enable balancing.
- **Cloud Pub/Sub or REST API**: Optionally wrap the `SimTest.py` to allow remote invocation of turns.
