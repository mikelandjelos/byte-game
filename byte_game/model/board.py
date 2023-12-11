from typing import TypeAlias
from .field import Field, FieldPosition
from .figure import Figure

MatrixOfFields: TypeAlias = list[list[Field]]


class Board:
    __CHAR_OFFSET = 65

    def __init__(self, board_size) -> None:
        if not _is_dimension_valid(board_size):
            raise ValueError(
                f"{board_size} is not a valid board dimension for Byte game!"
            )

        self.matrix: MatrixOfFields = []
        self.size = board_size

        for i in range(board_size):
            row = chr(Board.__CHAR_OFFSET + i)

            if i in (0, board_size - 1):
                # Do for first and last row
                # -> Fields with empty stack.
                self.matrix.append(
                    [Field((row, col), []) for col in range(1, board_size + 1)]
                )
            elif i % 2 != 0:
                # Do for odd rows
                # -> Alternating empty and fields with 'X'.
                self.matrix.append(
                    [
                        Field((row, col), [])
                        if col % 2 != 0
                        else Field((row, col), [Figure.X])
                        for col in range(1, board_size + 1)
                    ]
                )
            else:
                # Do for even rows
                # -> Alternating 'O' and empty fields.s
                self.matrix.append(
                    [
                        Field((row, col), [Figure.O])
                        if col % 2 != 0
                        else Field((row, col))
                        for col in range(1, board_size + 1)
                    ]
                )

    def __getitem__(self, position: FieldPosition) -> Field:
        row = ord(position[0]) - Board.__CHAR_OFFSET
        col = position[1] - 1  # 1-based
        return self.matrix[row][col]

    def __setitem__(self, position: FieldPosition, value: list) -> None:
        row = ord(position[0]) - Board.__CHAR_OFFSET
        col = position[1] - 1  # 1-based
        self.matrix[row][col] = Field(position, value)


def _is_dimension_valid(n: int) -> bool:
    return n >= 8 and n <= 16 and n % 2 == 0 and (n - 2) * (n / 2) % 8 == 0


__all__ = ["Board", "MatrixOfFields"]
