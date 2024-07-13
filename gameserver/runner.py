import time
import threading
from typing import cast

from model import Command
from model.state import RoundSnapshot, State, PassedRound
from .consumer import ApiConsumer
from .storage import RoundStorage
from .strategy import Strategy
from .strategies import ALL_STRATEGIES


class Runner(threading.Thread):
    def __init__(
        self,
        api: ApiConsumer,
        storage: RoundStorage,
        initial_strategy: Strategy,
    ):
        super().__init__()
        self._api = api
        self._cached_round: RoundSnapshot | None = None
        self._cache_lock = threading.Lock()

        self._storage = storage

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

    def run_round(self):
        with self._strategy_lock:
            if self._next_round_strategy_name is not None:
                self._strategy = ALL_STRATEGIES[self._next_round_strategy_name]

        with self._cache_lock:
            self._cache_round = None

        state = State(
            history=self._storage.get_stored(),
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
        self._api.send_command(command)

        self._storage.add(
            PassedRound(
                game=self.get_round_cached(),
                command=command,
            )
        )

    def run(self):
        while True:
            current_round = self.get_round_cached()
            time.sleep(current_round.units.turn_ends_in_ms / 1000)
            self.run_round()
