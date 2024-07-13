from dataclasses import dataclass
from typing_extensions import Self

from . import GetWorldResponse, GetUnitsResponse, Command


@dataclass
class RoundSnapshot:
    world: GetWorldResponse
    units: GetUnitsResponse

    @classmethod
    def from_json(cls, json) -> Self:
        return cls(
            world=GetWorldResponse.from_json(json["world"]),
            units=GetUnitsResponse.from_json(json["units"]),
        )

    def to_json(self):
        return {
            "world": self.world.to_json(),
            "units": self.units.to_json(),
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
