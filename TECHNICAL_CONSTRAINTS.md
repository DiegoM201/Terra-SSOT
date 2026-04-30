# TECHNICAL SPEC: ARCHITECTURE

## 1. LOGIC-FIRST DESIGN
- **Headless Simulation**: Python 3.11+ Core. Game State is a JSON object.
- **Input/Output**: Simulation must accept commands via CLI (e.g., `move unit_id q r`).
- **Validation**: Agents must run `SimTest.py` to verify deterministic outcomes before committing logic changes.

## 2. GOOGLE CLOUD INTEGRATION
- **AI Reasoning**: Vertex AI manages high-level tribal utility (Diplomacy/Expansion).
- **Data Flow**: Simulation logs processed via BigQuery to identify late-game stalemates.