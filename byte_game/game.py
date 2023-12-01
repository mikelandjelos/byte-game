from .model import Board, Color, Figure
from .playing import Move, Player
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

    def is_move_valid(self, move: Move, board: Board) -> bool:
        row = ord(move.field_position[0]) - ord("A") + 1
        column = move.field_position[1]

        # Check if given field position exists
        # row check
        if row <= 0 or row > board.size:
            self.ui.show_message(f"Row `{move.field_position[0]}` invalid!")
            return False

        # column check
        if column <= 0 or column > board.size:
            self.ui.show_message(f"Column `{move.field_position[0]}` invalid!")
            return False

        # Check if there are figures on given field
        if board[move.field_position].stack_height == 0:
            self.ui.show_message(f"Field {move.field_position} is empty!")
            return False

        # Check if the stack is high enough
        if board[move.field_position].stack_height - 1 < move.figure_position:
            self.ui.show_message(
                f"There is no figure on field {move.field_position} at position {move.figure_position}!"
                f"\nStack heigh on that field is {board[move.field_position].stack_height}"
            )
            return False

        return True

    def next_move(self, player: Player, board: Board):
        while True:
            self.ui.show_message(f"Player {player.figure} is playing!")
            move = self.ui.get_next_move()

            if self.is_move_valid(move, board):
                player.make_move(move, board)  # raises NotImplementedError
                break

    def start(self):
        # Prompting user for input parameters.

        board_size, chosen_figure = self.ui.get_input_parameters()

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
            if chosen_figure == first_player.figure:
                self.next_move(first_player, board)

            self.ui.show_board(board)
            self.ui.show_score(first_player.score, second_player.score)

            # Second player makes a move.
            if chosen_figure == second_player.figure:
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
