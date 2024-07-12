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

    @classmethod
    def initialize(cls, round: RoundSnapshot, history: list[PassedRound] | None = None):
        if history is None:
            history = []
        return cls(
            current_round=round,
            history=history,
        )

    def record_command(self, command: Command):
        if getattr(self, "command") is not None:
            raise ValueError("Tried to record command twice in a row")
        self.command = command

    def record_round_snapshot(self, snapshot: RoundSnapshot):
        command = getattr(self, "command")
        if command is None:
            raise ValueError("Tried to record round snapshot twice in a row")

        self.history.append(
            PassedRound(
                game=self.current_round,
                command=command,
            )
        )
        self.current_round = snapshot
        self.command = None
