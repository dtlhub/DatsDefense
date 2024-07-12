from dataclasses import dataclass


@dataclass
class State: ...


@dataclass
class Move:
    def to_json(self): ...
