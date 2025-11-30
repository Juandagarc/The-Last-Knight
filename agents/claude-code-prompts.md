# Claude Code Prompts Reference

Use these prompts with Claude Code for implementing each issue.

---

## KNIGHT-001: Project Initialization

```
Initialize The Last Knight Path Python/Pygame project with uv:

1. Run: uv init --name "the-last-knight-path"
2. Add dependencies: uv add pygame pytmx
3. Add dev dependencies: uv add --dev pytest pytest-cov flake8 black mypy

4. Create directory structure:
   - src/core/, src/entities/, src/states/, src/systems/
   - src/levels/, src/ui/, src/ui/screens/, src/data/
   - assets/sprites/knight, assets/sprites/enemies, assets/sprites/boss
   - assets/tiles/, assets/maps/, assets/audio/music, assets/audio/sfx
   - assets/fonts/
   - tests/, docs/, data/

5. Create src/core/settings.py with game constants:
   - SCREEN_WIDTH=1280, SCREEN_HEIGHT=720, FPS=60
   - GRAVITY=0.8, MAX_FALL_SPEED=15.0, JUMP_FORCE=-16.0
   - PLAYER_SPEED=5.0, DASH_SPEED=15.0

6. Create main.py entry point with pygame window

7. Create tests/conftest.py with pygame_init fixture

Follow CLAUDE.md. Use logging, not print. Include type hints.
```

---

## KNIGHT-002: Core Game Loop

```
Implement Game singleton and resource manager:

1. src/core/game.py - Game class:
   - Singleton pattern using __new__
   - game loop with clock.tick(FPS)
   - delta-time calculation
   - FPS counter display

2. src/core/resource_manager.py:
   - load_image() with caching
   - load_sound() with caching
   - load_font() with caching
   - clear_cache() method

3. Update main.py to use Game()

4. Write tests in tests/test_game.py

Game should maintain 60 FPS, ESC closes window.
Use logging module, include type hints.
```

---

## KNIGHT-003: Entity System

```
Create Entity base class and Animation system:

1. src/entities/entity.py:
   - Abstract class inheriting pygame.sprite.Sprite
   - pos (Vector2), velocity, image, rect
   - hitbox SEPARATE from rect (critical!)
   - apply_velocity(), set_position()

2. src/systems/animation.py:
   - Animation class: frames, frame_duration, loop
   - AnimationController: manages animations, handles flipping
   - create_placeholder_frames() for testing

3. Tests in tests/test_entity.py

CRITICAL: Keep hitbox separate from visual rect.
See CLAUDE.md section 7.2 on logic-visual decoupling.
```

---

## KNIGHT-004: Physics & Collision

```
Implement physics and collision systems:

1. src/systems/physics.py:
   - PhysicsBody: velocity, gravity, max_fall_speed
   - Collision flags: on_ground, on_wall_left, on_wall_right, on_ceiling
   - apply_gravity(), apply_friction()
   - PhysicsWorld to manage multiple bodies

2. src/systems/collision.py:
   - check_aabb_collision() function
   - CollisionManager with tile collision
   - resolve_collisions() with horizontal-first resolution
   - raycast() for line-of-sight checks
   - get_nearby_tiles() for optimization

3. Tests in tests/test_physics.py

CRITICAL: Resolve horizontal collisions before vertical
for smooth platform movement.
```

---

## KNIGHT-005: Player FSM

```
Implement Player entity with state machine:

1. src/states/state.py - Abstract State base:
   - name class attribute
   - enter(), update(dt), exit(), handle_input()
   - Return next state name from update/handle_input

2. Create state files in src/states/:
   - idle_state.py: standing, transitions to run/jump/attack/dash
   - run_state.py: horizontal movement, PLAYER_SPEED
   - jump_state.py: ascending, JUMP_FORCE applied
   - fall_state.py: descending, gravity applied
   - wall_slide_state.py: on wall + airborne, WALL_SLIDE_SPEED
   - wall_climb_state.py: hold jump on wall, limited stamina
   - dash_state.py: i-frames, locked movement, DASH_DURATION

3. src/systems/input_handler.py:
   - Key bindings dict
   - is_action_pressed(), is_action_just_pressed()
   - get_horizontal_axis() returns -1/0/1

4. src/entities/player.py:
   - Contains PhysicsBody, AnimationController, InputHandler
   - states dict, current_state
   - change_state() method
   - update() calls state.update()

Follow FSM diagram in CLAUDE.md exactly.
```

