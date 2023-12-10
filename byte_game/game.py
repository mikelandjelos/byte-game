from .model import Board, Figure
from .playing import Move, MoveValidator, Player
from .user_interface import UserInteface


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

    def is_move_valid(self, move: Move, board: Board,player:Player) -> bool:
        move_validator = MoveValidator(move, board,player)

        # Basic checking.

        # Check if given row is inside boundaries.
        if move_validator.row_in_boundaries:
            self.ui.show_message(f"Row `{move.field_row}` invalid!")
            return False

        # Check if given column is inside boundaries.
        if move_validator.column_in_boundaries:
            self.ui.show_message(f"Column `{move.field_column}` invalid!")
            return False

        # Check if there are figures on given field.
        if move_validator.is_field_empty:
            self.ui.show_message(f"Field {move.field_position} is empty!")
            return False

        # Check if the stack is high enough.
        if move_validator.is_stack_high_enough:
            self.ui.show_message(
                f"There is no figure on field {move.field_position} at position {move.figure_position}!"
                f"\nStack height on that field is {board[move.field_position].stack_height}"
            )
            return False
        if move_validator.neighbor_fields_empty:
            ...
        else:
            if not move_validator.merge_checked:
                self.ui.show_message(f"Stack can't be merged!")
                return False
        # Game rules checking

        # OVAJ KOMENTAR TREBA DA BUDE SKLONJEN NAKON IZRADE
        # Zadatak 2 - PRVI DEO
        # Realizovati funkcije koje na osnovu konkretnog poteza i stanje
        # problema (igre) proveravaju njegovu valjanost
        #   - Realizovati funkcije koje proveravaju da li su susedna polja prazna
        #   - Realizovati funkcije koje na osnovu konkretnog poteza i stanje igre
        #     proveravaju da li on vodi ka jednom od najbližih stekova (figura)
        #   - Realizovati funkcije koje na osnovu konkretnog poteza i stanje igre
        #     proveravaju da li se potez može odigrati prema pravilima pomeranja
        #     definisanim za stekove
        # Ideja:
        #   - Funkcije mogu da se napisu u klasi MoveValidator (/byte_game/playing/move_validator.py),
        #     pa da se samo pozivaju, nalik ovim gore, uz stampanje odgovarajuce poruke

        return True

    def next_move(self, player: Player, board: Board):
        while True:
            self.ui.show_message(f"Player {player.figure} is playing!")
            move = self.ui.get_next_move()

            if self.is_move_valid(move, board,player):
                # OVAJ KOMENTAR TREBA DA BUDE SKLONJEN NAKON IZRADE
                # Zadatak 2 - DRUGI DEO
                # Realizovati funkcije koje implementiraju operator promene stanja problema (igre)
                #   - Realizovati funkcije koje na osnovu zadatog poteza i zadatog stanja igre formiraju novo
                #     stanje igre
                #   - Realizovati funkcije koje na osnovu zadatog igrača na potezu i zadatog stanje igre (table)
                #     formiraju sve moguće poteze
                #   - Realizovati funkcije koje na osnovu svih mogućih poteza formiranju sva moguća stanja igre,
                #     korišćenjem funkcija iz prethodne dve stavke
                # Ideja:
                #   - Ako moze sve unutar funkcije Player.make_move

                player.make_move(move, board)
                break

    def start(self):
        # Prompting user for input parameters.

        board_size, chosen_figure, game_versus_ai = self.ui.get_input_parameters()

        # Initializing game state for chosen dimension.

        board = Board(board_size)

        # Printing initial state.

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
                    raise NotImplementedError
            else:
                self.next_move(first_player, board)

            self.ui.show_board(board)
            self.ui.show_score(first_player.score, second_player.score)

            # Second player makes a move.
            if game_versus_ai:
                if chosen_figure == second_player.figure:
                    self.next_move(second_player, board)
                else:
                    # AI plays a move.
                    raise NotImplementedError
            else:
                self.next_move(second_player, board)

            self.ui.show_board(board)
            self.ui.show_score(first_player.score, second_player.score)

            # Determining if game is over.
            winner = self.is_over(board.size, first_player.score, second_player.score)

            if winner != 0:
                self.ui.show_message(
                    f"{'First' if winner == -1 else 'Second'} player has won!"
                )
                break
