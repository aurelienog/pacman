Semana 1 (Arch & Adapters - ~40h en total): Análisis del subject, setup de Git/Makefile, ConfigLoader y MazeAdapter (A-Maze-ing).

Semana 2 (Core Logic & AI - ~40h en total): Entidades (Player, Ghost), colisiones, algoritmos de IA de los fantasmas (Chase, Frightened, Respawn) y Cheat Mode.

Semana 3 (UI & Rendering - ~35h en total): Bucle gráfico, RenderEngine, menús, HUD, gestión del estado e integración del sistema de Highscores.

Semana 4 (QA, Packaging & Docs - ~35h en total): Pruebas unitarias, linteo estricto (flake8, mypy), script de empaquetado (Steam/Itch.io) y documentación final.


## Gantt Chart

```mermaid
gantt
    title Pac-Man Project Planning (150h / 2 Developers / 4 Weeks)
    dateFormat  YYYY-MM-DD
    axisFormat  %W / %d-%b

    section 1. Setup & Architecture
    Specs, Git/Makefile & Docs setup                :des1, 2026-08-01, 6d
    Architecture design (MVC)                       :des2, 2026-08-03, 7d

    section 2. Core & Adapters
    Configuration Parser (JSON + comments)          :core1, 2026-08-06, 6d
    A-Maze-ing Adapter integration                  :core2, 2026-08-08, 7d
    Highscore Manager & JSON persistence            :core3, 2026-08-11, 6d

    section 3. Game Logic & Domain
    Maze engine & entities (Player, Items)          :dom1, 2026-08-12, 8d
    Ghost AI (Chase, Scared, Respawn)               :dom2, 2026-08-15, 9d
    Cheat Mode & game mechanics                     :dom3, 2026-08-18, 6d

    section 4. UI & Rendering
    Graphics Loop (Engine & Renderer)               :ui1, 2026-08-16, 9d
    Screens (Menu, HUD, Pause, GameOver)            :ui2, 2026-08-20, 8d

    section 5. Quality & Delivery
    Testing (pytest), Mypy & Flake8                 :qa1, 2026-08-23, 7d
    Packaging Build (Itch.io / Steam)               :qa2, 2026-08-25, 6d
    Documentation & final README.md                 :qa3, 2026-08-26, 6d
```

## Weekly Progress vs. Planned Baseline

| Week | Planned Goals | Actual Delivered | Status / Variances |
| :--- | :--- | :--- | :--- |
| **Week 1** | Config & MazeAdapter | Config & MazeAdapter complete | On track |
| **Week 2** | Domain Logic & Ghost AI | Ghost AI took +5 hours due to edge cases | +1 day variance (Mitigated in W3) |
| **Week 3** | UI Screens & Highscore | Menus & Highscore integrated | On track |
| **Week 4** | QA, Packaging & Docs | Packaging script & strict linting done | Finalized |