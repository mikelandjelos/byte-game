from typing import Tuple

from ..model import Board, FieldPosition
from ..utils import (
    get_neighbor_in_direction,
    get_neighbors,
    get_neighbors_leading_to_closest_nonempty_field,
)
from .move import Move, MoveDirection
from .player import Player


class MoveValidator:
    def __init__(self, move: Move, board: Board, player: Player) -> None:
        self.move = move
        self.board = board
        self.player = player

    # region Basic validations

    @property
    def row_in_boundaries(self) -> bool:
        row = ord(self.move.field_row) - ord("A") + 1
        return row <= 0 or row > self.board.size

    @property
    def column_in_boundaries(self) -> bool:
        column = self.move.field_column
        return column <= 0 or column > self.board.size

    @property
    def is_field_empty(self) -> bool:
        return self.board[self.move.field_position].stack_height == 0

    @property
    def is_stack_high_enough(self) -> bool:
        return (
            self.board[self.move.field_position].stack_height - 1
            < self.move.figure_position
        )

    # endregion !Basic validations

    # OVAJ KOMENTAR TREBA DA BUDE SKLONJEN NAKON IZRADE
    # Property-ji/funkcije ispod preimenuj, obrisi, pravi nove, kako god
    # ovo je samo pokazno

    @property
    def neighbor_fields_empty(self) -> bool:
        return all(
            self.board[position].stack_height == 0
            for position in get_neighbors(self.move.field_position).values()
        )

    @property
    def valid_chosen_figure(self):
        currentField = self.board[self.move.field_position]
        # returns True if position is 0 and figure on position 0 belongs to current player
        return (
            self.move.figure_position == 0
            and currentField.stack[self.move.figure_position] == self.player.figure
        )

    @property
    def shortest_path_constraint(self) -> Tuple[bool, list[FieldPosition]]:
        allowed_positions = get_neighbors_leading_to_closest_nonempty_field(
            self.board, self.move.field_position
        )

        return (
            (
                get_neighbor_in_direction(
                    self.move.field_position,
                    self.board.size,
                    self.move.move_direction,
                )
                in allowed_positions
            ),
            allowed_positions,
        )

    @property
    def get_neighbor_stack_height(self):
        row = ord(self.move.field_position[0])
        if self.move.move_direction == MoveDirection.DR:
            fieldPosition = self.board[(chr(row + 1), self.move.field_position[1] + 1)]
            return fieldPosition.stack_height
        elif self.move.move_direction == MoveDirection.DL:
            fieldPosition = self.board[(chr(row + 1), self.move.field_position[1] - 1)]
            return fieldPosition.stack_height
        elif self.move.move_direction == MoveDirection.UR:
            fieldPosition = self.board[(chr(row - 1), self.move.field_position[1] + 1)]
            return fieldPosition.stack_height
        else:
            fieldPosition = self.board[(chr(row - 1), self.move.field_position[1] - 1)]
            return fieldPosition.stack_height

    @property
    def boundaries_check(self):
        lastRowletter = chr(ord("A") + self.board.size - 1)
        if (
            self.move.field_column == 1
            and self.move.field_row == "A"
            and self.move.move_direction != MoveDirection.DR
        ):  # gornja leva
            return False
        # prva vrsta sredina
        elif (
            self.move.field_row == "A"
            and self.move.field_column != self.board.size
            and (
                self.move.move_direction != MoveDirection.DL
                and self.move.move_direction != MoveDirection.DR
            )
        ):
            return False
        # prva vrsta gore desno OVO JE BELO POLJE NE MORA DA SE PROVERAVA ALI NMVZ
        elif (
            self.move.field_row == "A"
            and self.move.field_column == self.board.size
            and self.move.move_direction != MoveDirection.DL
        ):
            return False
        elif (
            self.move.field_column == 1
            and self.move.field_row != "A"
            and self.move.field_row != lastRowletter
            and self.move.move_direction != MoveDirection.UR
            and self.move.move_direction != MoveDirection.DR
        ):
            return False
        # ovo je belo isto
        elif (
            self.move.field_row == lastRowletter
            and self.move.field_column == 1
            and self.move.move_direction != MoveDirection.UR
        ):
            return False
        elif (
            self.move.field_row == lastRowletter
            and self.move.field_column != self.board.size
            and self.move.move_direction != MoveDirection.UL
            and self.move.move_direction != MoveDirection.UR
        ):
            return False
        elif (
            self.move.field_row == lastRowletter
            and self.move.field_column == self.board.size
            and self.move.move_direction != MoveDirection.UL
        ):
            return False
        elif (
            self.move.field_column == self.board.size
            and self.move.move_direction != MoveDirection.DL
            and self.move.move_direction != MoveDirection.UL
        ):
            return False
        return True

    @property
    def merge_checked(self):
        currentField = self.board[self.move.field_position]

        if currentField.stack[self.move.figure_position] != self.player.figure:
            return False

        currentStack = currentField.stack[self.move.figure_position :]
        total = self.get_neighbor_stack_height + len(currentStack)

        if total > 8 or self.get_neighbor_stack_height <= self.move.figure_position:
            return False

        return True
