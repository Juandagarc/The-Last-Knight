# KNIGHT-012: Score Persistence

## Labels
`ai-ready`, `priority-medium`, `persistence`

## Estimate
2 hours

## Dependencies
- KNIGHT-010 (UI Screens)

## Objective
Implement score tracking and JSON persistence.

## Requirements

### 1. ScoreManager
- Track current score
- Track time elapsed
- Load/save high scores
- Top 10 leaderboard

### 2. Files to Create
- src/data/score_manager.py
- tests/test_scores.py
- data/scores.json (template)

### 3. JSON Structure
```json
{
  "high_scores": [
    {
      "name": "AAA",
      "score": 1000,
      "time": 120.5,
      "date": "2025-11-30"
    }
  ]
}
```

## Acceptance Criteria
- [ ] Score increments on enemy kill
- [ ] Time tracks gameplay duration
- [ ] Scores save to JSON
- [ ] High scores load on startup

## Agent-Specific Instructions

### Claude Code Prompt
```
Implement KNIGHT-012 following CLAUDE.md:

1. Create src/data/score_manager.py:
   - current_score, elapsed_time
   - add_score(points)
   - save_high_scores()
   - load_high_scores()
   - get_top_scores(count=10)

2. Create data/scores.json structure

3. Tests in tests/test_scores.py

Handle file not found gracefully.
Use logging instead of print. Include type hints.
```

## Test Cases

| Test ID | Description | Expected Result |
|---------|-------------|-----------------|
| TC-012-1 | Add score | Score increases |
| TC-012-2 | Track time | Time increments |
| TC-012-3 | Save scores | File created |
| TC-012-4 | Load scores | Data retrieved |
| TC-012-5 | Top 10 scores | Sorted correctly |
| TC-012-6 | Missing file | Creates default |
