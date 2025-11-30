# KNIGHT-010: UI Screens & HUD

## Labels
`ai-ready`, `priority-medium`, `ui`

## Estimate
3 hours

## Dependencies
- KNIGHT-002 (Core Game Loop)

## Objective
Implement all game screens and the in-game HUD.

## Requirements

### 1. Screens
- IntroScreen: Logo, fade to menu
- MenuScreen: Play, Help, Credits, Exit
- GameScreen: Active gameplay
- PauseScreen: Resume, Settings, Quit
- HelpScreen: Control diagram
- CreditsScreen: Developer credits

### 2. HUD
- Health bar (current/max)
- Score display
- Timer

### 3. Files to Create
- src/ui/screens/intro_screen.py
- src/ui/screens/menu_screen.py
- src/ui/screens/game_screen.py
- src/ui/screens/pause_screen.py
- src/ui/screens/help_screen.py
- src/ui/screens/credits_screen.py
- src/ui/hud.py
- src/ui/widgets.py
- tests/test_ui.py

## Acceptance Criteria
- [ ] All screens render correctly
- [ ] Menu navigation works
- [ ] HUD displays game state
- [ ] Screen transitions work

## Agent-Specific Instructions

### Claude Code Prompt
```
Implement KNIGHT-010 following CLAUDE.md:

1. Create src/ui/screens/:
   - intro_screen.py: Logo fade-in
   - menu_screen.py: Play, Help, Credits, Exit
   - game_screen.py: Active gameplay
   - pause_screen.py: Resume, Quit
   - help_screen.py: Controls
   - credits_screen.py: Team credits

2. Create src/ui/hud.py:
   - Health bar
   - Score display
   - Timer

3. Create src/ui/widgets.py:
   - Button class
   - Text rendering helpers

4. Tests in tests/test_ui.py

Use logging instead of print. Include type hints.
```

## Test Cases

| Test ID | Description | Expected Result |
|---------|-------------|-----------------|
| TC-010-1 | Render intro screen | Logo displayed |
| TC-010-2 | Menu navigation | Buttons work |
| TC-010-3 | HUD health bar | Displays correctly |
| TC-010-4 | HUD score | Updates correctly |
| TC-010-5 | Pause screen | Overlay works |
| TC-010-6 | Screen transition | Changes correctly |
