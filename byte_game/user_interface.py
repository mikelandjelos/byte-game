from collections import defaultdict
from typing import Tuple

from .model import Board, Color, Field, Figure
from .playing import Move, MoveDirection
from .utils import clear_console


class UserInteface:
    # region Output

    def _field_to_print_str(self, field: Field) -> str:
        if field.color == Color.WHITE:
            return "    \n    \n    "
        string_values = [
            ". " if i >= len(field.stack) else f"{field.stack[i]} " for i in range(9)
        ]
        return f'{"".join(string_values[6:])}\n{"".join(string_values[3:6])}\n{"".join(string_values[:3])}'

    def _print_row(self, row: list[Field]) -> None:
        some = defaultdict(list)

        letter = row[0].row

        some[0].append("      ")
        some[1].append(f"  {letter}   ")
        some[2].append("      ")

        if (ord(letter) - 65) % 2 != 0:
            some[0].append(" ")
            some[1].append(" ")
            some[2].append(" ")

        for field in row:
            field_str = self._field_to_print_str(field)
            parts = field_str.split("\n")
            some[0].append(parts[0])
            some[1].append(parts[1])
            some[2].append(parts[2])

        print(f'{"".join(some[0])}\n{"".join(some[1])}\n{"".join(some[2])}')

    def show_board(self, board: Board) -> None:
        print("        ", end="")
        for i in range(1, board.size + 1):
            if i < 9:
                print(f"{i}    ", end="")
            else:
                print(f" {i}  ", end="")
        print()
        for row in board.matrix:
            self._print_row(row)

        self.show_score(board.first_player_score, board.second_player_score)

    def show_score(self, first_player_score: int, second_player_score: int) -> None:
        print(f"X: {first_player_score} O: {second_player_score}")

    def show_message(self, message: str):
        print(message)

    # endregion !Output

    # region Input

    def __get_dimension(self) -> int:
        valid_dimensions = [
            str(n)
            for n in range(8, 16 + 1)
            if n % 2 == 0 and (n - 2) * (n / 2) % 8 == 0
        ]

        while True:
            dimension = input(f"Enter dimension: {valid_dimensions}\n=> ")

            if dimension in valid_dimensions:
                break

            print(
                f"\nInvalid dimension! Please enter one of the following: \n{valid_dimensions}\n"
            )

        return int(dimension)

    def __get_figure(self) -> Figure:
        valid_figures = [s.value for s in Figure]

        while True:
            figure = str(input(f"Choose figure: {valid_figures}\n=> ")).upper()

            if figure in valid_figures:
                return Figure(figure)

            print(
                f"\nInvalid figure! Please enter one of the following: \n{valid_figures}\n"
            )

    def __play_versus_ai(self) -> bool:
        while True:
            answer = input("Play versus AI? [Y/n]\n")

            if answer in ("Y", "y", ""):
                return True
            elif answer in ("N", "n"):
                return False
            else:
                print("Please enter `Y` or `N`!")

    def __confirm_choices(self, choices: Tuple[int, Figure | None, bool]) -> bool:
        board_dimensions = f"{choices[0]}x{choices[0]} board"
        chosen_figure = f"| {choices[1]} figure " if choices[2] else ""
        play_versus_ai = "AI" if choices[2] else "PVP"

        while True:
            answer = input(
                f"Confirm choices [ {board_dimensions} | {play_versus_ai + ' mode'} {chosen_figure}]? [Y/n]\n"
            )

            if answer in ("Y", "y", ""):
                return True
            elif answer in ("N", "n"):
                return False
            else:
                print("Please enter `Y` or `N`!")

    def get_input_parameters(
        self,
    ) -> Tuple[int, Figure | None, bool]:
        while True:
            clear_console()
            n = self.__get_dimension()

            clear_console()
            play_versus_ai = self.__play_versus_ai()

            if play_versus_ai:
                clear_console()
                chosen_figure = self.__get_figure()
            else:
                chosen_figure = None

            clear_console()
            if self.__confirm_choices((n, chosen_figure, play_versus_ai)):
                break

        return n, chosen_figure, play_versus_ai

    def get_next_move(self) -> Move:
        while True:
            move_str = input("Enter your move: ")
            try:
                # Input.

                # Parsing.
                move_str_arr = [token for token in move_str.split(" ") if token != ""]
                field_position = (move_str_arr[0].upper(), int(move_str_arr[1]))
                figure_position = int(move_str_arr[2])
                move_direction = MoveDirection[move_str_arr[3].upper()]

                return Move(field_position, figure_position, move_direction)
            except Exception:
                print(
                    f"Input `{move_str}` invalid! "
                    "\nPlease enter move in format "
                    "`<row letter> <column number> <stack position> <move direction>`\n"
                    "Move directions can be: `UL`, `UR`, `DL`, `DR`"
                )

    # endregion !Input
