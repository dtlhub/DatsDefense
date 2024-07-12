import logging
import requests
from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path

import model


@dataclass
class Config:
    api_url: str
    token: str
    round_tick: timedelta
    round_storage: Path


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

    def make_move(self, command: model.Command) -> model.CommandResponse:
        response = self.s.post(
            self.url("/play/zombidef/command"),
            json=command.to_json(),
        )
        response = model.CommandResponse.from_json(response.json())
        error = "\n\n".join(response.errors)
        if error != "":
            raise ValueError(error)
        return response

    def play(self) -> model.PlayResponse:
        response = self.s.put(self.url("/play/zombidef/participate"))
        return model.PlayResponse.from_json(response.json())

    def get_units_around(self) -> model.GetUnitsResponse:
        response = self.s.get(self.url("/play/zombidef/units"))
        return model.GetUnitsResponse.from_json(response.json())

    def get_world_around(self) -> model.GetWorldResponse:
        response = self.s.get(self.url("/play/zombidef/world"))
        return model.GetWorldResponse.from_json(response.json())

    def get_game_rounds(self) -> model.GetRoundsResponse:
        response = self.s.get(self.url("/rounds/zombidef"))
        return model.GetRoundsResponse.from_json(response.json())

    def run(self): ...
