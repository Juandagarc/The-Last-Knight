# KNIGHT-009: Level Loading & Camera

## Labels
`ai-ready`, `priority-medium`, `levels`

## Estimate
3 hours

## Dependencies
- KNIGHT-004 (Physics & Collision)

## Objective
Implement level loading from Tiled maps and camera system.

## Requirements

### 1. Tile Map Loading
- Load .tmx files with pytmx
- Extract collision layer
- Extract spawn points (player, enemies)
- Render tile layers

### 2. Level Manager
- Load levels by ID (1, 2, 3, boss)
- Level transitions
- Victory conditions

### 3. Camera System
- Follow player with smoothing
- Respect level bounds
- Screen shake effect

### 4. Files to Create
- src/levels/tile_map.py
- src/levels/level_manager.py
- src/systems/camera.py
- tests/test_levels.py

## Acceptance Criteria
- [ ] Levels load from .tmx files
- [ ] Collision works with tiles
- [ ] Camera follows player
- [ ] Level transitions work

## Agent-Specific Instructions

### Claude Code Prompt
```
Implement KNIGHT-009 following CLAUDE.md:

1. Create src/levels/tile_map.py:
   - Load .tmx files with pytmx
   - Extract collision layer to Rects
   - Extract spawn points
   - Render tile layers

2. Create src/levels/level_manager.py:
   - load_level(level_id)
   - get_spawn_points()
   - transition_to_next_level()

3. Create src/systems/camera.py:
   - Follow player with smoothing (lerp)
   - Clamp to level bounds
   - screen_shake(duration, intensity)

4. Tests in tests/test_levels.py

Use logging instead of print. Include type hints.
```

## Test Cases

| Test ID | Description | Expected Result |
|---------|-------------|-----------------|
| TC-009-1 | Load .tmx file | Level loaded |
| TC-009-2 | Extract collision tiles | Rect list created |
| TC-009-3 | Camera follows player | Position updates |
| TC-009-4 | Camera at bounds | Clamped correctly |
| TC-009-5 | Screen shake | Camera offset changes |
| TC-009-6 | Level transition | New level loads |
