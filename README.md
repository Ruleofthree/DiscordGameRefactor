# Discord Game Refactor

This project is for learning Python refactoring and improving the structure of an older Discord game bot.

## Folder Layout

- original: legacy bot code kept for compatibility during refactor. Files here may be edited only to delegate behavior into src/ while preserving legacy behavior.
- src: cleaned-up Python source code
- tests: test files
- data: JSON game data and sample files

## Refactor Rules

- Avoid rewriting original/ directly unless extracting behavior into src/ or preserving legacy wrapper compatibility.
- Original behavior must be protected by tests before changing legacy functions.
- New cleaned-up code goes in src/.
- Tests go in tests/.
- JSON data used by the refactored code goes in data/.
- Commit after each successful setup or refactor step.
