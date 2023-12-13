import copy
from dataclasses import dataclass

from .model import Board, FieldPosition, Figure
from .playing import Move, MoveDirection
from .utils import get_neighbor_in_direction


@dataclass
class StateChangeOperator:
    """
    Represents state change operator.
    """

    board: Board
    playing_figure: Figure

    def __generate_moves(
        self,
        field_position: FieldPosition,
        figure_position: int,
        list_of_moves: list[Move],
    ):
        from .game import is_move_valid

        move = Move(field_position, figure_position, MoveDirection.DL)
        if is_move_valid(move, self.board, self.playing_figure):
            list_of_moves.append(move)

        move = Move(field_position, figure_position, MoveDirection.DR)
        if is_move_valid(move, self.board, self.playing_figure):
            list_of_moves.append(move)

        move = Move(field_position, figure_position, MoveDirection.UL)
        if is_move_valid(move, self.board, self.playing_figure):
            list_of_moves.append(move)

        move = Move(field_position, figure_position, MoveDirection.UR)
        if is_move_valid(move, self.board, self.playing_figure):
            list_of_moves.append(move)

    def __process_field(
        self,
        field_position: FieldPosition,
        stack: list[Figure],
        list_of_moves: list[Move],
    ):
        for i, figure in enumerate(stack):
            if figure == self.playing_figure:
                self.__generate_moves(field_position, i, list_of_moves)

    def __get_all_possible_moves(self) -> list[Move]:
        list_of_moves = []
        for i, row in enumerate(self.board.matrix):
            # even rows
            if i % 2 == 0:
                for j in range(0, self.board.size, 2):
                    field = row[j]
                    if field.stack_height > 0:
                        self.__process_field(field.position, field.stack, list_of_moves)
            # odd rows
            else:
                for j in range(1, self.board.size, 2):
                    field = row[j]
                    if field.stack_height > 0:
                        self.__process_field(field.position, field.stack, list_of_moves)
        return list_of_moves

    def __get_new_state(self, move: Move) -> Board:
        deep_copy_board = copy.deepcopy(self.board)

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

        return deep_copy_board

    def ai_get_all_possible_states(self) -> list[Board]:
        all_possible_states = []

        for move in self.__get_all_possible_moves():
            all_possible_states.append(self.__get_new_state(move))

        return all_possible_states

    def pvp_get_all_possible_moves(self) -> list[Move]:
        return self.__get_all_possible_moves()
