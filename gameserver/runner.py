import time
import logging
import datetime
import traceback
import threading
from typing import cast
from pathlib import Path

from model import Command
from model.state import RoundSnapshot, State, PassedRound
from .consumer import ApiConsumer
from .storage import RoundStorage
from .strategy import Strategy
from .strategies import ALL_STRATEGIES


logger = logging.getLogger("runner")


class Runner(threading.Thread):
    def __init__(
        self,
        api: ApiConsumer,
        initial_strategy: Strategy,
    ):
        super().__init__()
        self._api = api
        self._cached_round: RoundSnapshot | None = None
        self._cache_lock = threading.Lock()

        self._strategy = initial_strategy
        self._next_round_strategy_name: str | None = None
        self._strategy_lock = threading.Lock()

        self._command: Command | None = None
        self._command_lock = threading.Lock()

    @property
    def current_strategy(self):
        with self._strategy_lock:
            return self._strategy_lock

    @property
    def next_round_strategy(self):
        with self._strategy_lock:
            return self._next_round_strategy_name

    @next_round_strategy.setter
    def next_round_strategy(self, new: str):
        with self._strategy_lock:
            self._next_round_strategy_name = new

    def get_round_cached(self) -> RoundSnapshot:
        with self._cache_lock:
            if self._cached_round is not None:
                return self._cached_round

            self._cached_round = RoundSnapshot(
                world=self._api.get_world_around(),
                units=self._api.get_units_around(),
                rounds=self._api.get_game_rounds(),
            )
            return self._cached_round

    def run_round(self, storage: RoundStorage) -> bool:
        with self._strategy_lock:
            if self._next_round_strategy_name is not None:
                self._strategy = ALL_STRATEGIES[self._next_round_strategy_name]

        with self._cache_lock:
            self._cached_round = None

        state = State(
            history=storage.get_stored(),
            current_round=self.get_round_cached(),
        )
        result = self._strategy.command(state)
        if isinstance(result, Command):
            command = result
        else:
            next_strategy, command = result
            with self._strategy_lock:
                if self.next_round_strategy is None:
                    self.next_round_strategy = cast(str, next_strategy)

        accepted_command = self._api.send_command(command)
        storage.add(
            PassedRound(
                game=self.get_round_cached(),
                command=accepted_command.accepted,
            )
        )
        return "you are dead" not in accepted_command.errors

    def play_until_dead(self, storage: RoundStorage):
        is_alive = True
        while is_alive:
            try:
                is_alive = self.run_round(storage)
            except Exception as ex:
                logger.error(f"Failed to run iteration: {ex}")
                if "too many requests" in str(ex):
                    logger.warning("Encountered too many requests; going to sleep for 2 seconds")
                    time.sleep(2)
                    continue

                print(traceback.format_exc())
            else:
                current_round = self.get_round_cached()
                sleep_seconds = current_round.units.turn_ends_in_ms / 1000
                logger.debug(f"Sleeping for {sleep_seconds} seconds")
                time.sleep(sleep_seconds)

        logger.info("Player is dead, quitting round")

    def participate_in_round(self):
        round_started = False
        while not round_started:
            try:
                response = self._api.play()
                logger.info(f"{response.starts_in_sec = }")
                time.sleep(1)
            except Exception:
                round_started = True

        rounds = self._api.get_game_rounds()
        now = rounds.now
        index = -1
        for i, round in enumerate(rounds.rounds):
            if round.startAt <= now and now < round.endAt:
                index = i
        if index == -1:
            raise ValueError("Failed to calculate current round")
        current_round = rounds.rounds[index]
        storage = RoundStorage(Path.cwd() / "storage" / current_round.name)

        logger.info(f"Playing round {current_round.name}")
        self.play_until_dead(storage)

        rounds = self._api.get_game_rounds()
        now = rounds.now
        closest_in_future_seconds_from_now = datetime.timedelta(days=999)
        index = -1
        for i, round in enumerate(rounds.rounds):
            if round.startAt < now:
                continue
            d = round.startAt - now
            if d < closest_in_future_seconds_from_now:
                closest_in_future_seconds_from_now = d
                index = i
        if index == -1:
            raise ValueError("Failed to calculate next round")
        closest = rounds.rounds[index]
        to_sleep_seconds = (closest.startAt - now).total_seconds()

        logger.info(
            f"Closest round is {closest.name} which starts at {closest.startAt.isoformat()}; now is {now.isoformat()}"
        )
        logger.info(f"Going to sleep for {to_sleep_seconds} seconds")
        time.sleep(to_sleep_seconds)

    def run(self):
        while True:
            self.participate_in_round()
