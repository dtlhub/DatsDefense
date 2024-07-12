from gameserver.strategy import Strategy

from model import Command
from model.state import State


class IdleStrategy(Strategy):
    @staticmethod
    def command(state: State) -> Command:
        return Command(
            attack=[],
            build=[],
            move_base=None,
        )

    @staticmethod
    def name() -> str:
        return "idle"
