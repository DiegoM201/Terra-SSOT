# TECHNICAL SPEC: THE FORUM

## 1. DIPLOMATIC ACTIONS
- **Truce**: 10 turns of non-aggression.
- **Embassy**: Reveals vision and generates Stars/Turn for the owner.
- **Trade**: Exchange Tech, Cities, or even specific Hex-Tiles for Stars or SPT.

## 2. VASSALIZATION (SUBJUGATION)
- **Suzerain**: Provides protection and shared vision.
- **Vassal**: Provides 20% of their SPT to the Suzerain.
- **Win Condition**: Controlling all Capitals via direct ownership or Vassalage.
# TECHNICAL SPEC: FAITH ECONOMY

## 1. THE TEMPLE ENGINE
Temples are the sole source of Faith. They upgrade automatically every 2 turns.
- **Tier 1 (Turns 1-2)**: +1 Faith/turn.
- **Tier 2 (Turns 3-4)**: +2 Faith/turn.
- **Tier 3 (Turns 5-6)**: +3 Faith/turn.
- **Tier 4 (Turns 7-8)**: +4 Faith/turn.
- **Tier 5 (Turn 9+)**: +5 Faith/turn (Zenith Tier).

## 2. ASCENSION WIN CONDITION
A tribe wins when their total Accumulated Faith reaches the "Zenith Threshold."
- **Threshold**: `500 + (Map_Total_Cities * 50)`.
# TECHNICAL SPEC: TRIPLE-LAYER GENERATION
**Geometry**: Flat Axial Hex Grid.

## 1. THE STACKED STATE
State is stored as: `Grid[(q, r)] = { -1: MantleTile, 0: SurfaceTile, 1: SkyTile }`.

## 2. BIOME GENERATION
- **Layer 0 (Surface)**: Simplex Noise ($N \geq 0.45$ = Land).
- **Layer 1 (Sky)**: Sparse Noise ($N \geq 0.8$ = Floating Island).
- **Layer -1 (Mantle)**: Cellular Automata generated tunnels. 90% "Solid Rock" (Blocked), 10% "Cavern Path."

## 3. ALIGNMENT RULES
- **Shadows**: If Layer 1 is Land, Layer 0 below is "Shadowed" (-1 SPT).
- **Entrances**: "Cave Mouths" spawn on Layer 0 where Layer -1 paths exist. "High Peaks" spawn on Layer 0 where Layer 1 islands exist.
# TECHNICAL SPEC: THE MINT
**Currency**: Stars.

## 1. REVENUE (SPT)
- Stars Per Turn (SPT) = City Level + Resource Extraction.
- Cities grow by consuming resources (Fruit, Game, Dark Metal, Aether).

## 2. GROWTH PREVENTION (INFLATION)
- Tech Cost = `Base_Cost + (Total_Cities * Multiplier)`.
- This prevents "Infinite Expansion" from making technology trivial.

## 3. COSTS
- Warrior: 2 Stars | Archer: 3 Stars | Temple: 20 Stars.
# TECHNICAL SPEC: ARCHITECTURE

## 1. LOGIC-FIRST DESIGN
- **Headless Simulation**: Python 3.11+ Core. Game State is a JSON object.
- **Input/Output**: Simulation must accept commands via CLI (e.g., `move unit_id q r`).
- **Validation**: Agents must run `SimTest.py` to verify deterministic outcomes before committing logic changes.

## 2. GOOGLE CLOUD INTEGRATION
- **AI Reasoning**: Vertex AI manages high-level tribal utility (Diplomacy/Expansion).
- **Data Flow**: Simulation logs processed via BigQuery to identify late-game stalemates.
# PROJECT TERRA: THE CENTRAL VISION
**Spiritual Core**: Evolved Polytopia (The Square has depth).

## 1. THE CORE HOOK
"It’s my square now." Terra is a further development on what Polytopia can be, introducing elements from established 4x Grand Strategies and new dynamic features. 

## 2. THE THREE LAYERS: STRATEGIC INTENT
- **The Heavens (Sky - Z=1)**: High-tech sanctuary and tactical high ground. Limited small floating islands provide salvation through progress or prayer.
- **The Crust (Surface - Z=0)**: The classic theater of war and economic engine. Most cities are founded here. Bridge between the light above and depths below.
- **The Mantle (Subterranean - Z=-1)**: Cramped, dangerous stronghold. A network of caves/tunnels invisible to Surface/Sky. Strategic for bypass maneuvers or heroic last stands.

## 3. KEY USER EXPERIENCES
- **Low-Poly Legibility**: Vibrant colors and distinct silhouettes for instant data readability.
- **Multi-Planar Maneuvers**: Players can exist solely on one layer if needed, or use them as complimentary theaters.
- **Deterministic Combat**: 100% predictable outcomes based on fixed math. No RNG.
- **Macro-Strategy Scaling**: Upgrade/veterancy systems and Battalion merging to reduce late-game micro-fatigue.

