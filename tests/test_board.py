from byte_game.model import Board, Color, Figure
from byte_game.user_interface import UserInteface
from byte_game.utils import path_to_closest_nonempty_position


def test_board_init():
    board = Board(8)

    assert board["B", 2].color == Color.BLACK
    assert board["A", 3].stack == []
    assert board["F", 6].stack == [Figure.X]
    assert board["G", 5].stack == [Figure.O]


def test_path_to_closest_nonempty_position():
    board = Board(8)
    ui = UserInteface()

    board[("B", 4)], board[("B", 6)], board[("B", 8)] = [], [], []
    board[("C", 1)], board[("C", 3)], board[("C", 5)] = [], [], []
    board[("D", 2)], board[("D", 4)], board[("D", 6)], board[("D", 8)] = [], [], [], []
    board[("E", 1)], board[("E", 3)], board[("E", 5)], board[("E", 7)] = [], [], [], []
    board[("F", 2)], board[("F", 4)], board[("F", 6)], board[("F", 8)] = [], [], [], []
    board[("G", 3)], board[("G", 5)] = [], []

    ui.show_board(board)
    print(path_to_closest_nonempty_position(board, ("B", 2)))
    assert False
