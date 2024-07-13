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
        build, new_center = StupidAttackStrategy.get_builder_commands(state)
        return Command(
            attack=attacks,
            build=build,
            move_base=new_center,
        )

    @staticmethod
    def get_builder_commands(state: State) -> tuple[list[Location], Location | None]:
        xs: list[int] = []
        ys: list[int] = []
        limit = state.current_round.units.player.gold

        base = state.current_round.units.base
        if len(base) == 0:
            return [], None

        for b in base:
            xs.append(b.location.x)
            ys.append(b.location.y)

        center_x = sum(xs) / len(xs)
        center_y = sum(ys) / len(ys)
        new_head = Location(
            x=round(center_x),
            y=round(center_y),
        )

        base_locations: set[Location] = set()
        for b in base:
            base_locations.add(b.location)

        neighbours: set[Location] = set()
        for b in base:
            x, y = b.location.x, b.location.y
            base_locations.add(Location(x, y))
            neighbours.add(Location(x - 1, y))
            neighbours.add(Location(x + 1, y))
            neighbours.add(Location(x, y - 1))
            neighbours.add(Location(x, y + 1))
        non_ocupied = neighbours - base_locations

        sorted_by_proximity_to_center = sorted(
            non_ocupied, key=lambda loc: new_head.distance(loc)
        )
        available = sorted_by_proximity_to_center[:limit]
        return available, new_head
