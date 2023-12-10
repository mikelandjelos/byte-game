import os
from queue import Queue

from .model import Board, Field, FieldPosition


def clear_console():
    command = "clear"
    if os.name in ("nt", "dos"):  # If Machine is running on Windows, use cls
        command = "cls"

    os.system(command)


def get_neighbors(
    field_position: FieldPosition, board_size: int = 8
) -> list[FieldPosition]:
    row = ord(field_position[0]) - ord("A")
    column = field_position[1]

    neighbors = []

    # Up left.
    if not row == 0 and not column == 1:
        up_left_row = chr(row + ord("A") - 1)
        up_left_column = column - 1
        neighbors.append((up_left_row, up_left_column))

    # Up right.
    if not row == 0 and not column == board_size:
        up_right_row = chr(row + ord("A") - 1)
        up_right_column = column + 1
        neighbors.append((up_right_row, up_right_column))

    # Down left.
    if not row == board_size - 1 and not column == 1:
        down_left_row = chr(row + ord("A") + 1)
        down_left_column = column - 1
        neighbors.append((down_left_row, down_left_column))

    # Down right.
    if not row == board_size - 1 and not column == board_size:
        down_right_row = chr(row + ord("A") + 1)
        down_right_column = column + 1
        neighbors.append((down_right_row, down_right_column))

    return neighbors


def path_to_closest_nonempty_position(
    board: Board, starting_position: FieldPosition
) -> list[FieldPosition]:
    # Problem initialization.
    queue_positions: Queue[FieldPosition] = Queue(board.size**2 / 2)
    visited = set()
    prev_positions = dict()
    prev_positions[starting_position] = None
    visited.add(starting_position)
    queue_positions.put(starting_position)
    end_positions = []

    while not queue_positions.empty():
        position = queue_positions.get()

        for neighbor_position in get_neighbors(position, board.size):
            if neighbor_position not in visited:
                prev_positions[neighbor_position] = position

                # If non empty stack found.
                if (
                    neighbor_position != starting_position
                    and board[neighbor_position].stack_height != 0
                ):
                    end_positions.append(neighbor_position)

                visited.add(neighbor_position)
                queue_positions.put(neighbor_position)

    paths = []
    for end_position in end_positions:
        path = []
        if end_position != None:
            path.append(end_position)
            prev = prev_positions[end_position]
            while prev is not None:
                path.append(prev)
                prev = prev_positions[prev]
            path.reverse()
        paths.append(path)

    min_len = min(len(path) for path in paths)

    return [path for path in paths if len(path) == min_len]


__all__ = ["clear_console", "get_neighbors", "path_to_closest_nonempty_position"]
