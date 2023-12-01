from byte_game.game import Game
from byte_game.user_interface import UserInteface

if __name__ == "__main__":
    ui = UserInteface()
    game = Game(ui)

    game.start()
