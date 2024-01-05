from typing import List, Tuple

from .model import MAX_STACK_HEIGHT, Board, Field, FieldPosition, Figure
from .playing import MoveDirection
from .state_change_operator import StateChangeOperator


def get_children_states_for_player(board: Board, figure: Figure) -> List[Board]:
    state_change_operator = StateChangeOperator(board, figure)
    return state_change_operator.ai_get_all_possible_states()


def generate_state_facts(board: Board) -> Tuple[int, ...]:
    SCORE_WEIGHT = 1000
    COUNT_WEIGHT = 20

    # Score has the heighest weight.
    score_fact = (board.first_player_score - board.second_player_score) * SCORE_WEIGHT

    # High stacks.
    stacks_count = sum(
        (1 if field.stack[-1] == Figure.X else -1) * field.stack_height * COUNT_WEIGHT
        for row in board.matrix
        for field in row
        if field.stack_height > 0
    )

    # All evaluation components.
    return score_fact, stacks_count


def evaluate_state(board: Board) -> int:
    facts = generate_state_facts(board)
    return sum(facts)


def maximize(
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
            minimize(state, depth - 1, figure, alpha, beta),
            key=lambda x: x[1],
        )
        if alpha[1] >= beta[1]:
            return beta

    return alpha


def minimize(
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
            maximize(state, depth - 1, figure, alpha, beta),
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
    minimax_value = maximize if figure == Figure.X else minimize
    best_board, best_eval = minimax_value(board, depth, figure, alpha, beta)

    # Backtracking to get next move.
    curr = best_board
    prev = best_board

    while curr._parent is not None:
        prev = curr
        curr = curr._parent

    return prev, best_eval
