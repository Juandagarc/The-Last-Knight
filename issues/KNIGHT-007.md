# KNIGHT-007: Enemy AI & Patrol

## Labels
`ai-ready`, `priority-high`, `enemies`

## Estimate
3 hours

## Dependencies
- KNIGHT-003 (Entity System)
- KNIGHT-004 (Physics & Collision)

## Objective
Implement enemy entities with patrol AI behavior and basic combat.

## Requirements

### 1. Enemy Entity
- Inherits from Entity
- Has patrol points (waypoints)
- Detection range for player
- States: patrol, chase, attack, hurt, death

### 2. AI Behaviors
- PatrolBehavior: walk between points, pause at ends
- ChaseBehavior: move toward player when detected
- AttackBehavior: attack when in melee range

### 3. Files to Create
- src/entities/enemy.py
- src/systems/ai.py
- tests/test_enemy.py

## Acceptance Criteria
- [ ] Enemy patrols between waypoints
- [ ] Enemy detects player in range
- [ ] Enemy chases player
- [ ] Enemy attacks in range
- [ ] Enemy can be damaged and killed

## Agent-Specific Instructions

### Claude Code Prompt
```
Implement KNIGHT-007 following CLAUDE.md:

1. Create src/entities/enemy.py:
   - Inherits from Entity
   - patrol_points list, current_point index
   - detection_range for player detection
   - States: patrol, chase, attack, hurt, death

2. Create src/systems/ai.py:
   - PatrolBehavior: walk between waypoints
   - ChaseBehavior: move toward player
   - AttackBehavior: attack in melee range

3. Tests in tests/test_enemy.py

Use state pattern for enemy behavior.
Use logging instead of print. Include type hints.
```

## Test Cases

| Test ID | Description | Expected Result |
|---------|-------------|-----------------|
| TC-007-1 | Enemy patrols to waypoint | Moves to target |
| TC-007-2 | Enemy reaches waypoint | Changes direction |
| TC-007-3 | Player in detection range | Transitions to chase |
| TC-007-4 | Player in attack range | Attacks player |
| TC-007-5 | Enemy takes damage | Health decreases |
| TC-007-6 | Enemy health reaches 0 | Enemy dies |
