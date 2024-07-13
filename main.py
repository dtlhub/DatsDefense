import logging
from pathlib import Path

import gameserver.consumer
import gameserver.storage
import gameserver.runner
import gameserver.strategies.idle

import visualisation.app


TEST_HOST = "https://games-test.datsteam.dev"
PRODUCTION_HOST = "https://games.datsteam.dev"

TOKEN = "66843ff3b401c66843ff3b401f"

STORAGE = Path.cwd() / "storage" / "test-day2-4"

logging.basicConfig(level=logging.DEBUG)


def main():
    STORAGE.mkdir(parents=True, exist_ok=True)

    api = gameserver.consumer.ApiConsumer(TEST_HOST, TOKEN)
    storage = gameserver.storage.RoundStorage(STORAGE)
    strategy = gameserver.strategies.idle.IdleStrategy()

    runner = gameserver.runner.Runner(api, storage, strategy)
    runner.start()

    visualise = visualisation.app.create_app(storage)
    visualise.run("0.0.0.0", 5000, debug=False)
    runner.join()


if __name__ == "__main__":
    main()
