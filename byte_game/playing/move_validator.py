from ..model import Board
from .move import Move


class MoveValidator:
    def __init__(self, move: Move, board: Board) -> None:
        self.move = move
        self.board = board

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
    def neighbor_fields_empty(self):
        row = ord(self.move.field_position[0])
        fieldPositionDR = self.board.__getitem__((chr(row+1),self.move.field_position[1]+1))
        fieldPositionDL=self.board.__getitem__((chr(row+1),self.move.field_position[1]-1))
        fieldPositionUR=self.board.__getitem__((chr(row-1),self.move.field_position[1]+1))
        fieldPositionUL=self.board.__getitem__((chr(row-1),self.move.field_position[1]-1))
        
        
        if len(fieldPositionDR.stack)==0 or len(fieldPositionDL.stack) == 0 or len (fieldPositionUL.stack)==0 or len(fieldPositionUR.stack)==0:
            print("True")
        else:
            print("False")
        return True

    @property
    def is_shortest_path_to_stack(self):
        raise NotImplementedError
    
    @property
    def is_move_valid(self):
         fieldPosition = self.board.__getitem__(self.move.field_position)
         print(fieldPosition.stack[self.move.figure_position])

   

    
