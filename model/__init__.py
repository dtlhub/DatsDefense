import datetime
from dataclasses import dataclass
from typing_extensions import Self
from enum import Enum
from math import sqrt


def to_date(datestr: str) -> datetime.datetime:
    if "." in datestr:
        datestr = datestr.split(".")[0]
    datestr = datestr.replace("+00:00", "").replace("Z", "")
    date_format = "%Y-%m-%dT%H:%M:%S"
    return datetime.datetime.strptime(datestr, date_format)


@dataclass
class Location:
    x: int
    y: int

    @classmethod
    def from_json(cls, json) -> Self:
        return cls(
            x=json["x"],
            y=json["y"],
        )

    def to_json(self):
        return {
            "x": self.x,
            "y": self.y,
        }

    def distance(self, other: Self) -> float:
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


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
            attack=[AttackCommand.from_json(obj) for obj in (json.get("attack") or [])],
            build=[Location.from_json(obj) for obj in (json.get("obj") or [])],
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
            errors=json["errors"] or [],
        )

    def to_json(self):
        return {
            "acceptedCommands": self.accepted.to_json(),
            "errors": self.errors,
        }


@dataclass
class PlayResponse:
    starts_in_sec: int

    @classmethod
    def from_json(cls, json) -> Self:
        return cls(
            starts_in_sec=json["startsInSec"],
        )

    def to_json(self):
        return {
            "startsInSec": self.starts_in_sec,
        }


@dataclass
class MyBaseLocation:
    id: str
    attack: int
    health: int
    is_head: bool
    range: int
    last_attack: Location | None
    location: Location

    @classmethod
    def from_json(cls, json) -> Self:
        is_head = json.get("isHead")
        if is_head is None:
            is_head = json["attack"] == 40

        last_attack = None
        if (la := json.get("lastAttack")) is not None:
            last_attack = Location.from_json(la)

        return cls(
            id=json["id"],
            attack=json["attack"],
            health=json["health"],
            is_head=is_head,
            range=json["range"],
            last_attack=last_attack,
            location=Location.from_json(json),
        )

    def to_json(self):
        json = {
            "id": self.id,
            "attack": self.attack,
            "health": self.health,
            "isHead": self.is_head,
            "range": self.range,
            "x": self.location.x,
            "y": self.location.y,
        }
        if self.last_attack is not None:
            json["lastAttack"] = self.last_attack.to_json()
        return json


@dataclass
class EnemyBaseLocation:
    name: str
    attack: int
    health: int
    is_head: bool
    range: int
    last_attack: Location | None
    location: Location

    @classmethod
    def from_json(cls, json) -> Self:
        is_head = json.get("isHead")
        if is_head is None:
            is_head = json["attack"] == 40

        last_attack = None
        if (la := json.get("lastAttack")) is not None:
            last_attack = Location.from_json(la)

        return cls(
            name=json.get("name", "unknown"),
            attack=json["attack"],
            health=json["health"],
            is_head=is_head,
            range=json.get("range", 8 if is_head else 5),
            last_attack=last_attack,
            location=Location.from_json(json),
        )

    def to_json(self):
        json = {
            "name": self.name,
            "attack": self.attack,
            "health": self.health,
            "isHead": self.is_head,
            "range": self.range,
            "x": self.location.x,
            "y": self.location.y,
        }
        if self.last_attack is not None:
            json["lastAttack"] = self.last_attack.to_json()
        return json


