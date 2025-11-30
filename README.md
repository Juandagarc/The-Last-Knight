# The Last Knight Path

A 2D Action-Platformer game developed with Python and Pygame.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.5+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🎮 Description

The Last Knight Path follows the journey of "The Last Knight" through a ruined kingdom, featuring advanced mobility mechanics (Parkour) and tactical combat. The game emphasizes mastery of movement and combat systems across three challenging levels culminating in an epic boss battle.

## ✨ Features

- **Advanced Movement System**: Run, jump, wall slide, wall climb, and dash
- **Combo Combat**: Chain attacks with timing-based combo system
- **State Machine AI**: Intelligent enemy behavior patterns
- **Boss Battle**: Multi-phase final boss with unique attack patterns
- **Score Persistence**: Track your best times and scores
- **Gamepad Support**: Play with keyboard or controller

## 🎯 Game Mechanics

### Movement
- **Run**: Arrow keys / WASD
- **Jump**: Space / W
- **Wall Slide**: Touch wall while airborne + direction toward wall
- **Wall Climb**: Hold jump while wall sliding (stamina limited)
- **Dash**: Shift / C (grants invulnerability frames)

### Combat
- **Attack**: Z / J
- **Combo Chain**: Time attacks in the combo window for 3-hit chains
  - Attack 1: 10 damage
  - Attack 2: 15 damage  
  - Attack 3: 25 damage

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- uv package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/the-last-knight-path.git
cd the-last-knight-path

# Install dependencies with uv
uv sync

# Run the game
uv run python main.py
```

### Development Setup

```bash
# Install with development dependencies
uv sync --extra dev

# Run tests
uv run pytest tests/ -v

# Run linter
uv run flake8 src/

# Format code
uv run black src/

# Type checking
uv run mypy src/
```

## 🎮 Controls

| Action | Keyboard | Gamepad |
|--------|----------|---------|
| Move | Arrow Keys / WASD | Left Stick |
| Jump | Space / W | A Button |
| Attack | Z / J | X Button |
| Dash | Shift / C | B Button |
| Pause | ESC | Start |

## 📁 Project Structure

```
the-last-knight-path/
├── main.py                 # Entry point
├── src/
│   ├── core/              # Game singleton, settings, resources
│   ├── entities/          # Player, enemies, boss
│   ├── states/            # FSM states
│   ├── systems/           # Animation, physics, collision, input
│   ├── levels/            # Level loading and management
│   ├── ui/                # Screens and HUD
│   └── data/              # Score persistence
├── assets/
│   ├── sprites/           # Character animations
│   ├── tiles/             # Level tilesets
│   ├── maps/              # Tiled .tmx maps
│   ├── audio/             # Music and SFX
│   └── fonts/             # Game fonts
├── tests/                 # Unit and integration tests
└── docs/                  # Documentation
```

## 🛠️ Development

### Running Tests

```bash
# All tests
uv run pytest tests/ -v

# With coverage
uv run pytest tests/ --cov=src --cov-report=html

# Specific test file
uv run pytest tests/test_player.py -v
```

### Code Style

This project uses:
- **black** for formatting
- **flake8** for linting
- **mypy** for type checking

```bash
# Format code
uv run black src/

# Check linting
uv run flake8 src/

# Type check
uv run mypy src/
```

## 🐳 Docker

```bash
# Build image
docker build -t the-last-knight-path .

# Run container
docker run -it --rm the-last-knight-path
```

## 📊 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG_MODE` | Enable debug features | `false` |
| `SHOW_HITBOXES` | Display collision boxes | `false` |
| `SHOW_FPS` | Show FPS counter | `true` |
| `MUSIC_VOLUME` | Music volume (0.0-1.0) | `0.7` |
| `SFX_VOLUME` | Sound effects volume (0.0-1.0) | `0.8` |

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- Juan David García
- Adrián Fernando Gaitán
