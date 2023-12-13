from dataclasses import dataclass
from enum import Enum

from ..model import FieldPosition


class MoveDirection(Enum):
    UL = "UL"  # Up-Left
    UR = "UR"  # Up-Right
    DL = "DL"  # Down-Left
    DR = "DR"  # Down-Right

    def __repr__(self) -> str:
        return self.value

    def __str__(self) -> str:
        return self.__repr__()


@dataclass
class Move:
    field_position: FieldPosition
    figure_position: int  # figure position, in stack
    move_direction: MoveDirection

    @property
    def field_row(self):
        return self.field_position[0]

    @property
    def field_column(self):
        return self.field_position[1]

    def __repr__(self) -> str:
        return f"{self.field_row}{self.field_column} {self.figure_position} {self.move_direction}"

    def __str__(self) -> str:
        return self.__repr__()
