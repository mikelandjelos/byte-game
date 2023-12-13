from dataclasses import dataclass, field
from enum import Enum
from typing import Tuple, TypeAlias

from .figure import Figure

MAX_STACK_HEIGHT = 8


class Color(Enum):
    BLACK = "BLACK"
    WHITE = "WHITE"


FieldPosition: TypeAlias = Tuple[str, int]


@dataclass
class Field:
    position: FieldPosition
    stack: list[Figure] = field(default_factory=list)

    def put_on(self, stack_to_add: list[Figure]) -> bool:
        # if given stack cannot be added to current stack
        if len(self.stack) + len(stack_to_add) > MAX_STACK_HEIGHT:
            return False

        # add given stack to current stack
        self.stack.extend(stack_to_add)

        # successful
        return True

    def remove_from(self, position: int) -> list[Figure]:
        if position < 0 or position >= MAX_STACK_HEIGHT or position >= len(self.stack):
            raise IndexError(f"Position `{position}` not valid!")

        # removing from given position to the end
        removed_from_stack = self.stack[position:]

        # everything up to that position stays
        self.stack = self.stack[:position]

        return removed_from_stack

    @property
    def color(self) -> Color:
        row = ord(self.position[0]) - ord("A") + 1
        col = self.position[1]

        return Color.BLACK if row % 2 == col % 2 else Color.WHITE

    @property
    def stack_height(self) -> int:
        return len(self.stack)

    @property
    def row(self) -> str:
        return self.position[0]

    @property
    def column(self) -> int:
        return self.position[1]

    def __repr__(self) -> str:  # to str
        return (
            f"Field(color={self.color},"
            f",position={self.position}"
            f",stack={self.stack})"
        )


__all__ = ["MAX_STACK_HEIGHT", "Color", "FieldPosition", "Field"]
