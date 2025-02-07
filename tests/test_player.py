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


def test_player_name_assignment(player):
    assert player.name == "Bob"
    assert player.player_gender == "Male"


def test_player_age_assignment(player):
    assert player.age == 20

@pytest.mark.skip(reason="Not implemented yet")
def test_player():
    assert False


'''
1. coding - 
2. HLD - 45 mins
3. bug squash - public git repo, debug, debugger, stack trace - 1 hr
4. integration - sample data, external APIs integration, coding, correctness, abstractions, readable, interaction collaboration - 1 hr
5. HM - tell me a time - past experience - 45 mins
'''

