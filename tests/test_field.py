from byte_game.model import Color, Field


def test_field_color():
    assert Field(("E", 3)).color == Color.BLACK
    assert Field(("E", 2)).color == Color.WHITE
