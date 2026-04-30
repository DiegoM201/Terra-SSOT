# TECHNICAL SPEC: THE FORGE
**Stats**: Small Integers (1-40).

## 1. COMBAT FORMULA
`Damage = (Attacker_ATK * (Current_HP / Max_HP)) / (Defender_DEF * Terrain_Bonus)`
- If Defender survives and is in range, they retaliate with 50% damage output.

## 2. BASE UNITS
- **Warrior**: 10 HP, 2 ATK, 2 DEF.
- **Archer**: 10 HP, 2 ATK, 1 DEF. Range 2.
- **Sentinel**: 10 HP, 3 ATK, 1 DEF. Sky-native.