import json
from pathlib import Path

from model.state import PassedRound

from logger import logger as globlog


logger = globlog.getChild("storage")


def load(path: Path) -> list[PassedRound]:
    filenames = []
    for file in path.iterdir():
        if file.name.endswith(".round.json"):
            filenames.append(file.name)

    filenames = sorted(filenames)
    rounds = []
    for filename in filenames:
        with open(path / filename) as f:
            data = json.load(f)
        round = PassedRound.from_json(data)
        rounds.append(round)
    return rounds


class RoundStorage:
    def __init__(self, path: Path):
        path.mkdir(parents=True, exist_ok=True)
        self.path = path
        self._rounds = load(path)

    def get_stored(self) -> list[PassedRound]:
        return self._rounds

    def add(self, round: PassedRound):
        filename = f"{len(self._rounds)}.round.json"
        with open(self.path / filename, "w") as f:
            json.dump(round.to_json(), f, indent=2)
        self._rounds.append(round)
