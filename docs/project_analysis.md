## Team Organization & Task Distribution

### Role Matrix / RACI:

| Developer       | Main Responsibilities                                                                                      |
| --------------- | ---------------------------------------------------------------------------------------------------------- |
| **aunoguei** |  Configuration loader, game logic, ghost AI, pathfinding, collision system, gameplay mechanics, persistence layer and testing|
| **oshtohri** |  A-Maze-ing adapter, domain models, Pygame renderer, UI, assets, menus, packaging and documentation. |

### Collaboration Strategy

Development was organised around architectural layers rather than gameplay features, allowing both developers to work in parallel with minimal merge conflicts.

Interfaces between the game engine and the rendering layer were defined before implementation, reducing coupling and enabling independent development. Architectural decisions were discussed through regular peer reviews until consensus was reached, while continuous integration with Git ensured frequent synchronization and early detection of integration issues.

## Risk Analysis & Mitigation Matrix

|  Risk ID | Risk Description                                                       | Severity | Likelihood | Mitigation Strategy                                                                                                         |
| :------: | ---------------------------------------------------------------------- | :------: | :--------: | --------------------------------------------------------------------------------------------------------------------------- |
| **R-01** | External package incompatibility (`A-Maze-ing`).                       |   High   |   Medium   | Isolate the dependency behind `MazeAdapter`, validating and converting external data into the internal representation.      |
| **R-02** | Rendering becoming coupled with gameplay logic.                        |   High   |    High    | Keep rendering completely independent through immutable snapshots while the engine operates only on logical grid positions. |
| **R-03** | Ghost AI complexity.                |  Medium  |    High    | Replace the initial Manhattan-distance heuristic with BFS pathfinding and independent targeting strategies for each ghost.  |
| **R-04** | Visual and logical collision mismatch. |   High   |    High    | Preserve a discrete simulation while delaying visual cell ownership through interpolation thresholds.                       |
| **R-05** | Renderer architecture refactoring.                 |  Medium  |   Medium   | Maintain clear layer boundaries and reserve dedicated time for renderer abstraction before release.                         |
| **R-06** | Code quality regressions during refactoring.                           |  Medium  |   Medium   | Develop unit and integration tests alongside refactoring and continuously run `mypy` and `flake8`.                          |
| **R-07** | Packaging or deployment issues on the evaluation environment.          |  Medium  |     Low    | Reserve the final stage for packaging, documentation and validation on a clean environment.                                 |


### Risk Management Strategy

The project followed a preventive risk management approach, prioritising the implementation of high-risk architectural components before less critical features. The game engine, collision system and external library integration were developed first, allowing fundamental design issues to be identified and resolved early in the project.

Rendering, UI improvements and packaging were intentionally postponed until the core gameplay mechanics had reached a stable state. This incremental strategy reduced the cost of architectural changes and avoided unnecessary rework.

Regular communication between developers, together with a strict separation between the simulation and rendering layers, minimised integration risks. In parallel, continuous testing and static analysis (`mypy` and `flake8`) provided immediate feedback during development, making large refactoring tasks considerably safer.

<!-- | Risk ID | Risk Description | Severity | Likelihood | Impact | Mitigation Strategy |
| :---: | :--- | :---: | :---: | :--- | :--- |
| **R-01** | **Faulty External Package Integration**<br>`A-Maze-ing` package fails, crashes, or returns unexpected grid formats. | High | Medium | Breaks level generation and crashes the game during evaluation. | Implement a defensive wrapper (`MazeAdapter`) with strict error handling, fallback defaults, and validation of the generated maze structure. |
| **R-02** | **Unhandled Exceptions / Unexpected Crashes**<br>Invalid config, missing files, or runtime bugs trigger a Python traceback. | Critical | Medium | Automatic project failure according to evaluation guidelines. | Enforce top-level `try-except` blocks, strict type checking with `mypy`, and comprehensive input validation across all file loaders. |
| **R-03** | **Ghost AI Complexity & Scope Creep**<br>Designing complex ghost algorithms takes more time than allocated in the schedule. | Medium | High | Delays UI rendering, testing, and packaging phases. | Implement basic BFS/distance-based movement first as an MVP, then refactor into modular behaviors (`ghost_ai.py`) if time permits. |
| **R-04** | **Cross-Platform & Packaging Failures**<br>The packaged build (Steam/Itch.io) fails to execute on a clean peer environment. | High | Low | Prevents demonstration of the deployed game during review. | Use isolated environments (`venv`/`uv`), create a simple reproducible packaging script, and test the build on a clean machine before submission. |
| **R-05** | **Config File Corruption / Missing Keys**<br>User or evaluator provides an invalid `config.json` file. | Medium | Medium | Game crashes on startup or behaves unpredictably. | Implement a fallback mechanism in `ConfigLoader` that clamps missing or invalid values to safe default settings without crashing. |
| **R-06** | **Code Quality & Linting Overhead**<br>Refactoring late in the project to pass strict `flake8` and `mypy` checks creates merge conflicts. | Medium | High | Last-minute bugs introduced right before code freeze. | Integrate `flake8` and `mypy` rules into the daily workflow and Makefile from Day 1 to catch type and style errors early. |
 -->
