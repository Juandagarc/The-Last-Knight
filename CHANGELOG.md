# CHANGELOG


## v0.5.0 (2025-11-30)

### Features

- **systems**: Implement Physics and Collision systems for KNIGHT-004
  ([`832e88b`](https://github.com/Juandagarc/The-Last-Knight/commit/832e88b66cc9709addf3927d02e605dfd49cfb20))

Co-authored-by: adriancho91s <72105546+adriancho91s@users.noreply.github.com>

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
