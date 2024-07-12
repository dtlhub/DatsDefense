import logging
from datetime import timedelta
from time import sleep
import gameserver.consumer

basedir = "./samples/%s"


CONFIG = gameserver.consumer.Config(
    api_url="https://games-test.datsteam.dev",
    token="66843ff3b401c66843ff3b401f",
    round_tick=timedelta(seconds=2),
    round_storage="./samples"
)

def get_all(pizda : gameserver.consumer.ApiConsumer):
    out = {
        #"rounds" : pizda.get_game_rounds(),
        "units" : pizda.get_units_around(),
        "world" : pizda.get_world_around()
    }


#10001
#10101
#10001
K = 2
A = 3
BASE = [[0,0],[0,0]]

#from itertools import 

from model import GetUnitsResponse, Command

def main():
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("api_consumer")
    consumer = gameserver.consumer.ApiConsumer(logger, CONFIG)
    start = False
    while not start:
        sleep(2)
        rounds = consumer.get_game_rounds().rounds
        for r in rounds:
            if r.status not in ['not started', 'ended', 'active']:
                start = True
                print("PIZDA123",r)
                break
    print(consumer.get_game_rounds())
    consumer.play()
    start = False
    while not start:
        try: 
            move = {
                "build" : [1,1],
                "attack": [],
                "moveBase": [1,1]
            }
            a = get_all(consumer)
            move['attack'] = GetUnitsResponse.from_json(a['units']).attack()
            consumer.make_move(Command.from_json(move))
            #to_pay = K + A
            #if a['units']['player']['gold'] > to_pay + 3:
            sleep(a['units'].turnEndsInMs / 1000)    
           # else:
        except:
            break


if __name__ == "__main__":
    main()
    exit(0)
