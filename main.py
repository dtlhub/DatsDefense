import logging
import gameserver.consumer


TEST_HOST = "https://games-test.datsteam.dev"
PRODUCTION_HOST = "https://games.datsteam.dev"

CONFIG = gameserver.consumer.Config(
    api_url="https://games-test.datsteam.dev",
    token="66843ff3b401c66843ff3b401f",
)


def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("api_consumer")

    consumer = gameserver.consumer.ApiConsumer(
        logger=logger,
        config=CONFIG,
    )


if __name__ == "__main__":
    main()
