## Team Organization & Task Distribution

### Role Matrix / RACI:

| Developer       | Main Responsibilities                                                                                      |
| --------------- | ---------------------------------------------------------------------------------------------------------- |
| **aunoguei** |  Configuration loader, persistence layer, simulation architecture, domain models, game logic and gameplay mechanics, ghost AI, pathfinding, collision system, testing, documentation.|
| **oshtohri**    | A-Maze-ing adapter, domain models, Pygame renderer architecture, asset production & sprite atlases, UI layout design (HUD, Menus, Instructions card, Pause overlay), MLX compliance refactoring, packaging, documentation. |

### Collaboration Strategy

Development was organised around architectural layers rather than gameplay features, allowing both developers to work in parallel with minimal merge conflicts.

Interfaces between the game engine and the rendering layer (such as `Snapshot` and `InputAction`) were defined before implementation, reducing coupling and enabling independent development. While **aunoguei** built the deterministic game rules and gameplay mechanics, **oshtohri** established the presentation layer, creating custom sprite atlases, responsive HUD components, mouse interaction handlers, and background layouts.

Architectural decisions were discussed through regular peer reviews until consensus was reached, while continuous integration with Git ensured frequent synchronization and early detection of integration issues.

## Risk Analysis & Mitigation Matrix

|  Risk ID | Risk Description                                                       | Severity | Likelihood | Mitigation Strategy                                                                                                         |
| :------: | ---------------------------------------------------------------------- | :------: | :--------: | --------------------------------------------------------------------------------------------------------------------------- |
| **R-01** | External package incompatibility (`A-Maze-ing`).                       |   High   |   Medium   | Isolate the dependency behind `MazeAdapter`, validating and converting external data into the internal representation.      |
| **R-02** | Config File Corruption / Missing Keys | Medium | Medium | Implement a fallback mechanism in `ConfigLoader` that clamps missing or invalid values to safe default settings without crashing. |
| **R-03** | Highscore persistence failure or corrupted data. | Medium | Medium | Isolate persistence behind a dedicated persistence layer, validate the stored JSON structure when loading, and safely handle missing, invalid or unreadable highscore files. |
| **R-04** | Rendering becoming coupled with gameplay logic.                        |   High   |    High    | Keep rendering completely independent through immutable `snapshots` while the engine operates only on logical grid positions. |
| **R-05** | Ghost AI complexity.                |  Medium  |    High    | Replace the initial Manhattan-distance heuristic with `BFS pathfinding` and `independent targeting strategies` for each ghost.  |
| **R-06** | Visual and logical collision mismatch. |   High   |    High    | Preserve a discrete simulation while delaying visual cell ownership through `interpolation thresholds`.                       |
| **R-07** | Renderer architecture refactoring.                 |  Medium  |   Medium   | Maintain clear layer boundaries and reserve dedicated time for renderer abstraction before release.                         |
| **R-08** | Code quality regressions during refactoring.                           |  Medium  |   Medium   | Develop unit and integration tests alongside refactoring and continuously run `mypy` and `flake8`.                          |
| **R-09** | Graphical Library Non-Compliance (MLX Equivalence Rule).             |   High   |    High    | Refactor UI and renderer to eliminate Pygame convenience functions (`Rect.collidepoint`, multi-layer alpha surfaces), relying only on MLX-equivalent primitives. |
| **R-10** | Asset Slicing & Resolution Distortion on window resize.               |  Medium  |   Medium   | Implement modular sprite atlas loaders (`pacman_neon_assets`, `ghosts_neon_assets`) and dynamic scale factors for HUD, fonts, and panel layouts.               |
| **R-11** | Packaging or deployment issues on the evaluation environment.         |  Medium  |    Low     | Reserve the final stage for packaging, documentation, and validation on a clean environment.                                                                     |


### Risk Management Strategy

The project followed a preventive risk management approach, prioritising the implementation of high-risk architectural components before less critical features. The game engine, collision system and external library integration were developed first, allowing fundamental design issues to be identified and resolved early in the project.

Rendering, UI improvements, asset creation, and packaging were intentionally structured into independent modules that consumed engine snapshots. This incremental strategy reduced the cost of architectural changes and avoided unnecessary rework.

Regular communication between developers, together with a strict separation between the simulation and rendering layers, minimised integration risks. In parallel, continuous testing and static analysis (`mypy` and `flake8`) provided immediate feedback during development, making large refactoring tasks considerably safer.

When the strict MLX graphical compliance rule was introduced, the isolated UI architecture allowed **oshtohri** to refactor input detection (pure math bounds checking) and asset rendering without disrupting **aunoguei**'s core simulation logic.

<!-- | Risk ID | Risk Description | Severity | Likelihood | Impact | Mitigation Strategy |

| **R-04** | **Cross-Platform & Packaging Failures**<br>The packaged build (Steam/Itch.io) fails to execute on a clean peer environment. | High | Low | Prevents demonstration of the deployed game during review. | Use isolated environments (`venv`/`uv`), create a simple reproducible packaging script, and test the build on a clean machine before submission. |
