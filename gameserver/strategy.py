from abc import ABCMeta, abstractmethod

from model import Command
from model.state import State


class Strategy(metaclass=ABCMeta):
    @abstractmethod
    @staticmethod
    def command(state: State) -> Command: ...
