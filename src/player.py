import dataclasses
from typing import Optional


@dataclasses.dataclass

class Player:
    name: str
    age: int
    a = dict({1:2, 3:4})
    addresses: Optional[list[str]] = None

    @property
    def player_gender(self) -> Optional[str]:
        return "Male"


Player(name="Rahul", age=20)