from .model import Board, Figure
from .playing import Move, MoveValidator, Player
from .user_interface import UserInteface
from .utils import clear_console


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

    def is_move_valid(self, move: Move, board: Board, player: Player) -> bool:
        move_validator = MoveValidator(move, board, player)

        # Basic checking.
        if not move_validator.boundaries_check:
            self.ui.show_message("Position out of bounds!")
            return False
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

        # Case 1: sva susedna polja su prazna i igrac je odabrao poziciju 0 i figura na toj poziciji pripada njemu a ne drugom igracu
        if move_validator.neighbor_fields_empty and move_validator.valid_chosen_figure:
            # Shortest path - ako ne zadovoljava ovaj uslov return False
            (
                is_shortest_path,
                allowed_positions,
            ) = move_validator.shortest_path_constraint
            if is_shortest_path:
                self.ui.show_message(
                    f"Invalid move! Shortest path constraint says valid moves are {allowed_positions}!"
                )
                return False
            return True
        # Case 2: postoji susedno polje koje nije prazno i vrsi se spajanje stack-ova
        else:
            if not move_validator.merge_checked:
                self.ui.show_message(
                    f"Invalid move!"
                )  # Ovo ovamo mozda da se razdvoji na vise poruka???
                return False

        return True

    def next_move(self, player: Player, board: Board):
        while True:
            self.ui.show_message(f"Player {player.figure} is playing!")
            move = self.ui.get_next_move()

            if self.is_move_valid(move, board, player):
                player.make_move(move, board)
                break

    """
    def generate_moves(self, board: Board, player: Player, field_position, figure_position, list_of_moves):
        move = Move(field_position, figure_position, MoveDirection.DL)
        if self.is_move_valid(move, board, player):
            list_of_moves.append(Move(field_position, figure_position, move))

        move = Move(field_position, figure_position, MoveDirection.DR)
        if self.is_move_valid(move, board, player):
            list_of_moves.append(Move(field_position, figure_position, move))

        move = Move(field_position, figure_position, MoveDirection.UL)
        if self.is_move_valid(move, board, player):
            list_of_moves.append(Move(field_position, figure_position, move))

        move = Move(field_position, figure_position, MoveDirection.UR)
        if self.is_move_valid(move, board, player):
            list_of_moves.append(Move(field_position, figure_position, move))

    def process_field(self, board: Board, player: Player, field_position, stack, list_of_moves):
        for i, figure in enumerate(stack):
            if figure == player.figure:
                self.generate_moves(board, player, field_position, i, list_of_moves)

    def get_all_possible_moves(self, player: Player, board: Board):
        list_of_moves = []
        for i, row in enumerate(board.matrix):
            # even rows
            if i % 2 == 0:
                for j in range(0, board.size, 2):
                    field = row[j]
                    if field.stack_height > 0:
                        self.process_field(board, player, field.position, field.stack, list_of_moves)
            # odd rows
            else:
                for j in range(1, board.size, 2):
                    field = row[j]
                    if field.stack_height > 0:
                        self.process_field(board, player, field.position, field.stack, list_of_moves)
        return list_of_moves
    """

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
                    raise NotImplementedError
            else:
                # print("Svi moguci potezi su: ")
                # all_moves = self.get_all_possible_moves(first_player, board)
                # for move in all_moves:
                #     print(move)

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
