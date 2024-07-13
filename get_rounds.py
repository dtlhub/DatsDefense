from pathlib import Path

import gameserver.consumer
import gameserver.storage
import gameserver.runner
import gameserver.strategies.idle


HOST = "https://games-test.datsteam.dev"
HOST = "https://games.datsteam.dev"

TOKEN = "66843ff3b401c66843ff3b401f"

STORAGE = Path.cwd() / "storage"


def main():
    api = gameserver.consumer.ApiConsumer(HOST, TOKEN)

    rounds = api.get_game_rounds()
    print(rounds.game_name, rounds.now)
    for round in rounds.rounds:
        print(f"{round.to_json()}")


if __name__ == "__main__":
    main()
