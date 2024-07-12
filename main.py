import logging
from pathlib import Path

import gameserver.consumer
import gameserver.storage
import gameserver.runner


TEST_HOST = "https://games-test.datsteam.dev"
PRODUCTION_HOST = "https://games.datsteam.dev"

TOKEN = "66843ff3b401c66843ff3b401f"

STORAGE = Path.cwd() / "storage"

logging.basicConfig(level=logging.INFO)


def main():
    api = gameserver.consumer.ApiConsumer(TEST_HOST, TOKEN)
    storage = gameserver.storage.RoundStorage(STORAGE)
    runner = gameserver.runner.Runner()

    runner.run()


if __name__ == "__main__":
    main()
