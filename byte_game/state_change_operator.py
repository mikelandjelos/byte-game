from dataclasses import dataclass
from .model import Board
from .playing import Move, MoveDirection, Player
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
    

    def generate_moves(self, board: Board, player: Player, field_position, figure_position, list_of_moves):
        move = Move(field_position, figure_position, MoveDirection.DL)
        if self.is_move_valid(move, board, player):
            list_of_moves.append(Move(field_position, figure_position, move))

        move = Move(field_position, figure_position, MoveDirection.DR)
        if self.is_move_valid(move, board, player):
            list_of_moves.append(Move(field_position, figure_position, move))

        move = Move(field_position, figure_position, MoveDirection.UL)
        if self.is_move_valid(move, board, player):
            list_of_moves.append(Move(field_position, figure_position, move))

        move = Move(field_position, figure_position, MoveDirection.UR)
        if self.is_move_valid(move, board, player):
            list_of_moves.append(Move(field_position, figure_position, move))

    def process_field(self, board: Board, player: Player, field_position, stack, list_of_moves):
        for i, figure in enumerate(stack):
            if figure == player.figure:
                self.generate_moves(board, player, field_position, i, list_of_moves)

    def get_all_possible_moves(self, player: Player, board: Board):
        list_of_moves = []
        for i, row in enumerate(board.matrix):
            # even rows
            if i % 2 == 0:
                for j in range(0, board.size, 2):
                    field = row[j]
                    if field.stack_height > 0:
                        self.process_field(board, player, field.position, field.stack, list_of_moves)
            # odd rows
            else:
                for j in range(1, board.size, 2):
                    field = row[j]
                    if field.stack_height > 0:
                        self.process_field(board, player, field.position, field.stack, list_of_moves)
        return list_of_moves
