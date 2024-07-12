import os
from pathlib import Path

from model.state import PassedRound


def load(path: Path) -> list[PassedRound]:
    for file in path.iterdir():
        if file.name.endswith('.round.json'):
            ...


class RoundStorage:
    def __init__(self, path: Path):
        self.path = path
        self._rounds = []
        self._current_round = 0

    def get_stored(self) -> list[PassedRound]:
        return self._rounds

    def add(self, round: PassedRound):
        self._rounds.append(round)
