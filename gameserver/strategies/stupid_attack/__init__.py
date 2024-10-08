from collections import defaultdict, deque

from gameserver.strategy import Strategy

from model import Command, Location, ZombieType, Direction, MyBaseLocation
from model.state import State, LocationType
from itertools import chain, count
from typing import Generator

from .coefs import Preset


def neighbours(loc: Location) -> Generator[Location, None, None]:
    for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
        yield Location(loc.x + dx, loc.y + dy)


def neighbours_with_diag(loc: Location) -> Generator[Location, None, None]:
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


def direction_generator(
    loc: Location, dir: Direction, amount: int | None = None
) -> Generator[Location, None, None]:
    dx, dy = {
        Direction.UNKNOWN: (0, 0),
        Direction.UP: (0, -1),
        Direction.DOWN: (0, 1),
        Direction.LEFT: (-1, 0),
        Direction.RIGHT: (1, 0),
    }[dir]
    gen = count if amount is None else lambda: range(amount)
    for d in gen():
        yield Location(loc.x + dx * d, loc.y + dy * d)


def get_attractiveness(
    state: State,
    start: Location,
    explore_radius: int,
    preset: Preset = Preset(),
) -> float:
    seen: set[Location] = set()
    q = deque()
    q.append(start)
    seen.add(start)

    d: dict[LocationType, int] = defaultdict(int)
    while len(q) > 0:
        loc = q.popleft()

        d[state.current_round.location_types[loc]] += 1

        for n in neighbours(loc):
            if n not in seen and start.distance(n) <= explore_radius:
                q.append(n)
                seen.add(n)

    return preset.get_coef(d)


class StupidAttackStrategy(Strategy):
    @staticmethod
    def name() -> str:
        return "stupid_attack"

    @staticmethod
    def command(state: State) -> Command:
        attacks = state.current_round.units.attack(
            StupidAttackStrategy.head_connected_blocks(state),
            prioritize_enemies=False,
        )

        # if len(state.history) < 100:
        #     build = StupidAttackStrategy.build_palka(state)
        # else:
        build = StupidAttackStrategy.build_circle(state)

        new_center = StupidAttackStrategy.calculate_head_location(state, build)

        return Command(
            attack=attacks,
            build=build,
            move_base=new_center,
        )

    @staticmethod
    def build_palka(state: State) -> list[Location]:
        direction = Direction.UP
        center = state.current_round.units.base_head
        assert center is not None
        return list(direction_generator(center.location, direction, amount=20))

    @staticmethod
    def build_circle(state: State) -> list[Location]:
        xs: list[int] = []
        ys: list[int] = []
        limit = state.current_round.units.player.gold

        base = state.current_round.units.base
        zombies = state.current_round.units.zombies
        zpots = state.current_round.world.zpots
        enemy_bases = state.current_round.units.enemy_bases

        if len(base) == 0:
            return []

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

        def calculate_weight(loc: Location) -> float:
            dist = center.distance(loc)
            # atc = get_attractiveness(
            #     state,
            #     loc,
            #     explore_radius=3,
            # #     preset=Preset(
            # #         wall=0.5,
            # #         zpot=0.5,
            # #         zombie=5.0,
            # #         enemy=0,
            # #         empty=1.0,
            # #         my_base=1.0,
            # #     ),
            # )
            return dist

        sorted_by_proximity_to_center = sorted(
            to_build,
            key=calculate_weight,
        )
        will_be_built = sorted_by_proximity_to_center[:limit]
        return will_be_built

    @staticmethod
    def calculate_head_location(
        state: State, will_be_built: list[Location]
    ) -> Location | None:
        base_cells = set(
            map(lambda x: x.location, state.current_round.units.base)
        ) | set(will_be_built)

        in_target_of_liner: set[Location] = set()
        for zomb in state.current_round.units.zombies:
            if zomb.type == ZombieType.LINER:
                first_base_cell = None
                for loc in direction_generator(zomb.location, zomb.direction, amount=3):
                    if loc in base_cells:
                        first_base_cell = loc
                        break
                if first_base_cell is not None:
                    for loc in direction_generator(first_base_cell, zomb.direction):
                        if loc not in base_cells:
                            break
                        in_target_of_liner.add(loc)

        dist: dict[Location | None, int] = {}
        q: deque[Location] = deque()

        for b in base_cells:
            if any(n not in base_cells for n in neighbours(b)):
                q.append(b)
                dist[b] = 1

        while len(q) > 0:
            loc = q.popleft()
            for n in neighbours(loc):
                if n not in dist and n in base_cells:
                    q.append(n)
                    dist[n] = dist[loc] + 1

        dist[None] = -1
        max_loc = None
        for loc in dist.keys():
            if loc in in_target_of_liner:
                continue

            if dist[loc] > dist[max_loc]:
                max_loc = loc
        return max_loc

    @staticmethod
    def head_connected_blocks(state: State) -> set[MyBaseLocation]:
        head = state.current_round.units.base_head
        if head is None:
            return set()

        loc_to_mbloc = {b.location: b for b in state.current_round.units.base}

        base_cells = set(map(lambda x: x.location, state.current_round.units.base))
        used: set[Location] = {head.location}
        q = deque()
        q.append(head.location)
        while len(q) > 0:
            loc = q.popleft()
            for n in neighbours(loc):
                if n not in used and n in base_cells:
                    q.append(n)
                    used.add(n)
        return {loc_to_mbloc[loc] for loc in used}
