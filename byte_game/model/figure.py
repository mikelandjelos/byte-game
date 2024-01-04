from enum import Enum

from typing_extensions import Literal


class Figure(Enum):
    X = "X"
    O = "O"

    def __repr__(self) -> str:
        return self.value

    def __str__(self) -> str:
        return self.value

    @property
    def inverse(self) -> "Figure":
        return Figure.X if self == Figure.O else Figure.O


__all__ = ["Figure"]
