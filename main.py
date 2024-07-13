import gameserver.consumer
import gameserver.storage
import gameserver.runner
import gameserver.strategies.idle


TEST_HOST = "https://games-test.datsteam.dev"
PRODUCTION_HOST = "https://games.datsteam.dev"

TOKEN = "66843ff3b401c66843ff3b401f"


def main():
    api = gameserver.consumer.ApiConsumer(TEST_HOST, TOKEN)
    strategy = gameserver.strategies.idle.IdleStrategy()

    runner = gameserver.runner.Runner(api, strategy)
    runner.start()
    runner.join()


if __name__ == "__main__":
    main()
