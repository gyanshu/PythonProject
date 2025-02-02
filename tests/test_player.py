# tests/test_player.py

import pytest
from src.player import Player


@pytest.fixture
def player():
    return Player(name="Alice", age=25)

def test_player_initialization(player):
    assert player.name == "Alice"
    assert player.age == 25
    assert player.a == dict({1:2, 3:4})

    with pytest.raises(TypeError):
        raise TypeError


def test_player_name_assignment():
    player = Player(name="Bob", age=30)
    assert player.name == "Bob"
    assert player.player_gender == "Male"


def test_player_age_assignment():
    player = Player(name="Charlie", age=20)
    assert player.age == 20

@pytest.mark.skip(reason="Not implemented yet")
def test_player():
    assert False
