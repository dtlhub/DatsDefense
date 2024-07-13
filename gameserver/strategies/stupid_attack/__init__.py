from gameserver.strategy import Strategy

from model import Command, Location
from model.state import State


class StupidAttackStrategy(Strategy):
    @staticmethod
    def name() -> str:
        return "stupid_attack"

    @staticmethod
    def command(state: State) -> Command:
        attacks = state.current_round.units.attack()
        base = state.current_round.units.base
        build: set[Location] = set()
        base_locations: set[Location] = set()
        for b in base:
            x, y = b.location.x, b.location.y
            base_locations.add(Location(x, y))
            build.add(Location(x - 1, y))
            build.add(Location(x + 1, y))
            build.add(Location(x, y - 1))
            build.add(Location(x, y + 1))

        return Command(
            attack=attacks,
            build=list(build - base_locations),
            move_base=None,
        )

    # @staticmethod
    # def get_builder_commands()
