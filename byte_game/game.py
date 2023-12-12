from byte_game.playing.move import Move
from byte_game.playing.move_validator import MoveValidator

from .model import Board, Figure
from .playing import Player
from .state_change_operator import StateChangeOperator
from .user_interface import UserInteface
from .utils import clear_console


def is_move_valid(
    move: Move, board: Board, player: Player, ui: UserInteface = UserInteface()
) -> bool:
    move_validator = MoveValidator(move, board, player)

    # Basic checking.
    if not move_validator.boundaries_check:
        ui.show_message("Position out of bounds!")
        return False
    # Check if given row is inside boundaries.
    if move_validator.row_in_boundaries:
        ui.show_message(f"Row `{move.field_row}` invalid!")
        return False

    # Check if given column is inside boundaries.
    if move_validator.column_in_boundaries:
        ui.show_message(f"Column `{move.field_column}` invalid!")
        return False

    # Check if there are figures on given field.
    if move_validator.is_field_empty:
        ui.show_message(f"Field {move.field_position} is empty!")
        return False

    # Check if the stack is high enough.
    if move_validator.is_stack_high_enough:
        ui.show_message(
            f"There is no figure on field {move.field_position} at position {move.figure_position}!"
            f"\nStack height on that field is {board[move.field_position].stack_height}"
        )
        return False

    # Case 1: sva susedna polja su prazna i igrac je odabrao poziciju 0 i figura na toj poziciji pripada njemu a ne drugom igracu
    if move_validator.neighbor_fields_empty and move_validator.valid_chosen_figure:
        # Shortest path - ako ne zadovoljava ovaj uslov return False
        (
            is_shortest_path,
            allowed_positions,
        ) = move_validator.shortest_path_constraint
        if not is_shortest_path:
            ui.show_message(
                f"Invalid move! Shortest path constraint says valid moves are {allowed_positions}!"
            )
            return False
        return True
    # Case 2: postoji susedno polje koje nije prazno i vrsi se spajanje stack-ova
    else:
        if not move_validator.merge_checked:
            ui.show_message(
                f"Invalid move!"
            )  # Ovo ovamo mozda da se razdvoji na vise poruka???
            return False

    return True


class Game:
    def __init__(self, ui: UserInteface) -> None:
        self.ui = ui

    def is_over(self, board_size, first_player_score, second_player_score) -> int:
        winning_score = (board_size - 2) * (board_size // 2) / 2

        if first_player_score >= winning_score:
            return -1
        elif second_player_score >= winning_score:
            return 1
        return 0

    def next_move(self, player: Player, board: Board):
        while True:
            self.ui.show_message(f"Player {player.figure} is playing!")
            move = self.ui.get_next_move()

            if is_move_valid(
                move,
                board,
                player,
                self.ui,
            ):
                player.make_move(move, board)
                break

    def start(self):
        # Prompting user for input parameters.

        board_size, chosen_figure, game_versus_ai = self.ui.get_input_parameters()

        # Initializing game state for chosen dimension.

        board = Board(board_size)

        # Printing initial state.

        clear_console()
        self.ui.show_board(board)
        self.ui.show_score(0, 0)

        # Creating players

        first_player = Player(Figure.X)
        second_player = Player(Figure.O)

        # Game starts.

        while True:
            # First player makes a move.
            if game_versus_ai:
                if chosen_figure == first_player.figure:
                    self.next_move(first_player, board)
                else:
                    # AI plays a move.
                    state_change_operator = StateChangeOperator(board, first_player)
                    all_possible_states = state_change_operator.execute()
                    for state in all_possible_states:
                        self.ui.show_message("------------------------")
                        self.ui.show_board(state)
                    self.ui.show_message(
                        f"Number of states: {len(all_possible_states)}"
                    )
                    self.ui.show_message("------------------------")
                    self.ui.show_board(board)
                    raise NotImplementedError
            else:
                self.next_move(first_player, board)

            clear_console()
            self.ui.show_board(board)
            self.ui.show_score(first_player.score, second_player.score)

            # Second player makes a move.
            if game_versus_ai:
                if chosen_figure == second_player.figure:
                    self.next_move(second_player, board)
                else:
                    # AI plays a move.
                    state_change_operator = StateChangeOperator(board, second_player)
                    all_possible_states = state_change_operator.execute()
                    for state in all_possible_states:
                        self.ui.show_message("------------------------")
                        self.ui.show_board(state)
                    self.ui.show_message(
                        f"Number of states: {len(all_possible_states)}"
                    )
                    self.ui.show_message("------------------------")
                    self.ui.show_board(board)
                    raise NotImplementedError
            else:
                self.next_move(second_player, board)

            clear_console()
            self.ui.show_board(board)
            self.ui.show_score(first_player.score, second_player.score)

            # Determining if game is over.
            winner = self.is_over(board.size, first_player.score, second_player.score)

            if winner != 0:
                self.ui.show_message(
                    f"{'First' if winner == -1 else 'Second'} player has won!"
                )
                break
