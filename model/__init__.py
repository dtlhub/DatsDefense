from dataclasses import dataclass
from typing_extensions import Self, cast


@dataclass
class Location:
    x: int
    y: int

    @classmethod
    def from_json(cls, json) -> Self:
        return cls(
            x=cast(int, json.get("x")),
            y=cast(int, json.get("y")),
        )

    def to_json(self):
        return {
            "x": self.x,
            "y": self.y,
        }


@dataclass
class AttackCommand:
    block_id: str
    target: Location

    @classmethod
    def from_json(cls, json) -> Self:
        return cls(
            block_id=cast(str, json.get("blockId")),
            target=Location.from_json(json.get("target")),
        )

    def to_json(self):
        return {
            "block_id": self.block_id,
            "target": self.target.to_json(),
        }


@dataclass
class Command:
    attack: list[AttackCommand]
    build: list[Location]
    move_base: Location | None

    @classmethod
    def from_json(cls, json) -> Self:
        move_base = None
        if (obj := json.get("moveBase")) is not None:
            move_base = Location.from_json(obj)

        return cls(
            attack=[AttackCommand.from_json(obj) for obj in json.get("attack")],
            build=[Location.from_json(obj) for obj in json.get("obj")],
            move_base=move_base,
        )

    def to_json(self):
        json = {
            "attack": [a.to_json() for a in self.attack],
            "build": [b.to_json() for b in self.build],
        }
        if self.move_base is not None:
            json["moveBase"] = self.move_base.to_json()
        return json


@dataclass
class CommandResponse:
    accepted: Command
    errors: list[str]

    @classmethod
    def from_json(cls, json) -> Self:
        return cls(
            accepted=Command.from_json(cast(dict, json["acceptedCommands"])),
            errors=cast(list[str], json["errors"]),
        )


@dataclass
class PlayResponse:
    starts_in_sec: int

    @classmethod
    def from_json(cls, json) -> Self:
        return cls(starts_in_sec=cast(int, json["startsInSec"]))


@dataclass
class BaseLocation:
    id: str
    attack: int
    health: int
    is_head: bool
    range: int
    last_attack: Location
    location: Location


@dataclass
class GetUnitsResponse:
    base: list[Location]
