from dataclasses import dataclass, field

from ..model import Board, Figure
from .move import Move


@dataclass
class Player:
    """
    Represents Byte game player.
    """

    figure: Figure
    score: int = field(init=False, default=0)  # number of collected stacks

    def make_move(self, move: Move, board: Board):  # faza 2
        raise NotImplementedError
