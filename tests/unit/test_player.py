"""Unit tests for the Player domain model."""

from src.domain import Direction, Player, Position


def make_player(
    position: Position = Position(2, 2),
    spawn: Position = Position(1, 1),
    lives: int = 3,
    direction: Direction = Direction.NONE,
    requested_direction: Direction = Direction.NONE,
) -> Player:
    """Create a predictable Player for unit tests."""
    return Player(
        position=position,
        spawn=spawn,
        lives=lives,
        direction=direction,
        requested_direction=requested_direction,
        prev_position=position,
    )


def test_player_initializes_with_expected_values() -> None:
    """A player should preserve the values supplied at construction."""
    player = make_player()

    assert player.position == Position(2, 2)
    assert player.spawn == Position(1, 1)
    assert player.lives == 3
    assert player.direction is Direction.NONE
    assert player.requested_direction is Direction.NONE
    assert player.prev_position == Position(2, 2)


def test_player_can_change_position() -> None:
    """Player position should be mutable during the game."""
    player = make_player()

    player.position = Position(3, 2)

    assert player.position == Position(3, 2)


def test_player_can_change_direction() -> None:
    """Player direction should be mutable."""
    player = make_player()

    player.direction = Direction.RIGHT

    assert player.direction is Direction.RIGHT


def test_player_can_change_requested_direction() -> None:
    """Requested direction should be stored independently."""
    player = make_player()

    player.requested_direction = Direction.UP

    assert player.requested_direction is Direction.UP
    assert player.direction is Direction.NONE


def test_player_can_lose_a_life() -> None:
    """Player lives should be decrementable."""
    player = make_player(lives=3)

    player.lives -= 1

    assert player.lives == 2


def test_player_can_gain_a_life() -> None:
    """Player lives should be incrementable."""
    player = make_player(lives=2)

    player.lives += 1

    assert player.lives == 3


def test_player_spawn_position_is_preserved() -> None:
    """The spawn position should remain available for respawning."""
    spawn = Position(4, 4)
    player = make_player(
        position=Position(2, 2),
        spawn=spawn,
    )

    player.position = Position(0, 0)

    assert player.spawn == spawn
    assert player.position != player.spawn


def test_player_previous_position_can_track_movement() -> None:
    """Previous position should be independently updated by movement logic."""
    player = make_player(
        position=Position(2, 2),
    )

    player.prev_position = player.position
    player.position = Position(3, 2)

    assert player.prev_position == Position(2, 2)
    assert player.position == Position(3, 2)


def test_player_starts_with_three_lives_by_default() -> None:
    """The domain default should provide three lives."""
    player = Player(
        lives=3,
        position=Position(0, 0),
        spawn=Position(0, 0),
    )

    assert player.lives == 3


def test_player_starts_with_no_direction_by_default() -> None:
    """A newly created player should not move until a direction is selected."""
    player = Player(
        lives=3,
        position=Position(0, 0),
        spawn=Position(0, 0),
    )

    assert player.direction is Direction.NONE
    assert player.requested_direction is Direction.NONE


def test_player_is_not_frozen() -> None:
    """Player state is expected to be mutable during gameplay."""
    player = make_player()

    player.lives = 1
    player.position = Position(0, 0)

    assert player.lives == 1
    assert player.position == Position(0, 0)
