# KNIGHT-013: Test Coverage

## Labels
`ai-ready`, `priority-medium`, `testing`

## Estimate
3 hours

## Dependencies
- All previous issues

## Objective
Achieve 80%+ test coverage across all modules.

## Requirements

### 1. Test Files
- tests/test_entity.py
- tests/test_physics.py
- tests/test_collision.py
- tests/test_player.py
- tests/test_states.py
- tests/test_combat.py
- tests/test_enemy.py
- tests/test_boss.py
- tests/test_levels.py
- tests/test_ui.py
- tests/test_audio.py
- tests/test_scores.py

### 2. Coverage Goals
- Minimum 80% overall
- 90%+ on critical paths (collision, combat, FSM)

### 3. Test Types
- Unit tests for individual functions
- Integration tests for component interactions
- Edge case testing
- Error handling testing

## Acceptance Criteria
- [ ] All test files created
- [ ] 80%+ coverage achieved
- [ ] All tests pass
- [ ] CI pipeline green

## Agent-Specific Instructions

### Claude Code Prompt
```
Implement KNIGHT-013 following CLAUDE.md:

1. Run: uv run pytest --cov=src --cov-report=html

2. Identify uncovered code paths

3. Add tests for:
   - Edge cases in physics
   - State transitions
   - Combat interactions
   - Error handling

4. Target 90%+ on critical modules:
   - collision.py
   - attack_state.py
   - player.py

5. Use parametrize for multiple test cases

Follow tests.instructions.md for test patterns.
```

## Test Cases

| Test ID | Description | Expected Result |
|---------|-------------|-----------------|
| TC-013-1 | Run coverage | Report generated |
| TC-013-2 | Overall coverage | 80%+ achieved |
| TC-013-3 | Critical modules | 90%+ achieved |
| TC-013-4 | All tests pass | 100% pass rate |
| TC-013-5 | CI pipeline | All checks pass |
