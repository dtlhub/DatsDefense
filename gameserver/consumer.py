import logging
import requests

import model


logger = logging.getLogger("api")


class ApiConsumer:
    def __init__(self, api_url: str, token: str):
        self.api_url = api_url
        self.token = token

        self.s = requests.Session()
        self.s.headers["X-Auth-Token"] = self.token
        self.s.hooks["response"].append(self.check_response)

    def url(self, path: str) -> str:
        return self.api_url + path + "/"

    def check_response(self, response: requests.Response, *args, **kwargs):
        request = response.request
        logger.debug(f"Request: {request.method = } {request.url = } {request.body = }")
        logger.debug(f"Response: {response.status_code = } {response.text = }")

        if response.status_code != 200:
            raise ValueError(
                f"Failed to {request.method} {request.url}: {response.status_code = }, {response.text = }"
            )

    def send_command(self, command: model.Command) -> model.CommandResponse:
        response = self.s.post(
            self.url("/play/zombidef/command"),
            json=command.to_json(),
        )
        response = model.CommandResponse.from_json(response.json())
        for error in response.errors:
            logger.error(f"Command execution error: {error}")
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
