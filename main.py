import logging
from datetime import timedelta

import gameserver.consumer


CONFIG = gameserver.consumer.Config(
    api_url="https://games-test.datsteam.dev",
    token="66843ff3b401c66843ff3b401f",
    round_tick=timedelta(seconds=2),
)


def main():
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("api_consumer")

    consumer = gameserver.consumer.ApiConsumer(logger, CONFIG)
    print(consumer.get_game_rounds())


if __name__ == "__main__":
    main()
