from abc import ABCMeta
from dataclasses import dataclass

from gameserver.state import State


class Strategy(metaclass=ABCMeta):
    def make_moves(self, state: State) -> Move: ...
