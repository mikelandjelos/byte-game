from enum import Enum


class Figure(Enum):
    X = "X"
    O = "O"

    def __repr__(self) -> str:
        return self.value

    def __str__(self) -> str:
        return self.value


__all__ = ["Figure"]
