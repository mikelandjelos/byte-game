from byte_game.model.board import Board
from byte_game.user_interface import UserInteface
from byte_game.utils import (
    get_neighbors,
    get_neighbors_leading_to_closest_nonempty_field,
)


def test_get_neighbors():
    neighbors_A1 = get_neighbors(("A", 1), 8)
    assert neighbors_A1 == [("B", 2)]

    neighbors_H8 = get_neighbors(("H", 8), 8)
    assert neighbors_H8 == [("G", 7)]

    neighbors_D4 = get_neighbors(("D", 4), 8)
    assert neighbors_D4 == [("C", 3), ("C", 5), ("E", 3), ("E", 5)]

    neighbors_E1 = get_neighbors(("E", 1), 8)
    assert neighbors_E1 == [("D", 2), ("F", 2)]


def test_get_neighbors_leading_to_closest_nonempty_field():
    board = Board(8)
    ui = UserInteface()

    for row in board.matrix:
        for field in row:
            if (
                field.position == ("B", 2)
                or field.position == ("G", 1)
                or field.position == ("C", 7)
            ):
                continue

            if field.stack_height >= 1:
                field.remove_from(0)

    allowed_positions = get_neighbors_leading_to_closest_nonempty_field(
        board, board[("B", 2)]
    )
    assert sorted([("C", 1), ("C", 3), ("A", 3)]) == sorted(allowed_positions)
