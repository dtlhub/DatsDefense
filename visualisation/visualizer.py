import requests
from matplotlib import pyplot as plt
from model.state import PassedRound
from model import (
    MyBaseLocation, 
    Zombie, 
    ZombieType, 
    EnemyBaseLocation, 
    Zpot, 
    Location
)


URL = 'http://0.0.0.0:1234'


class RoundVisualizer:
    def __init__(self, round):
        self.world = round.game.world
        self.zombies = round.game.units.zombies
        self.enemies = round.game.units.enemies
        self.base = round.game.units.base
        self.fig, self.ax = plt.subplots()

    def __get_points(self, obj: list[Zombie] | list[EnemyBaseLocation] | list[MyBaseLocation]):
        plot_points_x = []
        plot_points_y = []
        for base_points in obj:
            plot_points_x.append(base_points.location.x)
            plot_points_y.append(base_points.location.y)
            
        pass

    def __add_base(self):
        points = self.__get_points(self.base)
        self.ax.scatter(points[0], points[1], marker='*', color='green')

    def __add_zombies(self):
        # types later
        colors = {
            Zombie.NORMAL: 'g',  # Green for Normal
            Zombie.FAST: 'b',  # Blue for Fast
            Zombie.BOMBER: 'o',  # Orange for Bomber
            Zombie.LINER: 'y',  # Yellow for Liner
            Zombie.JUGGERNAUT: 'm',  # Magenta for Juggernaut
            Zombie.CHAOS_KNIGHT: 'k'  # Black for Chaos Knight
        }
        for zombie in self.zombies:
            self.ax.scatter(
                zombie.location['x'],
                zombie.location['y'],
                color=colors.get(zombie.type, 'gray'),  # Default to gray if type not found
                marker='o', 
            )
        pass
    
    def __add_enemy(self):
        points = self.__get_points(self.base)
        self.ax.scatter(points[0], points[1], marker='*', color='red')

    def visualize(self):
        plt.show()



def visualize_state(passed_round_json):
    round = PassedRound.from_json(passed_round_json)
    world = round.game.world