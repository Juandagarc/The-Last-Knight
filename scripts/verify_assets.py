#!/usr/bin/env python3
"""
Asset verification script for The Last Knight Path.

Checks if all required asset directories exist and lists missing assets.
Run this script after downloading assets to verify completeness.
"""

from pathlib import Path
from typing import Dict, List

# Color codes for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent


def check_directory_structure() -> Dict[str, bool]:
    """Check if required directories exist."""
    project_root = get_project_root()
    required_dirs = [
        "assets/sprites/knight",
        "assets/sprites/enemies",
        "assets/sprites/boss",
        "assets/tiles",
        "assets/maps",
        "assets/audio/music",
        "assets/audio/sfx",
        "assets/fonts",
    ]

    results = {}
    for dir_path in required_dirs:
        full_path = project_root / dir_path
        results[dir_path] = full_path.exists()

    return results


def check_asset_files() -> Dict[str, List[str]]:
    """Check for expected asset files and list what's present."""
    project_root = get_project_root()

    asset_checks = {
        "Knight Sprites": project_root / "assets/sprites/knight",
        "Enemy Sprites": project_root / "assets/sprites/enemies",
        "Boss Sprites": project_root / "assets/sprites/boss",
        "Tilesets": project_root / "assets/tiles",
        "Maps": project_root / "assets/maps",
        "Music": project_root / "assets/audio/music",
        "Sound Effects": project_root / "assets/audio/sfx",
        "Fonts": project_root / "assets/fonts",
    }

    results = {}
    for category, path in asset_checks.items():
        if path.exists():
            files = [f.name for f in path.rglob("*") if f.is_file()]
            results[category] = files
        else:
            results[category] = []

    return results


def print_section_header(title: str) -> None:
    """Print a formatted section header."""
    print(f"\n{BLUE}{'=' * 60}{RESET}")
    print(f"{BLUE}{title:^60}{RESET}")
    print(f"{BLUE}{'=' * 60}{RESET}\n")


def main() -> None:
    """Main verification function."""
    print(f"\n{BLUE}The Last Knight Path - Asset Verification{RESET}")
    print("=" * 60)

    # Check directory structure
    print_section_header("Directory Structure")
    dir_results = check_directory_structure()

    all_dirs_exist = True
    for dir_path, exists in dir_results.items():
        if exists:
            print(f"{GREEN}✓{RESET} {dir_path}")
        else:
            print(f"{RED}✗{RESET} {dir_path} {RED}(missing){RESET}")
            all_dirs_exist = False

    if all_dirs_exist:
        print(f"\n{GREEN}All directories present!{RESET}")
    else:
        print(f"\n{YELLOW}Some directories are missing. "
              f"Run setup to create them.{RESET}")

    # Check asset files
    print_section_header("Asset Inventory")
    asset_results = check_asset_files()

    for category, files in asset_results.items():
        print(f"{BLUE}{category}:{RESET}")
        if files:
            print(f"  {GREEN}✓{RESET} Found {len(files)} file(s):")
            for file in sorted(files)[:10]:  # Show first 10 files
                print(f"    - {file}")
            if len(files) > 10:
                print(f"    ... and {len(files) - 10} more")
        else:
            print(f"  {YELLOW}⚠{RESET} No files found - "
                  f"download from ASSETS.md resources")
        print()

    # Summary
    print_section_header("Summary")

    required_assets = {
        "Music": 3,  # menu, gameplay, boss
        "Sound Effects": 10,  # minimum SFX needed
        "Enemy Sprites": 1,  # at least one enemy type
        "Boss Sprites": 1,  # at least one boss
        "Tilesets": 1,  # at least one tileset
        "Fonts": 1,  # at least one font
    }

    missing = []
    for asset_type, min_count in required_assets.items():
        actual_count = len(asset_results.get(asset_type, []))
        if actual_count < min_count:
            missing.append(f"{asset_type} ({actual_count}/{min_count})")

    if missing:
        print(f"{YELLOW}Missing or incomplete assets:{RESET}")
        for item in missing:
            print(f"  - {item}")
        print(f"\n{YELLOW}Refer to ASSETS.md for download links.{RESET}")
    else:
        print(f"{GREEN}All required assets present!{RESET}")

    # Knight sprites check (should already exist)
    knight_files = asset_results.get("Knight Sprites", [])
    if knight_files:
        print(f"\n{GREEN}✓{RESET} Knight sprites verified: "
              f"{len(knight_files)} files")
    else:
        print(f"\n{RED}✗{RESET} Knight sprites missing!")

    print(f"\n{BLUE}{'=' * 60}{RESET}\n")


if __name__ == "__main__":
    main()
