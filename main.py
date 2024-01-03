from byte_game.game import Game
from byte_game.user_interface import UserInteface

if __name__ == "__main__":
    ui = UserInteface()

    # Getting input parameters from user.

    board_size, chosen_figure, game_versus_ai = ui.get_input_parameters()

    game = Game(ui, board_size, chosen_figure, game_versus_ai)

    game.start()
