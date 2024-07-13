from gameserver.strategy import Strategy

from model import Command
from model.state import State


class McmfAttackStrategy(Strategy):
    @staticmethod
    def name() -> str:
        return "mcmf_attack"

    @staticmethod
    def command(state: State) -> Command:
        return Command(
            attack=[],
            build=[],
            move_base=None,
        )
