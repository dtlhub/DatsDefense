from dataclasses import dataclass
from datetime import timedelta


@dataclass
class Config:
    api_url: str
    token: str
    round_tick: timedelta


class ApiConsumer:
    def __init__(self, config: Config):
        self.config = config

    def run(self): ...
