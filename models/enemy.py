from .point  import Point
from typing_extensions import Self, cast


class EnemyPoint(Point):
    def __init__(self, attack, health, is_head, last_attack, name, x, y):
        self.attack = attack
        self.health = health
        self.id = id
        self.is_head = is_head
        self.last_attack = last_attack
        self.name = name
        self.x = x
        self.y = y

    @classmethod
    def from_json(cls, enemy_data: dict) -> Self:
        return EnemyPoint(
            enemy_data['attack'],
            enemy_data['health'],
            enemy_data['isHead'],
            enemy_data['lastAttack'],
            enemy_data['name'],
            enemy_data['x'],
            enemy_data['y']
        )


class Enemy:
    def __init__(self, enemy_points: list[EnemyPoint]):
        self.enemy_points = enemy_points

    @classmethod
    def from_json(enemy_data: list) -> Self:
        points = [EnemyPoint.from_json(i) for i in enemy_data]
        return Enemy(points)