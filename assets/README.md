# Assets Directory

This directory contains all game assets for The Last Knight Path.

## Directory Structure

```
assets/
├── sprites/
│   ├── knight/          # ✓ Player character sprites (already present)
│   ├── enemies/         # Enemy character sprites (download required)
│   └── boss/            # Boss character sprites (download required)
├── tiles/               # Tileset images (download required)
├── maps/                # Tiled map files (.tmx) - create with Tiled
├── audio/
│   ├── music/           # Background music tracks (download required)
│   └── sfx/             # Sound effects (download required)
└── fonts/               # Game fonts (download required)
```

## Quick Start - Downloading Assets

### 1. Read the Asset Guide
See **[ASSETS.md](../ASSETS.md)** in the project root for:
- Curated list of free asset sources
- Direct download links
- License information
- Recommended assets for each category

### 2. Download Priority

#### Essential (Download First):
1. **Tilesets** - At least one main tileset for level design
2. **Music** - 3 tracks: menu, gameplay, boss
3. **Sound Effects** - Basic SFX: jump, attack, hit, damage
4. **Fonts** - At least one pixel/game font

#### Important (Download Second):
5. **Enemy Sprites** - 2-3 enemy types minimum
6. **Boss Sprites** - 1 boss character minimum

### 3. File Naming Conventions

Use consistent naming for easy integration:

**Music Files:**
- `menu.ogg` - Menu screen music
- `gameplay.ogg` - Main gameplay music
- `boss.ogg` - Boss battle music

**Sound Effects:**
- `jump.wav` - Jump sound
- `land.wav` - Landing sound
- `sword_slash.wav` - Sword attack
- `sword_hit.wav` - Hit enemy
- `player_hurt.wav` - Player damage
- `enemy_hurt.wav` - Enemy damage
- `dash.wav` - Dash ability
- `wall_slide.wav` - Wall slide
- `death.wav` - Death sound
- `menu_select.wav` - UI navigation
- `menu_confirm.wav` - UI confirm

**Sprite Directories:**
```
enemies/
├── skeleton/
│   ├── idle.png
│   ├── walk.png
│   ├── attack.png
│   └── death.png
├── goblin/
│   └── [similar structure]
└── bat/
    └── [similar structure]
```

### 4. Verify Your Downloads

Run the verification script to check your progress:

```bash
uv run python scripts/verify_assets.py
```

This will show:
- Which directories exist
- How many files are in each category
- What's still missing

### 5. Update Credits

After downloading assets, update **[CREDITS.md](../CREDITS.md)** with:
- Asset name
- Author/creator
- Source URL
- License type
- File location

## File Format Requirements

| Asset Type | Format | Notes |
|------------|--------|-------|
| Sprites | PNG | With transparency |
| Tilesets | PNG | Organized sprite sheets |
| Music | OGG | Preferred for Pygame (MP3 also works) |
| SFX | WAV/OGG | WAV preferred for short sounds |
| Maps | TMX | Tiled Map Editor format |
| Fonts | TTF/OTF | TrueType or OpenType |

## Recommended Asset Sizes

- **Tilesets**: 16x16 or 32x32 pixels per tile
- **Player/Enemy Sprites**: Match knight sprite scale (~48-64px height)
- **Boss Sprites**: 2-3x larger than player (~128-192px)
- **Background**: Match game resolution (1280x720 or scalable)

## Tools You'll Need

1. **[Tiled Map Editor](https://www.mapeditor.org/)** - Create game maps
   - Free, open-source
   - Download and install to create .tmx files

2. **Image Viewer/Editor** (Optional)
   - Preview sprite sheets
   - Make minor adjustments
   - Options: GIMP (free), Aseprite, Photoshop

3. **Audio Player** (Optional)
   - Preview music and SFX
   - Any audio player works

## Tips for Asset Selection

1. **Maintain Consistent Art Style**
   - Choose assets with similar pixel density
   - Match color palettes (dark medieval theme)
   - Consistent animation frame counts

2. **Check Licenses Carefully**
   - CC0 = No attribution required (easiest)
   - CC-BY = Attribution required (document in CREDITS.md)
   - Avoid "Personal Use Only" for open-source projects

3. **Test Assets Early**
   - Don't download everything at once
   - Test a few assets in-game first
   - Ensure they match the game's aesthetic

4. **Organize as You Go**
   - Rename files consistently
   - Create subdirectories for each asset pack
   - Document sources immediately

## Example: Quick Download Session

Here's a sample workflow to get started quickly:

```bash
# 1. Visit FreePD.com for music
# Download: Medieval theme → rename to menu.ogg
# Download: Battle theme → rename to gameplay.ogg
# Download: Epic theme → rename to boss.ogg
# Place in: assets/audio/music/

# 2. Visit Pixabay Sound Effects
# Search: "8bit jump" → download → rename to jump.wav
# Search: "sword" → download → rename to sword_slash.wav
# Search: "hit" → download → rename to sword_hit.wav
# Place in: assets/audio/sfx/

# 3. Visit itch.io - Medieval tilesets
# Download a CC0 castle/dungeon tileset
# Place in: assets/tiles/

# 4. Visit Google Fonts
# Download "Press Start 2P" font
# Place in: assets/fonts/

# 5. Verify
uv run python scripts/verify_assets.py

# 6. Update CREDITS.md with all sources
```

## Current Status

Knight sprites: ✓ Complete (32 files)

Run `scripts/verify_assets.py` to check other categories.

## Need Help?

- Asset download guide: **ASSETS.md** in project root
- License tracking: **CREDITS.md** in project root
- Issues? Check if asset format matches requirements above

---

**Remember**: Quality over quantity! It's better to have a few cohesive assets than many mismatched ones.
