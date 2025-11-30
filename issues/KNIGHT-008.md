# KNIGHT-008: Boss Battle

## Labels
`ai-ready`, `priority-high`, `boss`

## Estimate
4 hours

## Dependencies
- KNIGHT-007 (Enemy AI)

## Objective
Implement the final boss with multi-phase attack patterns.

## Requirements

### 1. Boss Entity
- Large hitbox, high health (500+)
- 3 phases based on health thresholds
- Phase 1 (100-66%): Basic melee attacks
- Phase 2 (66-33%): + Projectile attacks
- Phase 3 (33-0%): + Area attacks, increased speed

### 2. Boss States
- Idle, Melee Attack, Ranged Attack, Area Attack
- Transitions based on phase and cooldowns

### 3. Files to Create
- src/entities/boss.py
- src/states/boss_states/ (multiple files)
- tests/test_boss.py

## Acceptance Criteria
- [ ] Boss has 3 distinct phases
- [ ] Attack patterns change per phase
- [ ] Boss can be damaged
- [ ] Victory on boss death

## Agent-Specific Instructions

### Claude Code Prompt
```
Implement KNIGHT-008 following CLAUDE.md:

1. Create src/entities/boss.py:
   - Large health pool (500+)
   - 3 phases based on health thresholds
   - Phase 1: Basic melee
   - Phase 2: + Projectiles
   - Phase 3: + Area attacks, faster

2. Create src/states/boss_states/:
   - BossIdleState
   - BossMeleeState
   - BossRangedState
   - BossAreaState

3. Tests in tests/test_boss.py

Boss should be challenging but fair.
Use logging instead of print. Include type hints.
```

## Test Cases

| Test ID | Description | Expected Result |
|---------|-------------|-----------------|
| TC-008-1 | Boss initializes | Health = 500 |
| TC-008-2 | Boss at 100-66% health | Phase 1 attacks |
| TC-008-3 | Boss at 66-33% health | Phase 2 attacks |
| TC-008-4 | Boss at 33-0% health | Phase 3 attacks |
| TC-008-5 | Boss takes damage | Health decreases |
| TC-008-6 | Boss health reaches 0 | Victory condition |
