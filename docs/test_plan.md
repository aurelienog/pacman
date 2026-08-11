# Acceptance Test Plan

## 1. Functional Tests

Functional tests validate complete user-facing game scenarios.

| Test Case | Description         | Input / Trigger                                    | Expected Outcome                                                                            | Pass/Fail |
| :-------- | :------------------ | :------------------------------------------------- | :------------------------------------------------------------------------------------------ | :-------: |
| **TC-01** | Start New Game      | Confirm from main menu                             | A new game starts with the configured level, player, ghosts, collectibles, score and timer. |    PASS   |
| **TC-02** | Pause and Resume    | Press pause while playing, then pause again        | The game enters `PAUSED` and can return to `PLAYING` without losing the current game state. |    PASS   |
| **TC-03** | Return to Main Menu | Select return-to-menu while playing                | The session returns to `MAIN_MENU` and displays the start message.                          |    PASS   |
| **TC-04** | Level Completion    | Collect all collectibles or skip the current level | The next level starts while preserving the player's score and remaining lives.              |    PASS   |
| **TC-05** | Game Over           | Lose the player's final life                       | The session enters `GAME_OVER` and preserves the final score.                               |    PASS   |
| **TC-06** | Victory             | Complete the final configured level                | The session enters `VICTORY` and displays the final score.                                  |    PASS   |

## 2. Integration Tests

Integration tests validate the interaction between the main application components and external/persistent dependencies.

| Test Case | Description              | Components                                                  | Expected Outcome                                                                                                                   | Pass/Fail |
| :-------- | :----------------------- | :---------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------- | :-------: |
| **IT-01** | Game Session Integration | `GameSession` + application components                      | A game session can be started and its main state transitions work correctly using the configured maze factory and game components. |    PASS   |
| **IT-02** | Highscore Persistence    | `ScoreRegistry` + `JsonHighscoreRepository`                 | A valid high score is saved to JSON and can be loaded again with the same name and score.                                          |    PASS   |
| **IT-03** | Maze Adapter             | `AmazingMazeFactory` + A-Maze-ing generator + domain `Maze` | A generated external maze is correctly validated and converted into the domain `Maze`; invalid or unsolvable mazes are rejected.   |    PASS   |


## 3. Unit Tests

Unit tests validate individual components and isolated game rules.

The current unit-test suite covers:

* configuration loading and normalization;
* pathfinding and nearest-walkable resolution;
* ghost AI and personality targeting;
* ghost movement in `CHASE`, `FRIGHTENED` and `RESPAWNING` modes;
* player movement rules;
* item placement;
* collision handling;
* level loading;
* highscore validation;
* JSON highscore loading and saving;
* snapshot generation.

The unit tests verify individual behaviours independently from the complete user flow.

## 4. Bug Tracking Log

|   Bug ID   | Description                                                           | Severity | Resolution / Fix                                                                                                |
| :--------: | :-------------------------------------------------------------------- | :------: | :-------------------------------------------------------------------------------------------------------------- |
| **BUG-01** | Traceback when the highscore file is missing or invalid               |   High   | `JsonHighscoreRepository` catches file/JSON errors and returns an empty score list.                             |
| **BUG-02** | Ghost movement did not correctly handle walls and unreachable targets |  Medium  | Improved BFS pathfinding, fallback movement and target handling.                                                |
| **BUG-03** | Ghosts could move while respawning                                    |  Medium  | `move_ghosts()` skips ghosts in `RESPAWNING` mode until the respawn timer expires.                              |
| **BUG-04** | Frightened ghosts did not correctly move away from the player         |  Medium  | Added explicit frightened movement behaviour that selects a legal move maximizing the distance from the player. |
| **BUG-05** | Frightened ghosts did not transition back to chase mode correctly     |  Medium  | `update_world()` manages the frightened timer and restores ghosts to `CHASE` when it expires.                   |
| **BUG-06** | Collision timing could feel inconsistent with interpolated rendering  |  Medium  | Logical cell occupation is determined using movement progress before collision resolution.                      |
| **BUG-07** | Collectibles could be placed on decorative `42` cells                 |  Medium  | `place_items()` excludes cells identified by `Maze.is_42_art()`.                                                |
| **BUG-08** | Collectibles could be placed on non-traversable cells                 |  Medium  | `place_items()` only considers valid walkable cells as Pac-Gum candidates.                                      |
| **BUG-09** | Out-of-range level dimensions were not normalized consistently        |  Medium  | `ConfigLoader` clamps values to the configured limits before creating `LevelConfig`.                            |
| **BUG-10** | Even maze dimensions could break maze-generation requirements         |    Low   | Configured level dimensions are normalized to odd values after clamping.                                        |

---

*The acceptance tests are considered **PASS** when the corresponding automated tests pass and no unhandled exception or invalid game state is produced.*
