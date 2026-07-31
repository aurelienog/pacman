# Project Retrospective & Blocking Points

## 1. Summary of Blocking Points
* **Issue:** `A-Maze-ing` package interface didn't match initial assumptions regarding cell types.
  * **Resolution:** Refactored `MazeAdapter` to convert raw output into an internal grid matrix, ensuring strict decoupling from external logic.
* **Issue:** `mypy` strict mode failing on dynamic JSON parsing for comments.
  * **Resolution:** Added custom regex filtering step prior to JSON parsing, enforcing typed dictionaries.

## 2. Conflict Handling & Lessons Learned
* **Communication:** Daily standup syncs (10 mins) kept both developers aligned on interface contracts.
* **Code Standard:** Enforcing `flake8` and `mypy` via Makefile early on prevented massive refactoring debts at the end of the project.