from pathlib import Path

import gameserver.consumer
import gameserver.storage
import gameserver.runner
import gameserver.strategies.idle


TEST_HOST = "https://games-test.datsteam.dev"
PRODUCTION_HOST = "https://games.datsteam.dev"

TOKEN = "66843ff3b401c66843ff3b401f"

STORAGE = Path.cwd() / "storage"


def main():
    api = gameserver.consumer.ApiConsumer(PRODUCTION_HOST, TOKEN)

    response = api.play()
    print(f'{response.starts_in_sec = }')


if __name__ == "__main__":
    main()