---

## KNIGHT-006: Combat System

```
Implement combat with combo attacks:

1. src/states/attack_state.py:
   - 3-attack combo chain (attack1, attack2, attack3)
   - Damage: 10, 15, 25 respectively
   - Combo window at 70% of attack duration
   - combo_buffered flag for input buffering
   - hit_targets set to prevent double-hits

2. Add CombatManager class:
   - Tracks player and enemies
   - _check_player_attacks() - player vs enemies
   - _check_enemy_attacks() - enemy vs player

3. Update Player to include AttackState

4. Tests in tests/test_combat.py

Hitboxes appear in front based on facing_right.
Use separate hitbox from visual rect per CLAUDE.md.
```

---

## KNIGHT-007: Enemy AI

```
Implement enemy entities with patrol AI:

1. src/entities/enemy.py:
   - Inherits from Entity
   - patrol_points list, current_point index
   - detection_range for player detection
   - States: patrol, chase, attack, hurt, death

2. src/systems/ai.py:
   - PatrolBehavior: walk between waypoints
   - ChaseBehavior: move toward player
   - AttackBehavior: attack in melee range

3. Tests in tests/test_enemy.py

Use state pattern for enemy behavior.
```

---

## KNIGHT-008: Boss Battle

```
Implement boss with multi-phase attacks:

1. src/entities/boss.py:
   - Large health pool (500+)
   - 3 phases based on health thresholds
   - Phase 1: Basic melee
   - Phase 2: + Projectiles
   - Phase 3: + Area attacks, faster

2. src/states/boss_states/:
   - BossIdleState
   - BossMeleeState
   - BossRangedState
   - BossAreaState

3. Tests in tests/test_boss.py

Boss should be challenging but fair.
```

---

## KNIGHT-009: Level Loading

```
Implement level system with pytmx:

1. src/levels/tile_map.py:
   - Load .tmx files
   - Extract collision layer to Rects
   - Extract spawn points
   - Render tile layers

2. src/levels/level_manager.py:
   - load_level(level_id)
   - get_spawn_points()
   - transition_to_next_level()

3. src/systems/camera.py:
   - Follow player with smoothing (lerp)
   - Clamp to level bounds
   - screen_shake(duration, intensity)

4. Tests in tests/test_levels.py
```

---

## KNIGHT-010: UI Screens

```
Implement game screens and HUD:

1. src/ui/screens/:
   - intro_screen.py: Logo fade-in
   - menu_screen.py: Play, Help, Credits, Exit
   - game_screen.py: Active gameplay
   - pause_screen.py: Resume, Quit
   - help_screen.py: Controls
   - credits_screen.py: Team credits

2. src/ui/hud.py:
   - Health bar
   - Score display
   - Timer

3. src/ui/widgets.py:
   - Button class
   - Text rendering helpers

4. Tests in tests/test_ui.py
```

---

## KNIGHT-011: Audio System

```
Implement audio manager:

1. src/systems/audio.py:
   - AudioManager singleton
   - play_music(track, loop=True)
   - stop_music(), pause_music()
   - play_sfx(sound_name)
   - set_music_volume(), set_sfx_volume()

2. Integration:
   - Menu music on menu screen
   - Game music during gameplay
   - Boss music during boss fight
   - SFX for all actions

3. Tests in tests/test_audio.py
```

---

## KNIGHT-012: Score Persistence

```
Implement score system with JSON:

1. src/data/score_manager.py:
   - current_score, elapsed_time
   - add_score(points)
   - save_high_scores()
   - load_high_scores()
   - get_top_scores(count=10)

2. data/scores.json structure:
   {
     "high_scores": [
       {"name": "AAA", "score": 1000, "time": 120.5}
     ]
   }

3. Tests in tests/test_scores.py

Handle file not found gracefully.
```

---

## KNIGHT-013: Test Coverage

```
Achieve 80%+ test coverage:

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
```

---

## KNIGHT-014: Documentation & CI

```
Complete documentation and CI:

1. Update README.md with:
   - Full uv commands
   - Architecture overview
   - Contributing guidelines

2. Create .github/workflows/ci.yml:
   - Lint with flake8
   - Format check with black
   - Type check with mypy
   - Test with pytest + coverage
   - Build Docker image

3. Ensure all badges work:
   - Python version
   - Pygame version
   - CI status
   - Coverage

Use uv for all Python commands in CI.
```
