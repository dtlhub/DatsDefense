from gameserver.strategy import Strategy

from model import Command, Location
from model.state import State
from itertools import chain
from typing import Generator


def neighbours(loc: Location) -> Generator[Location, None]:
    for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
        yield Location(loc.x + dx, loc.y + dy)


def neighbours_with_diag(loc: Location) -> Generator[Location, None]:
    for dx, dy in [
        (1, 0),
        (0, 1),
        (-1, 0),
        (0, -1),
        (1, 1),
        (1, -1),
        (-1, 1),
        (-1, -1),
    ]:
        yield Location(loc.x + dx, loc.y + dy)


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
        zombies = state.current_round.units.zombies
        zpots = state.current_round.world.zpots
        enemy_bases = state.current_round.units.enemy_bases

        if len(base) == 0:
            return [], None

        for obj in base:
            xs.append(obj.location.x)
            ys.append(obj.location.y)

        center_x = sum(xs) / len(xs)
        center_y = sum(ys) / len(ys)
        center = Location(
            x=round(center_x),
            y=round(center_y),
        )

        unavailable: set[Location] = set()
        for obj in chain(base, zombies):
            unavailable.add(obj.location)
        for enemy_base in enemy_bases:
            for loc in neighbours_with_diag(enemy_base.location):
                unavailable.add(loc)
        for zpot in zpots:
            for loc in neighbours(Location(zpot.x, zpot.y)):
                unavailable.add(loc)

        to_build: set[Location] = set()

        def add_neighbour(loc: Location):
            if loc not in unavailable:
                to_build.add(loc)

        for b in base:
            x, y = b.location.x, b.location.y
            add_neighbour(Location(x - 1, y))
            add_neighbour(Location(x + 1, y))
            add_neighbour(Location(x, y - 1))
            add_neighbour(Location(x, y + 1))

        sorted_by_proximity_to_center = sorted(
            to_build, key=lambda loc: center.distance(loc)
        )
        available = sorted_by_proximity_to_center[:limit]

        new_head = None
        base_locations: set[Location] = set(map(lambda b: b.location, base))
        if center in base_locations or center in available:
            new_head = center

        return available, new_head
