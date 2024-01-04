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


# region Prunning Minimax


def generate_state_facts(board: Board) -> Tuple[int, ...]:
    score_component = (board.first_player_score - board.second_player_score) * 100

    x_o_count_component = x_o_count_component = sum(
        (1 if field.stack[-1] == Figure.X else -1) * field.stack_height
        for row in board.matrix
        for field in row
        if field.stack_height > 0
    )

    return (score_component, x_o_count_component)


def evaluate_state(board: Board) -> int:
    facts = generate_state_facts(board)
    return sum(facts)


def max_value(
    board: Board,
    depth: int,
    figure: Figure,
    alpha: Tuple[Board, int],
    beta: Tuple[Board, int],
) -> Tuple[Board, int]:
    if depth == 0 or board.finished():
        return (board, evaluate_state(board))

    children_states = get_children_states_for_player(board, figure)

    if children_states == []:
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


def min_value(
    board: Board,
    depth: int,
    figure: Figure,
    alpha: Tuple[Board, int],
    beta: Tuple[Board, int],
) -> Tuple[Board, int]:
    if depth == 0 or board.finished():
        return (board, evaluate_state(board))

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


def minimax(
    board: Board,
    depth: int,
    figure: Figure,
    alpha: Tuple[Board, int],
    beta: Tuple[Board, int],
) -> Tuple[Board, int]:
    # Calculating the best state.
    board._parent = None
    minimax_value = max_value if figure == Figure.X else min_value
    minimax_valued_state = minimax_value(board, depth, figure, alpha, beta)

    # Backtracking.
    curr = minimax_valued_state[0]
    prev = minimax_valued_state[0]

    while curr._parent is not None:
        prev = curr
        curr = curr._parent

    return prev, minimax_valued_state[1]


# endregion !Prunning Minimax
