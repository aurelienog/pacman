# Acceptance Test Plan

## 1. Mandatory Functional Tests

| Test Case | Description | Input / Trigger | Expected Outcome | Pass/Fail |
| :--- | :--- | :--- | :--- | :---: |
| **TC-01** | Config File Loading | Valid `config.json` | Game loads levels and parameters seamlessly. | PASS |
| **TC-02** | Faulty Config Fallback | Missing keys / Invalid values | Clamps to safe defaults, logs error, no crash/traceback. | PASS |
| **TC-03** | Ghost Edible State | Super-pacgum consumed | Ghosts change state, turn edible/scared, run away. | PASS |
| **TC-04** | Cheat Mode Activation | Pressing cheat hotkey | Enables invincibility / level skip / freeze. | PASS |
| **TC-05** | Highscore Persistence | Finish game with high score | Top 10 updated and persisted in JSON file. | PASS |

## 2. Bug Tracking Log

| Bug ID | Description | Severity | Resolution / Fix | Fixed By |
| :---: | :--- | :---: | :--- | :---: |
| **BUG-01** | Traceback on missing highscore file | High | Added `try-except FileNotFoundError` returning empty list | Dev 1 |
| **BUG-02** | Ghosts passing through inner corners | Medium | Corrected hitboxes grid math in `maze.py` | Dev 2 |