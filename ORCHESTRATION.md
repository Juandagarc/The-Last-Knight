# The Last Knight Path - Autonomous Development Guide

## Overview

This document orchestrates the autonomous development of "The Last Knight Path" - a 2D Action-Platformer game using Python and Pygame. The guide supports three AI agent approaches to test which method produces the best results for game development.

## Development Approaches

| Approach | Tool | Trigger | Best For |
|----------|------|---------|----------|
| **A** | GitHub Copilot Agent | Repository creation + Issues | Initial scaffolding, PR-based workflow |
| **B** | Claude Code | Direct terminal commands | Complex FSM logic, debugging, refactoring |
| **C** | GitHub Actions + Codex | Automated on issue assignment | Repetitive patterns, standardized code |

## Issue Labels

Use these labels when opening or triaging issues:

| Label | Purpose | Referenced Issues |
|-------|---------|-------------------|
| `ai-ready` | Clearly scoped for AI agent execution | All KNIGHT-001 → KNIGHT-014 |
| `priority-critical` | Must be addressed immediately | KNIGHT-001, KNIGHT-002, KNIGHT-003 |
| `priority-high` | High urgency backlog item | KNIGHT-004 through KNIGHT-008 |
| `priority-medium` | Medium urgency item | KNIGHT-009 through KNIGHT-014 |
| `infrastructure` | Setup, config, or environment work | KNIGHT-001 |
| `core` | Core game systems | KNIGHT-002, KNIGHT-003, KNIGHT-004 |
| `player` | Player entity and mechanics | KNIGHT-005, KNIGHT-006 |
| `fsm` | State machine implementation | KNIGHT-005 |
| `combat` | Combat system | KNIGHT-006 |
| `enemies` | Enemy AI and behavior | KNIGHT-007 |
| `boss` | Boss implementation | KNIGHT-008 |
| `levels` | Level design and loading | KNIGHT-009 |
| `ui` | User interface screens | KNIGHT-010 |
| `audio` | Sound and music | KNIGHT-011 |
| `persistence` | Save/load functionality | KNIGHT-012 |
| `testing` | Automated test coverage | KNIGHT-013 |
| `documentation` | Docs, guides, README | KNIGHT-014 |
| `devops` | CI/CD, pipelines | KNIGHT-014 |

## Repository Setup

### Step 1: Clone and Configure

```bash
git clone https://github.com/your-username/the-last-knight-path.git
cd the-last-knight-path

# Install dependencies with uv
uv sync

# Install with dev dependencies
uv sync --extra dev
```

### Step 2: Create GitHub Issues

Create all issues from `issues/` directory using GitHub CLI:

```bash
# Install GitHub CLI if needed
# macOS: brew install gh
# Ubuntu: sudo apt install gh

# Authenticate
gh auth login

# Create all issues
for file in issues/*.md; do
  title=$(head -1 "$file" | sed 's/# //')
  gh issue create --title "$title" --body-file "$file" --label "ai-ready"
done
```

## Development Phases

### Phase 1: Foundation (Issues 001-004)

**Goal**: Establish project infrastructure and core systems.

| Issue | Title | Est. Time | Dependencies |
|-------|-------|-----------|--------------|
| KNIGHT-001 | Project Initialization | 2h | None |
| KNIGHT-002 | Core Game Loop | 2h | KNIGHT-001 |
| KNIGHT-003 | Entity System | 3h | KNIGHT-002 |
| KNIGHT-004 | Physics & Collision | 3h | KNIGHT-003 |

**Total Phase Time**: 10 hours

### Phase 2: Player Mechanics (Issues 005-006)

**Goal**: Implement complete player with FSM and combat.

| Issue | Title | Est. Time | Dependencies |
|-------|-------|-----------|--------------|
| KNIGHT-005 | Player FSM | 4h | KNIGHT-004 |
| KNIGHT-006 | Combat System | 4h | KNIGHT-005 |

**Total Phase Time**: 8 hours

### Phase 3: Enemies & Boss (Issues 007-008)

**Goal**: Add adversaries with AI behaviors.

| Issue | Title | Est. Time | Dependencies |
|-------|-------|-----------|--------------|
| KNIGHT-007 | Enemy AI | 3h | KNIGHT-004 |
| KNIGHT-008 | Boss Battle | 4h | KNIGHT-007 |

**Total Phase Time**: 7 hours

### Phase 4: World & UI (Issues 009-010)

**Goal**: Create levels and user interface.

| Issue | Title | Est. Time | Dependencies |
|-------|-------|-----------|--------------|
| KNIGHT-009 | Level Loading | 3h | KNIGHT-004 |
| KNIGHT-010 | UI Screens | 3h | KNIGHT-002 |

**Total Phase Time**: 6 hours

### Phase 5: Polish (Issues 011-014)

**Goal**: Add audio, persistence, tests, and documentation.

| Issue | Title | Est. Time | Dependencies |
|-------|-------|-----------|--------------|
| KNIGHT-011 | Audio System | 2h | KNIGHT-002 |
| KNIGHT-012 | Score Persistence | 2h | KNIGHT-010 |
| KNIGHT-013 | Test Coverage | 3h | All previous |
| KNIGHT-014 | Documentation & CI | 2h | All previous |

**Total Phase Time**: 9 hours

**Grand Total**: ~40 hours

## Agent Execution Protocols

### GitHub Copilot Protocol

1. Navigate to Issues tab in repository
2. Open issue to implement
3. Click "Assign to Copilot" or invoke @github-copilot
4. Review generated PR
5. Request changes or merge

### Claude Code Protocol

1. Open Claude Code in repository root
2. Reference issue with exact requirements
3. Use prompt from `agents/claude-code-prompts.md`
4. Review and test changes
5. Commit when satisfied

### Quality Checklist

Before marking any issue complete:

- [ ] Code follows project style (snake_case files, type hints, logging)
- [ ] All existing tests pass: `uv run pytest tests/ -v`
- [ ] New functionality has tests
- [ ] No linting errors: `uv run flake8 src/`
- [ ] Type checking passes: `uv run mypy src/`
- [ ] Documentation updated if needed

## Comparison Metrics

Track these metrics for each agent approach:

| Metric | Description |
|--------|-------------|
| Time to PR | Minutes from issue assignment to PR creation |
| First-Pass Success | Did it pass tests on first attempt? |
| Code Quality | Adherence to style guide (1-5) |
| Test Coverage | Percentage of new code tested |
| Manual Fixes | Number of corrections needed |

## Troubleshooting

### Common Issues

**Pygame not initializing in tests**
```python
# Ensure conftest.py has session-scoped fixture
@pytest.fixture(scope="session", autouse=True)
def pygame_init():
    pygame.init()
    yield
    pygame.quit()
```

**Import errors**
```bash
# Make sure you're running from project root
uv run pytest tests/ -v
```

**Type checking failures**
```bash
# Install stubs for pygame
uv add --dev pygame-stubs
```
