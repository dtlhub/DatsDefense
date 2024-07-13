import base64
import requests
import json
from io import BytesIO
from matplotlib import pyplot as plt
from model.state import PassedRound
from model import (
    MyBaseLocation,
    Zombie,
    ZombieType,
    EnemyBaseLocation,
    Zpot,
    ZpotType,
    Location
)


URL = 'http://0.0.0.0:1234'


class RoundVisualizer:
    def __init__(self, round):
        self.world = round.game.world
        self.zombies = round.game.units.zombies
        self.enemies = round.game.units.enemy_bases
        self.base = round.game.units.base
        self.fig, self.ax = plt.subplots()

    def __get_points(self, obj: list[Zombie] | list[EnemyBaseLocation] | list[MyBaseLocation]):
        plot_points_x = []
        plot_points_y = []
        for base_points in obj:
            plot_points_x.append(base_points.location.x)
            plot_points_y.append(base_points.location.y)

        return (plot_points_x, plot_points_y)

    def __add_base(self):
        points = self.__get_points(self.base)
        self.ax.scatter(points[0], points[1], label='Our base', marker='*', color='green', s=100)

    def __add_zombies(self):
        # types later
        colors = {
            ZombieType.NORMAL: 'g',  # Green for Normal
            ZombieType.FAST: 'b',  # Blue for Fast
            ZombieType.BOMBER: 'c',  # Cyan for Bomber
            ZombieType.LINER: 'y',  # Yellow for Liner
            ZombieType.JUGGERNAUT: 'm',  # Magenta for Juggernaut
            ZombieType.CHAOS_KNIGHT: 'k'  # Black for Chaos Knight
        }
        if self.zombies == []:
            return

        for zombie in self.zombies:
            zombie_new_coord = zombie.get_affected_coordinates()[0]
            print(zombie.location.x, zombie_new_coord[0], zombie.direction)
            self.ax.scatter(
                zombie.location.x,
                zombie.location.y,
                color=colors.get(zombie.type, 'gray'),  # Default to gray if type not found,
                marker='o',
            )

        for kek in colors.keys():
            self.ax.scatter(
                zombie.location.x,
                zombie.location.y,
                color=colors.get(kek, 'gray'),  # Default to gray if type not found,
                label=str(kek),
                marker='o',
                s=30
            )

    def __add_enemy(self):
        points = self.__get_points(self.enemies)
        self.ax.scatter(points[0], points[1], label='Enemy', marker='*', color='red', s=100)

    def __add_world(self):
        colors = {
            ZpotType.DEFAULT: 'r',  # Green for Normal
            ZpotType.WALL: 'gray',  # Blue for Fast
        }
        markers = {
            ZpotType.DEFAULT: '^',  # Green for Normal
            ZpotType.WALL: 's',  # Blue for Fast
        }
        for zpot in self.world.zpots:
            self.ax.scatter(
                zpot.x,
                zpot.y,
                color=colors.get(zpot.type, 'gray'),  # Default to gray if type not found,
                marker=markers.get(zpot.type, '.'),
            )

        for kek in colors.keys():
            self.ax.scatter(
                zpot.x,
                zpot.y,
                color=colors.get(kek, 'gray'),  # Default to gray if type not found,
                label=str(kek),
                marker=markers.get(kek, '.'),
            )

    def get_png_bytes(self):
        self.__add_base()
        self.__add_zombies()
        self.__add_enemy()
        self.__add_world()
        plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")

        tmpfile = BytesIO()
        self.fig.savefig(tmpfile, format='png')
        return tmpfile.getvalue()

    def visualize(self):
        self.__add_base()
        self.__add_zombies()
        self.__add_enemy()
        self.__add_world()
        plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")


        plt.show()


def visualize_state(passed_round_json):
    round = PassedRound.from_json(passed_round_json)
    vis = RoundVisualizer(round)
    vis.visualize()


def get_png_bytes(passed_round_json):
    round = PassedRound.from_json(passed_round_json)
    vis = RoundVisualizer(round)
    return vis.get_png_bytes()


if __name__ == "__main__":
    round = json.loads(open('./storage/test-day2-6/3.round.json', 'r').read())
    visualize_state(round)
    print('done')
