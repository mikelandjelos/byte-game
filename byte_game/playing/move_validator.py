from ..model import Board
from .move import Move, MoveDirection
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
        #if 1,1
        #if 1,n
        #if n, 1
        #if n,n
        #if 1, sredina
        #if sredina, 1
        #if n, sredina
        #if sredina, n
        row = ord(self.move.field_position[0])
        fieldDR = self.board[(chr(row+1),self.move.field_position[1]+1)]
        fieldDL=self.board[(chr(row+1),self.move.field_position[1]-1)]
        fieldUR=self.board[(chr(row-1),self.move.field_position[1]+1)]
        fieldUL=self.board[(chr(row-1),self.move.field_position[1]-1)]
        return (fieldDR.stack_height == 0 and 
                fieldDL.stack_height == 0 and 
                fieldUL.stack_height ==0 and 
                fieldUR.stack_height==0)
        
    @property
    def valid_chosen_figure(self):
        currentField = self.board[self.move.field_position]
        # returns True if position is 0 and figure on position 0 belongs to current player 
        return self.move.figure_position == 0 and currentField.stack[self.move.figure_position] == self.player.figure

    @property
    def is_shortest_path_to_stack(self):
        raise NotImplementedError
    
    @property
    def get_neighbor_stack_height(self):
        row  = ord(self.move.field_position[0])
        if self.move.move_direction == MoveDirection.DR:
            fieldPosition = self.board[(chr(row+1),self.move.field_position[1]+1)]
            return fieldPosition.stack_height
        elif self.move.move_direction == MoveDirection.DL:
            fieldPosition = self.board[(chr(row+1),self.move.field_position[1]-1)]
            return fieldPosition.stack_height
        elif self.move.move_direction == MoveDirection.UR:
            fieldPosition = self.board[(chr(row-1),self.move.field_position[1]+1)]
            return fieldPosition.stack_height
        else:
            fieldPosition = self.board[(chr(row-1),self.move.field_position[1]-1)]
            return fieldPosition.stack_height
        
    @property
    def merge_checked(self):
        currentField = self.board[self.move.field_position]

        if currentField.stack[self.move.figure_position] != self.player.figure:
            return False

        currentStack = currentField.stack[self.move.figure_position:]
        total = self.get_neighbor_stack_height + len(currentStack)

        if total > 8 or self.get_neighbor_stack_height <= self.move.figure_position:
            return False

        return True


   

    
