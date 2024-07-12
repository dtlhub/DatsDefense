from abc import ABCMeta, abstractmethod

from model import Command
from model.state import State


class Strategy(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def command(state: State) -> Command: ...

    @staticmethod
    @abstractmethod
    def name() -> str: ...
