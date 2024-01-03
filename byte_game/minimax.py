from random import randint
from typing import List, Tuple

from .model import Board, Figure
from .state_change_operator import StateChangeOperator


def get_children_states_for_player(board: Board, figure: Figure) -> List[Board]:
    state_change_operator = StateChangeOperator(board, figure)
    return state_change_operator.ai_get_all_possible_states()


def max_state(lsv: List[Tuple[Board, int]]) -> Tuple[Board, int]:
    return max(lsv, key=lambda x: x[1])


def min_state(lsv: List[Tuple[Board, int]]) -> Tuple[Board, int]:
    return min(lsv, key=lambda x: x[1])


def evaluate_state(board: Board) -> int:
    return 0


# region Plain minimax

counter = 0


def minimax_recursive(
    board: Board, depth: int, playing_figure: Figure
) -> Tuple[Board, int]:
    global counter
    counter += 1
    print(counter)
    if depth == 0 or board.finished():
        return (board, evaluate_state(board))

    list_of_states = get_children_states_for_player(board, playing_figure)

    if list_of_states == []:
        return (board, evaluate_state(board))

    min_max_state = max_state if playing_figure == Figure.X else min_state
    other_figure = Figure.O if playing_figure == Figure.X else Figure.X

    return min_max_state(
        [minimax_recursive(state, depth - 1, other_figure) for state in list_of_states]
    )


def minimax(board: Board, depth: int, playing_figure: Figure) -> Board:
    children_states = get_children_states_for_player(board, playing_figure)

    evaluated_children_states = [
        (state, minimax_recursive(state, depth - 1, playing_figure)[1])
        for state in children_states
    ]

    min_max_state = max_state if playing_figure == Figure.X else min_state
    return min_max_state(evaluated_children_states)[0]


# endregion !Plain Minimax

# region Prunning Minimax


def max_value(
    board: Board,
    depth: int,
    figure: Figure,
    alpha: Tuple[Board, int],
    beta: Tuple[Board, int],
) -> Tuple[Board, int]:
    global counter
    counter += 1
    print(counter)
    children_states = get_children_states_for_player(board, figure)

    if depth == 0 or children_states == [] or board.finished():
        return (board, evaluate_state(board))

    for state in children_states:
        alpha = max(
            alpha,
            min_value(state, depth - 1, figure, alpha, beta),
            key=lambda x: x[1],
        )
        if alpha[1] >= beta[1]:
            return beta

    return alpha


#            x
#          / | \
#         y  z  p   8x8 => 35
#        /
#       t   ...
#      /
#     s     ...


def min_value(
    board: Board,
    depth: int,
    figure: Figure,
    alpha: Tuple[Board, int],
    beta: Tuple[Board, int],
) -> Tuple[Board, int]:
    global counter
    counter += 1
    print(counter)
    children_states = get_children_states_for_player(board, figure)

    if depth == 0 or children_states == [] or board.finished():
        return (board, evaluate_state(board))

    for state in children_states:
        beta = min(
            beta,
            max_value(state, depth - 1, figure, alpha, beta),
            key=lambda x: x[1],
        )
        if beta[1] <= alpha[1]:
            return alpha

    return beta


def minimax_prunning(
    board: Board,
    depth: int,
    figure: Figure,
    alpha: Tuple[Board, int],
    beta: Tuple[Board, int],
):
    if figure == Figure.X:
        return max_value(board, depth, figure, alpha, beta)
    else:
        return min_value(board, depth, figure, alpha, beta)


# endregion !Prunning Minimax
