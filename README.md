# The Last Samurai
A 2D samurai action-platformer built with Pygame.

## Quick setup (English)

Prerequisites
- Python 3.8 or newer
- pip

Repository
- Clone the repository and change into the project directory:
  git clone https://github.com/Juandagarc/The-Last-Samurai.git
  cd The-Last-Samurai

Virtual environment (this project does not include a committed virtual environment)
- Create and activate a virtual environment before installing dependencies.

macOS / Linux
```bash
python -m venv venv
source venv/bin/activate
```

Windows (PowerShell)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install dependencies
```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

Run the game
```bash
python main.py
```
Expected behavior: a Pygame window (1280x720) opens with title "The Last Samurai" and a black background. Close with ESC or the window close button.

Notes
- The virtual environment is intentionally not tracked by Git. Create it locally as shown above.
- Game sources are in the `src/` folder. Assets are under `assets/` (player sprites are available in `assets/player`).
- If pygame installation fails on macOS, install Xcode Command Line Tools and ensure pip, setuptools and wheel are up to date.

Development
- Use feature branches and make small, atomic commits.
- Follow PEP 8 and keep code modular (src/player.py, src/game.py, etc.).

If you want, I can add a small shell script (start.sh) to automate venv creation, dependency installation and run. Let me know and I will add it.
