# KNIGHT-014: Documentation & CI

## Labels
`ai-ready`, `priority-medium`, `documentation`, `devops`

## Estimate
2 hours

## Dependencies
- All previous issues

## Objective
Complete documentation and CI/CD pipeline.

## Requirements

### 1. Documentation
- README.md with full instructions
- CLAUDE.md for AI agents
- API documentation in docstrings
- CONTRIBUTING.md

### 2. CI/CD Pipeline
- GitHub Actions workflow
- Lint, typecheck, test jobs
- Build executable
- Docker build

### 3. Files to Create/Update
- .github/workflows/ci.yml (already exists)
- README.md (update if needed)
- CONTRIBUTING.md (new)
- docs/API.md (new)

## Acceptance Criteria
- [ ] README complete
- [ ] CI pipeline passes
- [ ] Docker builds successfully
- [ ] All badges green

## Agent-Specific Instructions

### Claude Code Prompt
```
Implement KNIGHT-014 following CLAUDE.md:

1. Update README.md with:
   - Full uv commands
   - Architecture overview
   - Contributing guidelines

2. Verify .github/workflows/ci.yml:
   - Lint with flake8
   - Format check with black
   - Type check with mypy
   - Test with pytest + coverage
   - Build Docker image

3. Create CONTRIBUTING.md:
   - Development workflow
   - Code style guidelines
   - PR process

4. Create docs/API.md:
   - Module documentation
   - Class references
   - Function signatures

Use uv for all Python commands in CI.
```

## Test Cases

| Test ID | Description | Expected Result |
|---------|-------------|-----------------|
| TC-014-1 | README complete | All sections filled |
| TC-014-2 | CI lint job | Passes |
| TC-014-3 | CI test job | Passes |
| TC-014-4 | Docker build | Succeeds |
| TC-014-5 | All badges | Display correctly |
| TC-014-6 | CONTRIBUTING.md | Guidelines clear |
