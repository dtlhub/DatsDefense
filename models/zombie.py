from .point import Point
from typing_extensions import Self, cast


class Zombie(Point):
    def __init__(self, x, y, direction, id, health, speed, type, wait_turns, attack):
        self.x = x
        self.y = y
        self.direction = direction
        self.id = id
        self.health = health
        self.speed = speed
        self.type = type
        self.wait_turns = wait_turns
        self.attack = attack

    def get_affected_coordinates(self) -> list[(int, int)]:
        """че надо написать неебаться хуйню да со свитчами по типу
        """
        zombie_type = self.type
        direction = Zombie.direction_map(self.direction)
        match zombie_type:
            case 'normal':
                return [(self.x+direction[0], self.y+direction[1])]
            case 'fast':
                return [(self.x+2*direction[0], self.y+2*direction[1])]
            case 'bomber':
                delta = [-1, 0, 1]
                res = []
                for dx in delta:
                    for dy in delta:
                        res.append((self.x+direction[0]+dx, self.y+direction[1]+dy))
                return res
            case 'liner':
                return [(self.x+direction[0], self.y+direction[1]), (self.x+2*direction[0], self.y+2*direction[1])]
            case 'juggernaut':
                return [(self.x+direction[0], self.y+direction[1])]
            case 'chaos_knight':
                if direction[0]==0:
                    return [(self.x+1, self.y+3*direction[1]), (self.x-1, self.y+3*direction[1])]
                else:
                    return [(self.x+3*direction[0], self.y+1), (self.x+3*direction[0], self.y-1)] 


    # Возвращает кортеж с направлением где если первым параметром 1 значит наверх -1 значит вниз вторым параметром если 1 значит вправо иначе влево
    @staticmethod
    def direction_map(direction: str) -> tuple:
        match direction:
            case 'up':
                return (0, 1)
            case 'down':
                return (0, -1)
            case 'right':
                return (1, 0)
            case 'left':
                return (-1, 0)


    
    @classmethod
    def from_json(cls, zombie_data: dict) -> Self:
        return Zombie(
            zombie_data['x'],
            zombie_data['y'],
            zombie_data['direction'],
            zombie_data['id'],
            zombie_data['health'],
            zombie_data['speed'],
            zombie_data['type'],
            zombie_data['waitTurns'],
            zombie_data['attack']
        )
