from abc import ABCMeta
from dataclasses import dataclass

from gameserver.state import State


@dataclass
class Move:
    def to_json(self): ...


class Strategy(metaclass=ABCMeta):
    def make_moves(self, state: State) -> Move: ...
