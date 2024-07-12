import datetime
from dataclasses import dataclass
from typing_extensions import Self
from enum import Enum
from math import sqrt


@dataclass
class Location:
    x: int
    y: int

    @classmethod
    def from_json(cls, json) -> Self:
        return cls(
            x=json.get("x"),
            y=json.get("y"),
        )

    def to_json(self):
        return {
            "x": self.x,
            "y": self.y,
        }
    
    def distance(self, other: Self) -> float:
        return sqrt(
            (self.x**2 - other.x**2) + (self.y**2 - other.y**2)
        )


@dataclass
class AttackCommand:
    block_id: str
    target: Location

    @classmethod
    def from_json(cls, json) -> Self:
        return cls(
            block_id=json.get("blockId"),
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
            accepted=Command.from_json(json["acceptedCommands"]),
            errors=json["errors"],
        )


@dataclass
class PlayResponse:
    starts_in_sec: int

    @classmethod
    def from_json(cls, json) -> Self:
        return cls(
            starts_in_sec=json["startsInSec"],
        )


@dataclass
class MyBaseLocation:
    id: str
    attack: int
    health: int
    is_head: bool
    range: int
    last_attack: Location
    location: Location

    @classmethod
    def from_json(cls, json) -> Self:
        return cls(
            id=json["id"],
            attack=json["attack"],
            health=json["health"],
            is_head=json["isHead"],
            range=json["range"],
            last_attack=Location.from_json(json["lastAttack"]),
            location=Location.from_json(json),
        )


@dataclass
class EnemyBaseLocation:
    name: str
    attack: int
    health: int
    is_head: bool
    range: int
    last_attack: Location
    location: Location

    @classmethod
    def from_json(cls, json) -> Self:
        return cls(
            name=json["str"],
            attack=json["attack"],
            health=json["health"],
            is_head=json["isHead"],
            range=json["range"],
            last_attack=Location.from_json(json["lastAttack"]),
            location=Location.from_json(json),
        )


@dataclass
class Player:
    enemy_block_kills: int
    game_ended_at: datetime.datetime
    gold: int
    name: str
    points: int
    zombie_kills: int

    @classmethod
    def from_json(cls, json) -> Self:
        return cls(
            enemy_block_kills=json["enemyBlockKills"],
            game_ended_at=datetime.datetime.fromisoformat(json["gameEndedAt"]),
            gold=json["gold"],
            name=json["name"],
            points=json["points"],
            zombie_kills=json["zombieKills"],
        )


class Direction(Enum):
    UNKNOWN = 0
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

    @staticmethod
    def from_typestr(type: str) -> "Direction":
        match type:
            case "up":
                return Direction.UP
            case "right":
                return Direction.RIGHT
            case "down":
                return Direction.DOWN
            case "left":
                return Direction.LEFT
            case _:
                return Direction.UNKNOWN


class ZombieType(Enum):
    UNKNOWN = 0
    NORMAL = 1
    FAST = 2
    BOMBER = 3
    LINER = 4
    JUGGERNAUT = 5
    CHAOS_KNIGHT = 6

    @staticmethod
    def from_typestr(type: str) -> "ZombieType":
        match type:
            case "normal":
                return ZombieType.NORMAL
            case "fast":
                return ZombieType.FAST
            case "bomber":
                return ZombieType.BOMBER
            case "liner":
                return ZombieType.LINER
            case "juggernaut":
                return ZombieType.JUGGERNAUT
            case "chaos_knight":
                return ZombieType.CHAOS_KNIGHT
            case _:
                return ZombieType.UNKNOWN


@dataclass
class Zombie:
    attack: int
    direction: Direction
    health: int
    id: str
    speed: int
    type: ZombieType
    wait_turns: int
    x: int
    y: int

    @classmethod
    def from_json(cls, json) -> Self:
        return cls(
            attack=json["attack"],
            direction=Direction.from_typestr(json["direction"]),
            health=json["health"],
            id=json["id"],
            speed=json["speed"],
            type=ZombieType.from_typestr(json["type"]),
            wait_turns=json["waitTurns"],
            x=json["x"],
            y=json["y"],
        )


@dataclass
class GetUnitsResponse:
    base: list[MyBaseLocation]
    enemy_bases: list[EnemyBaseLocation]
    player: Player
    realm_name: str
    turn: int
    turn_ends_in_ms: int
    zombies: list[Zombie]

    @classmethod
    def from_json(cls, json) -> Self:
        return cls(
            base=[MyBaseLocation.from_json(obj) for obj in json["base"]],
            enemy_bases=[
                EnemyBaseLocation.from_json(obj) for obj in json["enemyBlocks"]
            ],
            player=Player.from_json(json["player"]),
            realm_name=json["realmName"],
            turn=json["turn"],
            turn_ends_in_ms=json["turnEndsInMs"],
            zombies=[Zombie.from_json(obj) for obj in json["zombies"]],
        )
    
    def attack(self) -> list[AttackCommand]:
        accumulated_damage = 0
        attackers: list[MyBaseLocation] = []
        attacks = []
        for zombie in self.zombies:
            attackers = []
            for point in self.base:
                if point.location.distance(zombie.location) <= point.range:
                    attackers.append(point)
                    accumulated_damage += point.attack
                if accumulated_damage >= zombie.health:
                    break
            else:
                # Если не брейкнулся изза того что аккумулированыный урон больше хп зомби
                continue
            for attacker in attackers:
                attacks.append(AttackCommand(attacker.id, zombie.location))
            
                
        return attackers


class ZpotType(Enum):
    UNKNOWN = 0
    DEFAULT = 1
    WALL = 2

    @staticmethod
    def from_typestr(typestr: str) -> "ZpotType":
        match typestr:
            case "default":
                return ZpotType.DEFAULT
            case "wall":
                return ZpotType.WALL
            case _:
                return ZpotType.UNKNOWN


@dataclass
class Zpot:
    x: int
    y: int
    type: ZpotType

    @classmethod
    def from_json(cls, json) -> Self:
        return cls(
            x=json["x"],
            y=json["y"],
            type=ZpotType.from_typestr(json["type"]),
        )


@dataclass
class GetWorldResponse:
    realm_name: str
    zpots: list[Zpot]

    @classmethod
    def from_json(cls, json) -> Self:
        return cls(
            realm_name=json["realmName"],
            zpots=[Zpot.from_json(obj) for obj in json["zpots"]],
        )


@dataclass
class GameRound:
    duration: int
    endAt: datetime.datetime
    name: str
    repeat: int | None
    startAt: datetime.datetime
    status: str

    @classmethod
    def from_json(cls, json) -> Self:
        return cls(
            duration=json["duration"],
            endAt=datetime.datetime.fromisoformat(json["endAt"].replace('Z', '+00:00')),
            name=json["name"],
            repeat=json.get("repeat"),
            startAt=datetime.datetime.fromisoformat(json["startAt"].replace('Z', '+00:00')),
            status=json["status"],
        )


@dataclass
class GetRoundsResponse:
    game_name: str
    now: str
    rounds: list[GameRound]

    @classmethod
    def from_json(cls, json) -> Self:
        return cls(
            game_name=json["gameName"],
            now=json["now"],
            rounds=[GameRound.from_json(obj) for obj in json["rounds"]],
        )
