# Project Timeline

The project was initially planned over four weeks, with an estimated workload of approximately **150 hours** distributed across two developers. Thanks to an early focus on the engine architecture and the parallel development of the rendering system and asset pipeline, implementation progressed faster than originally expected. As a result, the second week is dedicated primarily to renderer refactoring, UI abstraction, asset polishing, and testing, while the final week focuses on release preparation, packaging and documentation.

## Planned Schedule

### Week 1 (~60h)

Main milestones:

- Project setup (Git, Makefile, coding standards)
- Layered Architecture design & interface contract definition (`Snapshot`, `InputAction`)
- Configuration loader and JSON parser
- A-Maze-ing adapter integration
- Highscore persistence
- Domain model (Maze, Position, Player, Ghost, Items)
- Game session and game loop
- Level loading
- Ghost AI (BFS pathfinding and personalities)
- Collision system
- Entity interpolation and renderer snapshots
- Parallel development of the Pygame renderer, assets and game loop
- Improve Pygame renderer abstraction and isolate asset loaders
- Refactor rendering primitives for strict MLX compatibility (pure math bounds checking, standard text rendering, sprite blitting)
- Design and implement custom sprite atlases (Pac-Man 4x3 direction/mouth animation, 4 individual Ghost 4x2 atlases, and Utils item atlas)
- HUD redesign with dynamic resolution scaling and section separators
- Interactive menu and pause overlay mouse support (`MOUSEMOTION` & `MOUSEBUTTONDOWN`)
- Dynamic sci-fi background frame scaling and UI panel integration


### Week 2 (~60h)

With the core functionality already implemented, the second week focuses on improving the internal architecture of the rendering layer, increasing the level of abstraction in the UI, and ensuring strict compliance with graphical library constraints (MLX equivalence rules). In parallel, unit and integration tests are developed, while gameplay polishing, asset refinement, bug fixing, and static analysis (mypy and flake8) are carried out to prepare the project for release.

Main milestones:

- Improve Pygame renderer abstraction
- Decouple rendering from engine
- Improve UI architecture
- HUD polishing
- Menu improvements
- Animation polishing
- Asset integration
- Unit tests
- Integration tests
- Gameplay balancing and collision threshold tuning
- Bug fixing
- Static analysis (mypy & flake8)

### Week 3 (~30h)

Final stabilization and release preparation including packaging, documentation and delivery.

Main milestones:

- Packaging
- Documentation
- Final release build

## Gantt Chart

```mermaid
gantt
    title Pac-Man Project Timeline
    dateFormat YYYY-MM-DD
    axisFormat %d-%b

    section Core Engine
    Project setup & architecture                 :a1, 2026-08-01, 1d
    Configuration & adapters                     :a2, 2026-08-01, 2d
    Domain model                                 :a3, 2026-08-02, 2d
    Game session & update loop                   :a4, 2026-08-03, 3d
    Ghost AI & pathfinding                       :a5, 2026-08-04, 2d
    Collision system                             :a6, 2026-08-05, 2d
    Entity interpolation & snapshots             :a7, 2026-08-06, 1d

    section UI & Rendering
    Assets production                            :b1, 2026-08-03, 4d
    Pygame renderer                              :b2, 2026-08-03, 4d
    HUD, menus & game screens                    :b3, 2026-08-04, 3d

    section Refactoring & Testing
    Renderer architecture                        :c1, 2026-08-08, 3d
    UI abstraction                               :c2, 2026-08-09, 3d
    Rendering integration & polish               :c3, 2026-08-11, 2d
    Unit & integration testing                   :c4, 2026-08-08, 5d
    Gameplay bug fixing                          :c5, 2026-08-10, 3d
    Static analysis (mypy, flake8)               :c6, 2026-08-11, 2d

    section Quality & Delivery
    Packaging                                    :d1, 2026-08-15, 2d
    Documentation                                :d2, 2026-08-15, 2d
    Final polishing & release                    :d3, 2026-08-15, 4d
```

## Weekly Progress vs. Planned Baseline

| Week       | Planned Goals                                    | Actual Delivered                                                                                                                                                                | Status / Variances                                                                                                                          |
| :--------- | :----------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------ |
| **Week 1** | Core engine implementation and initial rendering | Core engine completed (configuration, adapters, domain model, game session, AI, collisions, interpolation) together with a functional Pygame renderer, custom asset pipeline foundation, and initial UI layouts, implemented interactive mouse navigation, dynamic HUD scaling  | **Completed ahead of schedule.** Parallel development allowed the rendering layer to mature alongside the core engine, bringing forward a substantial portion of the work originally planned for Week 2. |
| **Week 2** | Renderer refactoring and testing                 | Improve renderer architecture and UI abstraction while expanding unit and integration tests, fixing gameplay issues and performing static analysis. Refactored renderer architecture into isolated asset modules, ensured strict MLX compatibility                              | **Completed ahead of schedule.** Focus shifts from feature development to code quality and maintainability. *Focus shifted from core gameplay to visual presentation polish, MLX compliance, code quality, and maintainability.*                                                |
| **Week 3** | Packaging and delivery                           | Final documentation, project management evidence compilation, packaging, release preparation and final polish                                                                                                            | **Completed ahead of schedule.** Reserved primarily for stabilization and project delivery rather than feature implementation.                              |