## 4. THE WIN CONDITIONS
- **The Triumph (Military)**: Capture all rival Capitals across all three layers.
- **The Pax Squarena (Diplomatic)**: Control all capitals or subjugate rivals as subjects.
- **The Ascension (Faith)**: Build a civilization seeking communion with the heavens via Temple Tier zenith.
# TECHNICAL SPEC: THE 12 TRIBES OF TERRA

## 1. LAYER-NATIVE TRIBES (Z-AXIS SPECIALISTS)
- **1. The Aethereal**: Start on a **Heavens (Z=1)** island. 
    - *Feature*: Cloud-Sails. All units gain "Flyer" trait at Rank 1 Veterancy.
- **2. The Hollowed**: Start in the **Mantle (Z=-1)**. 
    - *Feature*: Sonar. Can see units on the Surface (Z=0) from the Mantle.
- **3. The Deep-Forged**: Start in the **Mantle (Z=-1)**. 
    - *Feature*: Dark Metal Mastery. Mines yield +2 additional Stars per turn.

## 2. DIPLOMACY & ASCENSION SPECIALISTS
- **4. The Seraphim**: Faith focus. 
    - *Feature*: Divine Growth. Temples start at Tier 2 (+2 Faith/turn) when built.
- **5. The Mercanti**: Economic focus. 
    - *Feature*: Trade Hubs. Embassies generate 2x Stars based on the rival's SPT.
- **6. The Arbiters**: Diplomatic focus. 
    - *Feature*: Iron Truce. Truces last 15 turns instead of 10. Breaking a Truce with an Arbiter costs the aggressor 50 Stars.

## 3. MILITARY & MACRO-SCALING SPECIALISTS
- **7. The Vanguard**: Veterancy focus. 
    - *Feature*: Combat Drills. Units gain Rank 1 at 2 kills instead of 3.
- **8. The Iron-Legion**: Battalion focus. 
    - *Feature*: Phalanx. Battalions deal +2 damage when attacking from a Field tile.
- **9. The Shadow-Walkers**: Stealth focus. 
    - *Feature*: Veil. Units are invisible on the Surface (Z=0) if they are adjacent to a Mountain or Forest.

## 4. TERRAIN & RESOURCE SPECIALISTS
- **10. The Arboris**: Nature focus. 
    - *Feature*: Can spend 2 Stars to grow a Forest on any land tile.
- **11. The Mariners**: Naval focus. 
    - *Feature*: Starts with "Sailing" tech. Rafts have +1 Movement.
- **12. The Nomads**: Expansion focus. 
    - *Feature*: Pioneers. Capturing a Neutral Village grants a one-time bonus of 10 Stars.

## 5. STARTING TECH TABLE
*Each tribe starts with one Tier 1 Technology unlocked based on their theme (e.g., Hollowed starts with Mining, Mariners with Sailing).*
# TECHNICAL SPEC: PLANAR TRANSITIONS

## 1. SENSORY RULES (VISION)
- **Sky → Surface**: Full vision.
- **Surface → Mantle**: Zero vision into tunnels unless standing on an entrance.
- **Mantle → Anywhere**: Zero vision outside the Subterranean layer.

## 2. TRANSITIONS
- **Natural**: Cave Mouths (L0 ↔ L-1) and High Peaks (L0 ↔ L1).
- **Drop-Pods**: Units on L1 can "Drop" to any visible L0 tile (costs turn action).
- **Teleports**: T3 Tech "Aether Gate" allows instant transit between city centers.
# TECHNICAL SPEC: THE FORGE
**Stats**: Small Integers (1-40).

## 1. COMBAT FORMULA
`Damage = (Attacker_ATK * (Current_HP / Max_HP)) / (Defender_DEF * Terrain_Bonus)`
- If Defender survives and is in range, they retaliate with 50% damage output.

## 2. BASE UNITS
- **Warrior**: 10 HP, 2 ATK, 2 DEF.
- **Archer**: 10 HP, 2 ATK, 1 DEF. Range 2.
- **Sentinel**: 10 HP, 3 ATK, 1 DEF. Sky-native.
# TECHNICAL SPEC: UNIT EVOLUTION

## 1. VETERANCY TIERS
- **Rank 1 (3 Kills)**: +5 Health. Unit gains a custom Name.
- **Rank 2 (6 Kills)**: Choose: +1 permanent Attack OR +1 permanent Defense.
- **Rank 3 (9 Kills)**: Choose: Terrain Mastery (Negate penalty/gain +1 DEF on 1 Terrain type).

## 2. BATTALION MERGE (LATE GAME)
- **Condition**: Military Tradition Tech unlocked + Unit has killed at least 1 enemy.
- **Logic**: 3 units of the same type on adjacent hexes can "Merge."
- **Stats**: HP = Sum of 3 units (Max 40). ATK/DEF = Highest of the 3 units + 1.
