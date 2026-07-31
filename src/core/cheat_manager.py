from dataclasses import dataclass

@dataclass
class CheatManager:
    invincible: bool = False
    freeze_ghosts: bool = False
    player_speed_multiplier: float = 1.0

    toggle_invincibility()

    toggle_freeze()

    skip_level(level)

    add_life(score_registry)

    increase_speed()

    reset()