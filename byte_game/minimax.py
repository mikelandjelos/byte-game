import sys
from typing import List, Tuple

from .model import Board, Figure
from .state_change_operator import StateChangeOperator


def next_possible_states(board: Board, figure: Figure) -> List[Board]:
    state_change_operator = StateChangeOperator(board, figure)
    return state_change_operator.ai_get_all_possible_states()


def max_state(lsv: List[Tuple[Board, int]]) -> Tuple[Board, int]:
    return max(lsv, key=lambda x: x[1])


def min_state(lsv: List[Tuple[Board, int]]) -> Tuple[Board, int]:
    return min(lsv, key=lambda x: x[1])


def evaluate_state(board: Board):
    raise NotImplementedError


def minimax(board: Board, depth: int, playing_figure: Figure) -> Tuple[Board, int]:
    if board.finished():
        return (board, -1)

    list_of_states = next_possible_states(board, playing_figure)
    min_max_state = max_state if playing_figure == Figure.X else min_state

    if depth == 0 or not list_of_states:
        return (board, evaluate_state(board))

    return min_max_state(
        [
            minimax(x, depth - 1, Figure.O if playing_figure == Figure.X else Figure.X)
            for x in list_of_states
        ]
    )
