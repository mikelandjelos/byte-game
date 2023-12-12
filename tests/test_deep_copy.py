import copy

from byte_game.model import Board
from byte_game.playing import Move, MoveDirection
from byte_game.utils import get_neighbor_in_direction


def test_deep_copy_board():
    board = Board(8)
    move = Move(("B", 8), 0, MoveDirection.DL)

    deep_copy_board = copy.deepcopy(board)

    # Get destination stack.
    destination_field_position = get_neighbor_in_direction(
        move.field_position, deep_copy_board.size, move.move_direction
    )

    if destination_field_position is None:
        raise ValueError(
            f"Can't retreive neighbor of {move.field_position}"
            f" in direction {move.move_direction}, on {deep_copy_board.size}x{deep_copy_board.size} board!"
        )

    destination_field = deep_copy_board[destination_field_position]

    # Get source stack and remove figures from it.
    source_field = deep_copy_board[move.field_position]

    stack_in_hand = source_field.remove_from(move.figure_position)

    # Put removed figures on destination stack.
    destination_field.put_on(stack_in_hand)

    assert board is not deep_copy_board
    assert board.matrix != deep_copy_board.matrix
