from dataclasses import dataclass
from enum import Enum

from ..model import FieldPosition


class MoveDirection(Enum):
    UL = "UL"  # Up-Left
    UR = "UR"  # Up-Right
    DL = "DL"  # Down-Left
    DR = "DR"  # Down-Right


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
