from .point  import Point
from .zombie import Zombie
from .enemy import Enemy
from typing_extensions import Self, cast


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

    @classmethod
    def from_json(cls, base_point_data) -> Self:
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

    def attack(self, zombie: Zombie | Enemy) -> list[BasePoint]:
        accumulated_damage = 0
        attackers = []
        for point in self.base_points:
            if point.distance(zombie) <= point.range:
                attackers.append(point)
                accumulated_damage += point.attack
            if accumulated_damage >= zombie.health:
                break
        
        return attackers
    
    @classmethod
    def from_json(cls, base_data) -> Self:
        points = [BasePoint.from_json(i) for i in base_data]
        return Base(points)