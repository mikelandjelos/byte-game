from typing import Optional

from byte_game.playing.move import Move
from byte_game.playing.move_validator import MoveValidator

from .model import Board, Figure
from .playing import Player
from .state_change_operator import StateChangeOperator
from .user_interface import UserInteface
from .utils import clear_console


def is_move_valid(
    move: Move,
    board: Board,
    playing_figure: Figure,
    print_flag: bool = False,
    ui: UserInteface = UserInteface(),
) -> bool:
    move_validator = MoveValidator(move, board, playing_figure)

    # Basic checking.
    if not move_validator.boundaries_check:
        if print_flag:
            ui.show_message("Position out of bounds!")
        return False

    # Check if given row is inside boundaries.
    if move_validator.row_in_boundaries:
        if print_flag:
            ui.show_message(f"Row `{move.field_row}` invalid!")
        return False

    # Check if given column is inside boundaries.
    if move_validator.column_in_boundaries:
        if print_flag:
            ui.show_message(f"Column `{move.field_column}` invalid!")
        return False

    # Check if there are figures on given field.
    if move_validator.is_field_empty:
        if print_flag:
            ui.show_message(f"Field {move.field_position} is empty!")
        return False

    # Check if the stack is high enough.
    if move_validator.is_stack_high_enough:
        if print_flag:
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
            if print_flag:
                ui.show_message(
                    f"Invalid move! Shortest path constraint says valid moves are {allowed_positions}!"
                )
            return False
        return True
    # Case 2: postoji susedno polje koje nije prazno i vrsi se spajanje stack-ova
    else:
        if not move_validator.merge_checked:
            if print_flag:
                ui.show_message(
                    f"Invalid move!"
                )  # Ovo ovamo mozda da se razdvoji na vise poruka???
            return False

    return True


class Game:
    def __init__(self, ui: UserInteface) -> None:
        # Initializing user interface.
        self.ui = ui

        # Creating players.
        self.first_player = Player(Figure.X)
        self.second_player = Player(Figure.O)

    def is_over(
        self, board_size: int, first_player_score: int, second_player_score: int
    ) -> int:
        winning_score = ((((board_size - 2) * board_size) // 2) // 8) / 2

        if first_player_score >= winning_score:
            return -1
        elif second_player_score >= winning_score:
            return 1
        return 0

    def player_next_move(self, playing_figure: Figure, board: Board):
        while True:
            self.ui.show_message(f"Player with the {playing_figure} figure is playing!")
            move = self.ui.get_next_move()

            if is_move_valid(move, board, playing_figure, print_flag=True, ui=self.ui):
                figure_to_update = None
                if self.first_player.figure == playing_figure:
                    figure_to_update = self.first_player.make_move(move, board)
                else:
                    figure_to_update = self.second_player.make_move(move, board)

                if figure_to_update is not None:
                    if figure_to_update == self.first_player.figure:
                        self.first_player.score += 1
                    else:
                        self.second_player.score += 1

                break

    def next_move(
        self,
        board: Board,
        game_versus_ai: bool,
        player: Player,
        chosen_figure: Optional[Figure],
    ):
        player_move_generator = StateChangeOperator(board, player.figure)
        possible_moves_for_player = player_move_generator.pvp_get_all_possible_moves()

        # If game is played versus AI.
        if game_versus_ai:
            if chosen_figure == player.figure:
                if len(possible_moves_for_player) == 1:
                    self.ui.show_message(
                        f"There is one valid move for player {player.figure}"
                    )
                    self.ui.show_message(f"{possible_moves_for_player[0]}")
                    self.player_next_move(player.figure, board)
                elif len(possible_moves_for_player) > 1:
                    self.player_next_move(player.figure, board)
            else:
                # AI plays a move.
                raise NotImplementedError

        # If game is player in player-versus-player mode.
        else:
            if len(possible_moves_for_player) == 1:
                self.ui.show_message(
                    f"There is one valid move for player {player.figure}"
                )
                self.ui.show_message(f"{possible_moves_for_player[0]}")
                self.player_next_move(player.figure, board)
            elif len(possible_moves_for_player) > 1:
                self.player_next_move(player.figure, board)

    def start(self):
        # Prompting user for input parameters.

        board_size, chosen_figure, game_versus_ai = self.ui.get_input_parameters()

        # Initializing game state for chosen dimension.

        board = Board(board_size)

        # Printing initial state.

        clear_console()
        self.ui.show_board(board)
        self.ui.show_score(0, 0)

        # Game starts.

        while True:
            # First player makes a move.

            self.next_move(board, game_versus_ai, self.first_player, chosen_figure)

            clear_console()
            self.ui.show_board(board)
            self.ui.show_score(self.first_player.score, self.second_player.score)

            # Second player makes a move.

            self.next_move(board, game_versus_ai, self.second_player, chosen_figure)

            clear_console()
            self.ui.show_board(board)
            self.ui.show_score(self.first_player.score, self.second_player.score)

            # Determining if game is over.
            winner = self.is_over(
                board.size, self.first_player.score, self.second_player.score
            )

            if winner != 0:
                self.ui.show_message(
                    f"{'First' if winner == -1 else 'Second'} player has won!"
                )
                break
