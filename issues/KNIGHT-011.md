# KNIGHT-011: Audio System

## Labels
`ai-ready`, `priority-medium`, `audio`

## Estimate
2 hours

## Dependencies
- KNIGHT-002 (Core Game Loop)

## Objective
Implement audio playback for music and sound effects.

## Requirements

### 1. AudioManager
- play_music(track, loop)
- play_sfx(sound)
- Volume controls
- Stop/pause functionality

### 2. Audio Integration
- Menu theme music
- Gameplay theme music
- Boss theme music
- SFX: footstep, jump, land, attack, hit, hurt, UI sounds

### 3. Files to Create
- src/systems/audio.py
- tests/test_audio.py

## Acceptance Criteria
- [ ] Music plays and loops
- [ ] SFX play on events
- [ ] Volume controls work
- [ ] Audio stops on scene change

## Agent-Specific Instructions

### Claude Code Prompt
```
Implement KNIGHT-011 following CLAUDE.md:

1. Create src/systems/audio.py:
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

Handle missing audio files gracefully.
Use logging instead of print. Include type hints.
```

## Test Cases

| Test ID | Description | Expected Result |
|---------|-------------|-----------------|
| TC-011-1 | Play music | Music starts |
| TC-011-2 | Music loops | Repeats correctly |
| TC-011-3 | Play SFX | Sound plays |
| TC-011-4 | Set volume | Volume changes |
| TC-011-5 | Stop music | Music stops |
| TC-011-6 | Missing audio file | Handles gracefully |
