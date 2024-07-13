import gameserver.consumer
import gameserver.storage
import gameserver.runner
import gameserver.strategies.idle
import gameserver.strategies.stupid_attack


HOST = "https://games-test.datsteam.dev"
HOST = "https://games.datsteam.dev"

TOKEN = "66843ff3b401c66843ff3b401f"


def main():
    api = gameserver.consumer.ApiConsumer(HOST, TOKEN)
    strategy = gameserver.strategies.stupid_attack.StupidAttackStrategy()

    runner = gameserver.runner.Runner(api, strategy)
    runner.start()
    runner.join()


if __name__ == "__main__":
    main()
