# CHANGELOG


## v0.10.0 (2025-12-02)

### Bug Fixes

- **ai**: Fix black formatting and mypy type errors in ai.py
  ([`904a145`](https://github.com/Juandagarc/The-Last-Knight/commit/904a145545909707e3e72d1f51da2be13a8bf19b))

Co-authored-by: adriancho91s <72105546+adriancho91s@users.noreply.github.com>

### Features

- **enemies**: Implement Enemy AI & Patrol with intelligent utility-based AI (KNIGHT-007)
  ([`87b33d8`](https://github.com/Juandagarc/The-Last-Knight/commit/87b33d8aeccbfd2e88f9d153fbf0f1041fdbfb95))

Co-authored-by: adriancho91s <72105546+adriancho91s@users.noreply.github.com>

### Refactoring

- **ai**: Address code review feedback - replace magic numbers with constants
  ([`9282aae`](https://github.com/Juandagarc/The-Last-Knight/commit/9282aae819ed482607d487a86119e5a3e3ac7f1b))

Co-authored-by: adriancho91s <72105546+adriancho91s@users.noreply.github.com>


## v0.9.0 (2025-12-02)

### Features

- Implement UI screens and HUD system (KNIGHT-010)
  ([`961421a`](https://github.com/Juandagarc/The-Last-Knight/commit/961421af28b743e85cb547764c7f546ab1613126))

Co-authored-by: Juandagarc <136721434+Juandagarc@users.noreply.github.com>


## v0.8.0 (2025-11-30)

### Chores

- Initial plan for KNIGHT-006
  ([`70c4175`](https://github.com/Juandagarc/The-Last-Knight/commit/70c41750ea5dfeadc7834e6d23408c115826b9bd))

Co-authored-by: adriancho91s <72105546+adriancho91s@users.noreply.github.com>

### Features

- **combat**: Implement combat system with attack state and combos (KNIGHT-006)
  ([`ca750f7`](https://github.com/Juandagarc/The-Last-Knight/commit/ca750f7361cf5cf19af1cf3b7428ee3fb067df92))

Co-authored-by: adriancho91s <72105546+adriancho91s@users.noreply.github.com>

### Refactoring

- **combat**: Address code review feedback - clean up hitbox method and add constant
  ([`515697c`](https://github.com/Juandagarc/The-Last-Knight/commit/515697ca5d6126d9e660184b60d4e68815982fb2))

Co-authored-by: adriancho91s <72105546+adriancho91s@users.noreply.github.com>


## v0.7.0 (2025-11-30)


## v0.6.0 (2025-11-30)


## v0.5.0 (2025-11-30)

### Chores

- Initial plan for KNIGHT-005
  ([`08b18b7`](https://github.com/Juandagarc/The-Last-Knight/commit/08b18b7574f6f58a7d059a81b07d57804c81b87e))

Co-authored-by: adriancho91s <72105546+adriancho91s@users.noreply.github.com>

### Documentation

- Add asset credits and verification tools
  ([`2969555`](https://github.com/Juandagarc/The-Last-Knight/commit/296955574d94cf32153253356fcb9381e830bc0f))

Add documentation and tooling for asset management: - CREDITS.md: Complete attribution for all
  downloaded assets with sources, licenses, authors, and file locations - MAPS_CREATED.md: Detailed
  map documentation with layouts, features, and usage instructions for each level -
  scripts/verify_assets.py: Python script to verify asset completeness and generate inventory
  reports

All assets properly credited with CC0, CC-BY, OFL, and other licenses.

- **assets**: Add documentation for asset organization and maps
  ([`bf403b4`](https://github.com/Juandagarc/The-Last-Knight/commit/bf403b4e0d9ab7787de68b26943c1b41c26bff74))

Add comprehensive documentation: - assets/README.md: Asset directory structure, file naming
  conventions, quick start guide, and verification instructions - assets/maps/README.md: Map
  structure, layer details, Tiled usage guide, coordinate systems, and loading instructions for
  pytmx

Includes examples for loading assets in Pygame and editing maps in Tiled.

### Features

- **audio**: Add background music tracks
  ([`c1206b3`](https://github.com/Juandagarc/The-Last-Knight/commit/c1206b314cc87d744ac84da82cd32d2d83d6e53a))

Add three CC0 licensed music tracks from FreePD.com: - menu.mp3: Dancing at the Inn by Kevin MacLeod
  - gameplay.mp3: Celebration by Alexander Nakarada - boss.mp3: Epic Boss Battle by Rafael Krux

All tracks are public domain and suitable for medieval fantasy platformer.

- **audio**: Add sound effects for gameplay
  ([`e76c53b`](https://github.com/Juandagarc/The-Last-Knight/commit/e76c53b3306417548a52463aa979e9d0d5079ebb))

Add comprehensive SFX library including: - Player movement sounds (jump, land, footstep, wall
  climb/slide) - Combat sounds (sword slash, sword hit, player/enemy hurt) - UI sounds (menu
  select/confirm, clicks, switches) - 51 additional UI variations from Kenney UI SFX pack

Sources: - 12 Player Movement SFX (CC-BY 4.0) from OpenGameArt - 51 UI Sound Effects (CC0) by Kenney
  from OpenGameArt

- **fonts**: Add game fonts for UI and titles
  ([`fe37856`](https://github.com/Juandagarc/The-Last-Knight/commit/fe3785630e3290bccb2872cd32beeb8bdf5c3c08))

Add two fonts for game interface: - Press Start 2P: Classic 8-bit pixel font for UI (OFL by
  CodeMan38) - Cinzel: Medieval-themed serif font for titles (OFL by Natanael Gama)

Both fonts from Google Fonts with Open Font License.

- **fsm**: Implement Player FSM with movement states (KNIGHT-005)
  ([`94b6b39`](https://github.com/Juandagarc/The-Last-Knight/commit/94b6b394e49bcac125cde7703cf029f909ecaa9b))

Co-authored-by: adriancho91s <72105546+adriancho91s@users.noreply.github.com>

- **maps**: Create three playable game levels
  ([`4c04abb`](https://github.com/Juandagarc/The-Last-Knight/commit/4c04abbc5d969c2272333aa8aa0135b171654e5d))

Add Tiled map files (.tmx) for platformer gameplay: - level_01_tutorial.tmx: 40x23 tutorial level
  with basic platforming (1280x736px) - level_02_dungeon.tmx: 50x30 advanced dungeon level with
  challenges (1600x960px) - level_03_boss_arena.tmx: 30x20 enclosed boss battle arena (960x640px)

All maps use 32x32 tile size with castle_tileset.png and include 4 layers: Background, Platforms,
  Decorations, and Collision.

- **sprites**: Add boss character sprites
  ([`3d1e32c`](https://github.com/Juandagarc/The-Last-Knight/commit/3d1e32cf7f0769331596135cc90c5bd744ae0c4f))

Add LPC Medieval fantasy character sprites for boss encounters. Includes modular skeleton/knight
  sprites with full animation sets, armor variations, and weapon options. Can be scaled 2x for boss
  size.

Source: wulax on OpenGameArt.org

License: CC-BY-SA 3.0 and GPL 3.0

- **sprites**: Add enemy character sprites
  ([`d94c074`](https://github.com/Juandagarc/The-Last-Knight/commit/d94c074fdd0e2de1d6727ba2c4c17aac358af1fe))

Add 4 enemy types with animations: - Skeleton: 32x32 pixel art with idle, attack, walk (CC0 by tbbk)
  - Goblin: 32x32 animated with idle, run, attack, death (CC0 by thekingphoenix) - Bat: 32x32 flying
  enemy with 5 flight frames (CC0 by MoikMellah) - Slime: Animated with idle, movement, attack, hurt
  (CC0 by rvros)

All sprites sourced from OpenGameArt.org with CC0 public domain license.

- **systems**: Implement Physics and Collision systems for KNIGHT-004
  ([`832e88b`](https://github.com/Juandagarc/The-Last-Knight/commit/832e88b66cc9709addf3927d02e605dfd49cfb20))

Co-authored-by: adriancho91s <72105546+adriancho91s@users.noreply.github.com>

- **tiles**: Add dungeon and castle tilesets
  ([`ae76fe8`](https://github.com/Juandagarc/The-Last-Knight/commit/ae76fe8f6c09d788aebbdaa0ada368605dcb49e8))

Add 32x32 tilesets for platformer level design: - Dungeon tileset with walls, corners, and floor
  tiles (CC0 by Enyph Games) - Castle platformer tileset with 20 decoration objects (CC0 by Vicplay)

Both tilesets sourced from OpenGameArt.org with public domain licenses.

### Refactoring

- Replace magic numbers with constants from settings
  ([`20b243b`](https://github.com/Juandagarc/The-Last-Knight/commit/20b243b91dd0e1b03fa7a9a940c0c2fefc8292f0))

Co-authored-by: adriancho91s <72105546+adriancho91s@users.noreply.github.com>

- **tests**: Remove unused pytest import from test_collision.py
  ([`672c059`](https://github.com/Juandagarc/The-Last-Knight/commit/672c0590b38e3685ccd1b91555c0169e154c63ca))


## v0.4.0 (2025-11-30)

### Chores

- Initial plan for KNIGHT-003
  ([`d7152d9`](https://github.com/Juandagarc/The-Last-Knight/commit/d7152d9d5155b195b807e187384b51e533ba783f))

Co-authored-by: adriancho91s <72105546+adriancho91s@users.noreply.github.com>

### Features

- **assets**: Add knight sprite assets and animations configuration
  ([`2efc21a`](https://github.com/Juandagarc/The-Last-Knight/commit/2efc21a946723164ccaf3584b8b9b3c70e465761))

- **entities**: Add knight sprite implementation with 30 animations and resource management
  ([`eb025a5`](https://github.com/Juandagarc/The-Last-Knight/commit/eb025a587b532317729995345c1179c2d267bf55))

- **entities**: Enhance ResourceManager with animation caching and loading methods
  ([`676ce02`](https://github.com/Juandagarc/The-Last-Knight/commit/676ce02d86f3f6a3a6370ef8bd409d9815cdcd9b))

- **entities**: Implement Entity base class and Animation system (KNIGHT-003)
  ([`9dadcf3`](https://github.com/Juandagarc/The-Last-Knight/commit/9dadcf33ea646c1c804981c39b49001376332d7a))

Co-authored-by: adriancho91s <72105546+adriancho91s@users.noreply.github.com>

- **tests**: Add comprehensive test suite for knight sprite animations and resource management
  ([`ff26cc9`](https://github.com/Juandagarc/The-Last-Knight/commit/ff26cc9ef44caddf0fdde5f390a888439fb9f670))

- **tests**: Add test script for knight sprite loading and animation display
  ([`ddc1637`](https://github.com/Juandagarc/The-Last-Knight/commit/ddc1637d46cf79e4fb5eea7a23095376b86d1046))


## v0.3.0 (2025-11-30)

### Bug Fixes

- **resource-manager**: Handle FileNotFoundError in load_sound
  ([`e4eef3d`](https://github.com/Juandagarc/The-Last-Knight/commit/e4eef3d7b1d0ce512fde31132a09148ebe7ceaa1))

Co-authored-by: Juandagarc <136721434+Juandagarc@users.noreply.github.com>

### Chores

- Initial plan for KNIGHT-002
  ([`5b98ea2`](https://github.com/Juandagarc/The-Last-Knight/commit/5b98ea2f9e244b568c242587af14b809488102e8))

Co-authored-by: Juandagarc <136721434+Juandagarc@users.noreply.github.com>

### Features

- **core**: Implement Game singleton and ResourceManager
  ([`8e0f398`](https://github.com/Juandagarc/The-Last-Knight/commit/8e0f39864df3f57dcb9f17384493f8bbb31589bc))

Co-authored-by: Juandagarc <136721434+Juandagarc@users.noreply.github.com>


## v0.2.1 (2025-11-30)


## v0.2.0 (2025-11-30)

### Bug Fixes

- Update semantic-release configuration to simplify build process
  ([`a5e8d72`](https://github.com/Juandagarc/The-Last-Knight/commit/a5e8d72f7d65bae6c8354b36750414f045a6bf7e))

- Update semantic-release installation and remove verbose flag
  ([`2a50731`](https://github.com/Juandagarc/The-Last-Knight/commit/2a50731d2a44881dc59df6cca3fe7b2cc841dfae))

### Chores

- Add verbose flag to semantic release command
  ([`331753b`](https://github.com/Juandagarc/The-Last-Knight/commit/331753b35ab22ba5d3cbb3197894f14723c81fce))

- Remove redundant semantic-release installation step and enhance configuration
  ([`5345b86`](https://github.com/Juandagarc/The-Last-Knight/commit/5345b8638d012f8fea54ce960d2b533f8cefb374))

### Features

- Enhance Docker workflow with build and push steps
  ([`6495248`](https://github.com/Juandagarc/The-Last-Knight/commit/6495248b3a4aabce02ba55287b75399ea0bff94b))


## v0.1.0 (2025-11-30)

### Bug Fixes

- Update dependency installation command to use --all-extras flag
  ([`3ff04bc`](https://github.com/Juandagarc/The-Last-Knight/commit/3ff04bc2c0c4d3e8276f8fbba925cf5793b1fa02))

- Update dependency installation command to use --extra dev flag
  ([`514daaa`](https://github.com/Juandagarc/The-Last-Knight/commit/514daaa90109d8dc6787b3bf73e255201e71ec33))

- Update python-semantic-release version and adjust installation commands
  ([`f96586c`](https://github.com/Juandagarc/The-Last-Knight/commit/f96586ced5182b7d2097ce92fad8737884d01dc1))

### Chores

- Add KNIGHT stories and write initial documentation of the project
  ([`5fe243d`](https://github.com/Juandagarc/The-Last-Knight/commit/5fe243daabd5695548561441b2e8641009053fea))

### Features

- Add .gitkeep file to data directory for version control
  ([`3ed57df`](https://github.com/Juandagarc/The-Last-Knight/commit/3ed57dfa29578d9baf71871a8c6ac629a69fd46e))

- Add asset directories and remove unused player assets
  ([`43c8824`](https://github.com/Juandagarc/The-Last-Knight/commit/43c882423d569006ab5642f319869f945f5efe72))

- Add automated semantic release workflow and update dependencies
  ([`6475457`](https://github.com/Juandagarc/The-Last-Knight/commit/64754579230cc22a24d4a832da3d9a0f424f1621))

- Add CI workflow for continuous integration and testing
  ([`00244cc`](https://github.com/Juandagarc/The-Last-Knight/commit/00244cc29688ff4523b08d7d63fcd2cfa5a4d473))

- Add comprehensive testing guidelines and framework setup for The Last Knight Path
  ([`9e68134`](https://github.com/Juandagarc/The-Last-Knight/commit/9e6813489bad3fe143db0bc790ba815eaef17141))

- Introduced a new instructions file detailing testing guidelines using pytest. - Established test
  file organization and pytest fixture examples. - Outlined testing patterns for entities, states,
  physics, and collisions. - Added coverage requirements and assertions best practices. - Documented
  running tests and specific command usage. - Created CLAUDE.md for project overview, architecture,
  and development commands. - Developed ORCHESTRATION.md to outline autonomous development
  approaches and agent protocols. - Implemented TRACKING.md for issue status and agent comparison
  metrics. - Compiled agents/claude-code-prompts.md for structured prompts for AI agents.

- Add Dockerfile and docker-compose.yml for containerized game setup
  ([`72349a8`](https://github.com/Juandagarc/The-Last-Knight/commit/72349a83aaad4f30316dce160864570de55e132e))

- Add initial game structure, settings, and logging setup
  ([`3a5277e`](https://github.com/Juandagarc/The-Last-Knight/commit/3a5277ebf8b5bac7949ab0edb76feca5aa77c239))

- Remove configuration, requirements, and startup script files
  ([`8fecceb`](https://github.com/Juandagarc/The-Last-Knight/commit/8feccebb6f215f975bccc363c5f240e57f4d49a9))

- Update .gitignore to include additional file types and directories for better project management
  ([`c9785da`](https://github.com/Juandagarc/The-Last-Knight/commit/c9785da44a815e4fa821d27aae517eba08296b92))

### Refactoring

- Add uv.lock to avoid errors on new dependencies
  ([`7e92198`](https://github.com/Juandagarc/The-Last-Knight/commit/7e9219811b3087dcd9d1c034d4e57f67f3fd55cc))
