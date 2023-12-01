from byte_game.model import Board, Color, Figure


def test_board_init():
    board = Board(8)

    assert board["B", 2].color == Color.BLACK
    assert board["A", 3].stack == []
    assert board["F", 6].stack == [Figure.X]
    assert board["G", 5].stack == [Figure.O]
