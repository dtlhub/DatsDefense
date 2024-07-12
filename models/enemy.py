class EnemyPoint:
    def __init__(self, attack, health, is_head, last_attack, name, x, y):
        self.attack = attack
        self.health = health 
        self.id = id
        self.is_head = is_head 
        self.last_attack = last_attack
        self.name = name
        self.x = x 
        self.y = y


def enemy_points_from_json(enemy_data: dict) -> EnemyPoint:
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


def enemy_from_json(enemy_data: list) -> Base:
     points = [enemy_points_from_jsone(i) for i in enemy_data]
     return Enemy(points)