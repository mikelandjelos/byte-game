from dataclasses import dataclass, field

from ..model import MAX_STACK_SIZE, Board, Figure
from .move import Move, MoveDirection


@dataclass
class Player:
    figure: Figure
    collected_stacks: list[list] = field(init=False, default_factory=list)

    @property
    def score(self) -> int:
        return len(self.collected_stacks)

    def make_move(self, move: Move, board: Board) -> None:
        source_field = board[move.field_position]

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
        destination_field = board[destination_field_position]

        stack_in_hand = source_field.remove_from(move.figure_position)

        destination_field.put_on(stack_in_hand)

        if destination_field.stack_height == MAX_STACK_SIZE:
            self.collected_stacks.append(stack_in_hand)
            destination_field.stack = []
