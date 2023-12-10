from ..model import Board
from .move import Move,MoveDirection
from .player import Player
 
class MoveValidator:
    def __init__(self, move: Move, board: Board,player:Player) -> None:
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
    def neighbor_fields_empty(self)-> bool:
        row = ord(self.move.field_position[0])
        fieldPositionDR = self.board.__getitem__((chr(row+1),self.move.field_position[1]+1))
        fieldPositionDL=self.board.__getitem__((chr(row+1),self.move.field_position[1]-1))
        fieldPositionUR=self.board.__getitem__((chr(row-1),self.move.field_position[1]+1))
        fieldPositionUL=self.board.__getitem__((chr(row-1),self.move.field_position[1]-1))
        if len(fieldPositionDR.stack)==0 and len(fieldPositionDL.stack) == 0 and len (fieldPositionUL.stack)==0 and len(fieldPositionUR.stack)==0:
            return True
        else:
            return False
        

    @property
    def is_shortest_path_to_stack(self):
        raise NotImplementedError
    @property
    def get_neighbor_stack(self):
        row  = ord(self.move.field_position[0])
        if self.move.move_direction==MoveDirection.DR:
            fieldPosition = self.board.__getitem__((chr(row+1),self.move.field_position[1]+1))
            return fieldPosition.stack
        elif self.move.move_direction==MoveDirection.DL:
            fieldPosition = self.board.__getitem__((chr(row+1),self.move.field_position[1]-1))
            return fieldPosition.stack
        elif self.move.move_direction==MoveDirection.UR:
            fieldPosition = self.board.__getitem__((chr(row-1),self.move.field_position[1]+1))
            return fieldPosition.stack
        else:
            fieldPosition = self.board.__getitem__((chr(row-1),self.move.field_position[1]-1))
            return fieldPosition.stack
        
    @property
    def merge_checked(self):
        fieldPosition = self.board[self.move.field_position]
        if fieldPosition.stack[self.move.figure_position] == self.player.figure:
            currentStack = fieldPosition.stack
            newStack = currentStack[self.move.figure_position:]
            neighborStack =self.get_neighbor_stack
            total = len(neighborStack)+len(newStack)
            print(total)
            if not total > 8:
              if len(neighborStack)>self.move.figure_position:
                 return True
              else:
                  return False
            else:
                return False

        else:
            return False
        



   

    
