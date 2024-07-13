from gameserver.strategy import Strategy

from model import Command, Location
from model.state import State


class StupidAttackStrategy(Strategy):
    @staticmethod
    def name() -> str:
        return "stupid attack"

    @staticmethod
    def command(state: State) -> Command:
        attacks = state.current_round.units.attack()
        base = state.current_round.units.base
        build: list[Location] = []
        for b in base:
            x, y = b.location.x, b.location.y
            build.append(Location(x - 1, y))
            build.append(Location(x + 1, y))
            build.append(Location(x, y - 1))
            build.append(Location(x, y + 1))
        return Command(
            attack=attacks,
            build=build,
            move_base=None,
        )
