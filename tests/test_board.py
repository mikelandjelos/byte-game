from byte_game.model import Board, Color, Figure
from byte_game.user_interface import UserInteface
from byte_game.utils import get_neighbors_leading_to_closest_nonempty_field


def test_board_init():
    board = Board(8)

    assert board["B", 2].color == Color.BLACK
    assert board["A", 3].stack == []
    assert board["F", 6].stack == [Figure.X]
    assert board["G", 5].stack == [Figure.O]
