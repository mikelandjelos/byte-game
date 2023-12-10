from byte_game.model import Color, Field
from byte_game.utils import get_neighbors


def test_field_color():
    assert Field(("E", 3)).color == Color.BLACK
    assert Field(("E", 2)).color == Color.WHITE


def test_get_neighbors():
    neighbors_A1 = get_neighbors(("A", 1), 8)
    assert neighbors_A1 == [("B", 2)]

    neighbors_H8 = get_neighbors(("H", 8), 8)
    assert neighbors_H8 == [("G", 7)]

    neighbors_D4 = get_neighbors(("D", 4), 8)
    assert neighbors_D4 == [("C", 3), ("C", 5), ("E", 3), ("E", 5)]

    neighbors_E1 = get_neighbors(("E", 1), 8)
    assert neighbors_E1 == [("D", 2), ("F", 2)]
