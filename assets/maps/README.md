# Game Maps

This directory contains Tiled map files (.tmx) for The Last Knight Path levels.

## Available Maps

### 1. level_01_tutorial.tmx
**Dimensions**: 40x23 tiles (1280x736 pixels)
**Type**: Tutorial/Intro Level
**Description**: Simple platforming level to introduce basic mechanics
**Features**:
- Basic platform layout with gaps for jumping practice
- Progressive difficulty (platforms get farther apart)
- Ground floor with platforms at multiple heights
- Suitable for teaching: jump, run, fall mechanics

**Layout**:
- Starting area on left with small gap
- Mid-level platforms for jump practice
- Higher platforms to introduce double-jump or wall mechanics
- Safe ground level throughout

---

### 2. level_02_dungeon.tmx
**Dimensions**: 50x30 tiles (1600x960 pixels)
**Type**: Main Dungeon Level
**Description**: Larger, more challenging platformer level
**Features**:
- Vertical and horizontal platforming challenges
- Multiple pathways and routes
- Platforms at varying heights requiring precise jumping
- More complex layout for advanced movement

**Layout**:
- Walls on both sides creating vertical climb sections
- Scattered platforms requiring wall-jump or dash
- Mid-level platforms for combat encounters
- Longer gaps between platforms

---

### 3. level_03_boss_arena.tmx
**Dimensions**: 30x20 tiles (960x640 pixels)
**Type**: Boss Battle Arena
**Description**: Enclosed arena for boss fights
**Features**:
- Walled arena (no escape!)
- Two small platforms for tactical positioning
- Large open floor space for combat
- Simple layout focuses attention on boss

**Layout**:
- Solid walls on all sides
- Two elevated platforms on left and right (middle height)
- Open central area for boss movement
- Minimal distractions for intense combat

---

## Map Structure

All maps use the standard 4-layer structure:

### Layer 1: Background
- Visual background elements
- Non-interactive decorations
- Typically empty (no collision)

### Layer 2: Platforms
- Main gameplay tiles
- Platform surfaces
- Visible elements player interacts with

### Layer 3: Decorations
- Foreground decorative elements
- Props, furniture, detail objects
- Non-colliding visual enhancements

### Layer 4: Collision (Hidden)
- Collision detection layer
- Invisible in-game
- Used by physics system for solid tiles
- Same data as Platforms layer

---

## Tileset Used

All maps use: **castle_tileset.png** (32x32 tiles)
- Location: `../tiles/castle_tileset.png`
- Tile size: 32x32 pixels
- Total tiles: 20 tiles (10x2 grid)

---

## Opening Maps in Tiled

1. Install [Tiled Map Editor](https://www.mapeditor.org/)
2. Open any `.tmx` file
3. The tileset will automatically load from `../tiles/castle_tileset.png`

---

## Editing Maps

### To modify existing maps:
1. Open in Tiled
2. Select the layer you want to edit
3. Use the stamp tool to paint tiles
4. Save the file

### To create new maps:
1. File → New → New Map
2. Settings:
   - Orientation: Orthogonal
   - Tile layer format: CSV
   - Tile size: 32x32
   - Map size: Your choice (40x23 is good for standard level)
3. Add tileset: Map → Add External Tileset
4. Browse to `castle_tileset.png`
5. Create 4 layers: Background, Platforms, Decorations, Collision
6. Paint your level!
7. Save as `.tmx` in this directory

---

## Map Coordinates

Tile coordinate system:
- (0, 0) = Top-left corner
- X increases to the right
- Y increases downward

Pixel coordinates:
- Multiply tile coords by 32 for pixel position
- Example: Tile (10, 5) = Pixel (320, 160)

---

## Loading Maps in Game

Maps are loaded using the `pytmx` library:

```python
import pytmx

# Load map
tmx_data = pytmx.load_pygame("assets/maps/level_01_tutorial.tmx")

# Get tile at position
tile = tmx_data.get_tile_image(x, y, layer_index)

# Get collision layer
collision_layer = tmx_data.get_layer_by_name("Collision")

# Iterate through tiles
for layer in tmx_data.visible_layers:
    for x, y, image in layer.tiles():
        # Render tile at (x*32, y*32)
```

---

## Map Testing Tips

When testing maps:
1. Check platform spacing (can player jump between them?)
2. Verify collision layer matches platform layer
3. Test spawn points (where does player start?)
4. Ensure level has an exit/goal
5. Check for impossible jumps or soft-locks
6. Test with all player abilities (jump, dash, wall-climb)

---

## Future Map Ideas

Consider creating:
- **level_01b_advanced_tutorial.tmx** - Wall-jump and dash tutorial
- **level_04_castle_exterior.tmx** - Outdoor castle level
- **level_05_throne_room.tmx** - Final boss arena
- **level_secret_01.tmx** - Hidden bonus area

---

**Created**: 2025-11-30
**Format**: Tiled TMX (XML-based)
**Compatible with**: Pygame + pytmx
