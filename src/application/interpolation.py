from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .game_session import GameSession


def player_progress(session: "GameSession") -> float:
    step = (
        session.BASE_PLAYER_STEP_SECONDS / 2
        if session.speed_boost
        else session.BASE_PLAYER_STEP_SECONDS
    )

    return min(
        1.0,
        max(
            0.0,
            session._player_elapsed / step,
        ),
    )


def ghost_progress(session: "GameSession") -> float:
    if session.freeze_ghosts:
        return 1.0

    return min(
        1.0,
        max(
            0.0,
            session._ghost_elapsed
            / session.GHOST_STEP_SECONDS,
        ),
    )
