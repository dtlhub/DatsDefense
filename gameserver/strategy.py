from abc import ABCMeta, abstractmethod

from model import Command
from model.state import State


class Strategy(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def command(state: State) -> Command:
        """Returns either command to command to execute, or tuple of name of strategy to switch to and command to execute."""

    @staticmethod
    @abstractmethod
    def name() -> str: ...
