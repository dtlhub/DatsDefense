from dataclasses import dataclass
from . import GetWorldResponse, GetUnitsResponse, GetRoundsResponse, Command


@dataclass
class RoundSnapshot:
    world: GetWorldResponse
    units: GetUnitsResponse
    rounds: GetRoundsResponse


@dataclass
class PassedRound:
    game: RoundSnapshot
    command: Command | None


@dataclass
class State:
    history: list[PassedRound]
    current_round: RoundSnapshot
