from dataclasses import dataclass
from typing_extensions import Self
from enum import Enum
from functools import cached_property
from collections import defaultdict


from . import (
    GetWorldResponse,
    GetUnitsResponse,
    GetRoundsResponse,
    Command,
    Location,
    ZpotType,
)


class LocationType(Enum):
    EMPTY = 0
    WALL = 1
    ZPOT = 2
    ZOMBIE = 3
    ENEMY = 4
    MY_BASE = 5


@dataclass
class RoundSnapshot:
    world: GetWorldResponse
    units: GetUnitsResponse
    rounds: GetRoundsResponse

    @cached_property
    def location_types(self) -> dict[Location, LocationType]:
        d = defaultdict(lambda: LocationType.EMPTY)
        for zpot in self.world.zpots:
            loc = Location(zpot.x, zpot.y)
            if zpot.type == ZpotType.WALL:
                d[loc] = LocationType.WALL
            elif zpot.type == ZpotType.DEFAULT:
                d[loc] = LocationType.ZPOT
        for enemy_base in self.units.enemy_bases:
            d[enemy_base.location] = LocationType.ENEMY
        for base in self.units.base:
            d[base.location] = LocationType.MY_BASE
        for zomb in self.units.zombies:
            d[zomb.location] = LocationType.ZOMBIE
        return d

    @classmethod
    def from_json(cls, json) -> Self:
        return cls(
            world=GetWorldResponse.from_json(json["world"]),
            units=GetUnitsResponse.from_json(json["units"]),
            rounds=GetRoundsResponse.from_json(json["rounds"]),
        )

    def to_json(self):
        return {
            "world": self.world.to_json(),
            "units": self.units.to_json(),
            "rounds": self.rounds.to_json(),
        }


@dataclass
class PassedRound:
    game: RoundSnapshot
    command: Command

    @classmethod
    def from_json(cls, json) -> Self:
        return cls(
            game=RoundSnapshot.from_json(json["game"]),
            command=Command.from_json(json["command"]),
        )

    def to_json(self):
        return {
            "game": self.game.to_json(),
            "command": self.command.to_json(),
        }


@dataclass
class State:
    history: list[PassedRound]
    current_round: RoundSnapshot
