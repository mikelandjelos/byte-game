from dataclasses import dataclass
from .model import Board
from .playing import Move, MoveDirection
import copy

@dataclass
class ChangeOperator:
    """
    Represents state change operator.
    """
    def get_new_state(self, move: Move, board: Board) -> Board:
        deep_copy_board = copy.deepcopy(board)
        source_field = deep_copy_board[move.field_position]

        destination_row = ord(move.field_row)

        if (
            move.move_direction == MoveDirection.DL
            or move.move_direction == MoveDirection.DR
        ):
            destination_row += 1
        else:
            destination_row -= 1

        destination_column = move.field_column

        if (
            move.move_direction == MoveDirection.DR
            or move.move_direction == MoveDirection.UR
        ):
            destination_column += 1
        else:
            destination_column -= 1

        destination_field_position = (chr(destination_row), destination_column)
        destination_field = deep_copy_board[destination_field_position]

        stack_in_hand = source_field.remove_from(move.figure_position)

        destination_field.put_on(stack_in_hand)
 
        return deep_copy_board