@dataclass
class Player:
    enemy_block_kills: int
    game_ended_at: datetime.datetime | None
    gold: int
    name: str
    points: int
    zombie_kills: int

    @classmethod
    def from_json(cls, json) -> Self:
        game_end = None
        if json.get("gameEndedAt") is not None:
            game_end = to_date(json["gameEndedAt"])

        return cls(
            enemy_block_kills=json["enemyBlockKills"],
            game_ended_at=game_end,
            gold=json["gold"],
            name=json["name"],
            points=json["points"],
            zombie_kills=json["zombieKills"],
        )

    def to_json(self):
        json = {
            "enemyBlockKills": self.enemy_block_kills,
            "gold": self.gold,
            "name": self.name,
            "points": self.points,
            "zombieKills": self.zombie_kills,
        }
        if self.game_ended_at is not None:
            json["gameEndedAt"] = self.game_ended_at.isoformat()
        return json


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

    def to_coords(self) -> tuple[int, int]:
        match self:
            case Direction.UP:
                return (0, 1)
            case Direction.DOWN:
                return (0, -1)
            case Direction.RIGHT:
                return (1, 0)
            case Direction.LEFT:
                return (-1, 0)
            case _:
                return (0, 0)


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
    location: Location

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
            location=Location.from_json(json),
        )

    def to_json(self):
        return {
            "attack": self.attack,
            "direction": self.direction.name.lower(),
            "health": self.health,
            "id": self.id,
            "speed": self.speed,
            "type": self.type.name.lower(),
            "waitTurns": self.wait_turns,
            "x": self.location.x,
            "y": self.location.y,
        }

    @staticmethod
    def direction_map(direction: Direction) -> tuple:
        match direction:
            case Direction.UP:
                return (0, 1)
            case Direction.DOWN:
                return (0, -1)
            case Direction.RIGHT:
                return (1, 0)
            case Direction.LEFT:
                return (-1, 0)


    def get_affected_coordinates(self) -> list[(int, int)]:
        """че надо написать неебаться хуйню да со свитчами по типу
        """
        zombie_type = self.type
        direction = Zombie.direction_map(self.direction)
        return [(self.location.x + direction[0] * self.speed, self.location.y + direction[1] * self.speed)]


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
            base=[MyBaseLocation.from_json(obj) for obj in (json["base"] or [])],
            enemy_bases=[
                EnemyBaseLocation.from_json(obj) for obj in (json["enemyBlocks"] or [])
            ],
            player=Player.from_json(json["player"]),
            realm_name=json["realmName"],
            turn=json["turn"],
            turn_ends_in_ms=json["turnEndsInMs"],
            zombies=[Zombie.from_json(obj) for obj in (json["zombies"] or [])],
        )

    def to_json(self):
        return {
            "base": [base.to_json() for base in self.base],
            "enemyBlocks": [enemy_base.to_json() for enemy_base in self.enemy_bases],
            "player": self.player.to_json(),
            "realmName": self.realm_name,
            "turn": self.turn,
            "turnEndsInMs": self.turn_ends_in_ms,
            "zombies": [zombie.to_json() for zombie in self.zombies],
        }

    def attack(self) -> list[AttackCommand]:
        attackers: list[MyBaseLocation] = []
        used_attackers = []
        attacks = []
        for zombie in self.zombies:
            accumulated_damage = 0
            attackers = []
            for point in self.base:
                if point in used_attackers:
                    continue

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
                used_attackers.append(attacker)

        return attacks


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

    def to_json(self):
        return {
            "x": self.x,
            "y": self.y,
            "type": self.type.name.lower(),
        }


@dataclass
class GetWorldResponse:
    realm_name: str
    zpots: list[Zpot]

    @classmethod
    def from_json(cls, json) -> Self:
        return cls(
            realm_name=json["realmName"],
            zpots=[Zpot.from_json(obj) for obj in (json["zpots"] or [])],
        )

    def to_json(self):
        return {
            "realmName": self.realm_name,
            "zpots": [zpot.to_json() for zpot in self.zpots],
        }


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
            endAt=to_date(json["endAt"]),
            name=json["name"],
            repeat=json.get("repeat"),
            startAt=to_date(json["startAt"]),
            status=json["status"],
        )

    def to_json(self):
        return {
            "duration": self.duration,
            "endAt": self.endAt.isoformat(),
            "name": self.name,
            "repeat": self.repeat,
            "startAt": self.startAt.isoformat(),
            "status": self.status,
        }


@dataclass
class GetRoundsResponse:
    game_name: str
    now: datetime.datetime
    rounds: list[GameRound]

    @classmethod
    def from_json(cls, json) -> Self:
        return cls(
            game_name=json["gameName"],
            now=to_date(json["now"]),
            rounds=[GameRound.from_json(obj) for obj in (json["rounds"] or [])],
        )

    def to_json(self):
        return {
            "gameName": self.game_name,
            "now": self.now.isoformat(),
            "rounds": [round.to_json() for round in self.rounds],
        }
