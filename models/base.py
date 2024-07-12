from .point  import Point
from .zombie import Zombie


class BasePoint(Point):
    def __init__(self, attack, health, id, is_head, last_attack, range, x, y):
        self.attack = attack
        self.health = health
        self.id = id
        self.is_head = is_head
        self.last_attack = last_attack
        self.range = range
        self.x = x
        self.y = y


def base_points_from_json(base_point_data: dict) -> BasePoint:
    return BasePoint(
        base_point_data['attack'],
        base_point_data['health'],
        base_point_data['id'],
        base_point_data['isHead'],
        base_point_data['lastAttack'],
        base_point_data['range'],
        base_point_data['x'],
        base_point_data['y']
    )


class Base:
    def __init__(self, base_points: list[BasePoint]):
        self.base_points = base_points

    def attack_zombie(self, zombie: Zombie) -> list[BasePoint]:
        accumulated_damage = 0
        attackers = []
        for point in self.base_points:
            if point.distance(zombie) <= point.range:
                attackers.append(point)
                accumulated_damage += point.attack
            if accumulated_damage >= zombie.health:
                break
        
        return attackers


def base_from_json(base_data: list) -> Base:
     points = [base_points_from_json(i) for i in base_data]
     return Base(points)