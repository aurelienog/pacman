## Team Organization & Task Distribution

Role Matrix / RACI:

Dev 1: Core Logic, Ghost AI, Cheat Mode, Highscore Manager.

Dev 2: ConfigLoader, MazeAdapter, RenderEngine (UI/HUD), Packaging Script.

Decision Making Process: Acuerdos mediante Peer Code Reviews periódicos y consenso en la definición de la arquitectura MVC.

## Risk Analysis & Mitigation Matrix

| Risk ID | Risk Description | Severity | Likelihood | Impact | Mitigation Strategy |
| :---: | :--- | :---: | :---: | :--- | :--- |
| **R-01** | **Faulty External Package Integration**<br>`A-Maze-ing` package fails, crashes, or returns unexpected grid formats. | High | Medium | Breaks level generation and crashes the game during evaluation. | Implement a defensive wrapper (`MazeAdapter`) with strict error handling, fallback defaults, and validation of the generated maze structure. |
| **R-02** | **Unhandled Exceptions / Unexpected Crashes**<br>Invalid config, missing files, or runtime bugs trigger a Python traceback. | Critical | Medium | Automatic project failure according to evaluation guidelines. | Enforce top-level `try-except` blocks, strict type checking with `mypy`, and comprehensive input validation across all file loaders. |
| **R-03** | **Ghost AI Complexity & Scope Creep**<br>Designing complex ghost algorithms takes more time than allocated in the schedule. | Medium | High | Delays UI rendering, testing, and packaging phases. | Implement basic BFS/distance-based movement first as an MVP, then refactor into modular behaviors (`ghost_ai.py`) if time permits. |
| **R-04** | **Cross-Platform & Packaging Failures**<br>The packaged build (Steam/Itch.io) fails to execute on a clean peer environment. | High | Low | Prevents demonstration of the deployed game during review. | Use isolated environments (`venv`/`uv`), create a simple reproducible packaging script, and test the build on a clean machine before submission. |
| **R-05** | **Config File Corruption / Missing Keys**<br>User or evaluator provides an invalid `config.json` file. | Medium | Medium | Game crashes on startup or behaves unpredictably. | Implement a fallback mechanism in `ConfigLoader` that clamps missing or invalid values to safe default settings without crashing. |
| **R-06** | **Code Quality & Linting Overhead**<br>Refactoring late in the project to pass strict `flake8` and `mypy` checks creates merge conflicts. | Medium | High | Last-minute bugs introduced right before code freeze. | Integrate `flake8` and `mypy` rules into the daily workflow and Makefile from Day 1 to catch type and style errors early. |