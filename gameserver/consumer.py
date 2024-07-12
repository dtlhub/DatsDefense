import logging
import requests
from dataclasses import dataclass
from datetime import timedelta

from .models import Move, State


@dataclass
class Config:
    api_url: str
    token: str
    round_tick: timedelta


class ApiConsumer:
    def __init__(self, logger: logging.Logger, config: Config):
        self.config = config
        self.logger = logger

        self.s = requests.Session()
        self.s.headers["X-Auth-Token"] = self.config.token
        self.s.hooks["response"].append(self.check_response)

    def url(self, path: str) -> str:
        return self.config.api_url + path + "/"

    def check_response(self, response: requests.Response, *args, **kwargs):
        request = response.request
        self.logger.debug(
            f"Request: {request.method = } {request.url = } {request.body = }"
        )
        self.logger.debug(f"Response: {response.status_code = } {response.text = }")

        if response.status_code != 200:
            raise ValueError(
                f"Failed to {request.method} {request.url}: {response.status_code = }, {response.text = }"
            )

    def make_move(self, move: Move):
        response = self.s.post(
            self.url("/play/zombidef/command"),
            json=move.to_json(),
        )
        self.check_response(response, "make move")
        return response.json()

    def play(self):
        response = self.s.put(self.url("/play/zombidef/participate"))
        return response.json()

    def get_units_around(self):
        response = self.s.get(self.url("/play/zombidef/units"))
        return response.json()

    def get_world_around(self):
        response = self.s.get(self.url("/play/zombidef/world"))
        return response.json()

    def get_game_rounds(self):
        response = self.s.get(self.url("/rounds/zombidef"))
        return response.json()

    def run(self): ...
