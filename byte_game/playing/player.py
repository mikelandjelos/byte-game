from dataclasses import dataclass, field

from ..model import MAX_STACK_SIZE, Board, Figure
from ..utils import get_neighbor_in_direction
from .move import Move


@dataclass
class Player:
    figure: Figure
    collected_stacks: list[list] = field(init=False, default_factory=list)

    @property
    def score(self) -> int:
        return len(self.collected_stacks)

    def make_move(self, move: Move, board: Board) -> None:
        # Get destination stack.
        destination_field_position = get_neighbor_in_direction(
            move.field_position, board.size, move.move_direction
        )

        if destination_field_position is None:
            raise ValueError(
                f"Can't retreive neighbor of {move.field_position}"
                f" in direction {move.move_direction}, on {board.size}x{board.size} board!"
            )

        destination_field = board[destination_field_position]

        # Get source stack and remove figures from it.
        source_field = board[move.field_position]

        stack_in_hand = source_field.remove_from(move.figure_position)

        # Put removed figures on destination stack.
        destination_field.put_on(stack_in_hand)

        # If stack height reached 8, update player score!
        if destination_field.stack_height == MAX_STACK_SIZE:
            self.collected_stacks.append(stack_in_hand)
            destination_field.stack = []
