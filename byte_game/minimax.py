from typing import Dict, List, Optional, Tuple

from .model import MAX_STACK_HEIGHT, Board, Field, FieldPosition, Figure
from .playing import MoveDirection
from .state_change_operator import StateChangeOperator


def get_children_states_for_player(board: Board, figure: Figure) -> List[Board]:
    state_change_operator = StateChangeOperator(board, figure)
    return state_change_operator.ai_get_all_possible_states()


def get_neighbor_stacks(
    field_position: FieldPosition, board: Board
) -> Dict[MoveDirection, Field]:
    row = ord(field_position[0]) - ord("A")
    column = field_position[1]

    neighbors = {}

    # Up left.
    if not row == 0 and not column == 1:
        up_left_row = chr(row + ord("A") - 1)
        up_left_column = column - 1
        neighbors[MoveDirection.UL] = board[(up_left_row, up_left_column)]

    # Up right.
    if not row == 0 and not column == board.size:
        up_right_row = chr(row + ord("A") - 1)
        up_right_column = column + 1
        neighbors[MoveDirection.UR] = board[(up_right_row, up_right_column)]

    # Down left.
    if not row == board.size - 1 and not column == 1:
        down_left_row = chr(row + ord("A") + 1)
        down_left_column = column - 1
        neighbors[MoveDirection.DL] = board[(down_left_row, down_left_column)]

    # Down right.
    if not row == board.size - 1 and not column == board.size:
        down_right_row = chr(row + ord("A") + 1)
        down_right_column = column + 1
        neighbors[MoveDirection.DR] = board[(down_right_row, down_right_column)]

    return neighbors


def generate_state_facts(board: Board) -> Tuple[int, ...]:
    SCORE_WEIGHT = 1000
    EVEN_WEIGHT = 10
    ODD_WEIGHT = 2

    # Score has the heighest weight.
    score_fact = (board.first_player_score - board.second_player_score) * SCORE_WEIGHT

    # High stacks => we want to be on top of those!
    x_o_count_stacks = int(
        sum(
            (1 if field.stack[-1] == Figure.X else -1)
            * field.stack_height
            * (EVEN_WEIGHT if field.stack_height % 2 == 0 else ODD_WEIGHT)
            for row in board.matrix
            for field in row
            if field.stack_height > 0
        )
    )

    x_points = 0
    o_points = 0

    # for row in board.matrix:
    #     for field in row:
    #         if field.stack_height == 0:
    #             continue
    #         left_space_on_current_stack = MAX_STACK_HEIGHT - field.stack_height
    #         for neighbor_stack in get_neighbor_stacks(field.position, board).values():
    #             if len(neighbor_stack) == 0:
    #                 continue
    #             if (
    #                 neighbor_stack[-1] == Figure.X
    #                 and left_space_on_current_stack <= len(neighbor_stack)
    #                 and neighbor_stack[
    #                     len(neighbor_stack) - left_space_on_current_stack
    #                 ]
    #                 == Figure.X
    #             ):
    #                 x_points += SCORE_WEIGHT
    #             elif (
    #                 neighbor_stack[-1] == Figure.O
    #                 and left_space_on_current_stack <= len(neighbor_stack)
    #                 and neighbor_stack[
    #                     len(neighbor_stack) - left_space_on_current_stack
    #                 ]
    #                 == Figure.O
    #             ):
    #                 o_points -= SCORE_WEIGHT

    # avoid_merge_penalty = (
    #     sum(
    #         (
    #             1
    #             if field.stack_height == 7
    #             and any(
    #                 adjacent_field.stack_height > 0
    #                 and adjacent_field.stack[-1] == Figure.O
    #                 for adjacent_field in get_neighbor_stacks(
    #                     field.position, board
    #                 ).values()
    #             )
    #             else 0
    #             for row in board.matrix
    #             for field in row
    #         )
    #     )
    #     * SCORE_WEIGHT
    # )

    # All evaluation components.
    return score_fact, x_o_count_stacks  # , x_points, o_points, avoid_merge_penalty


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
