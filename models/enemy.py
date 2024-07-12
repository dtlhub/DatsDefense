class Enemy:
    def __init__(self, attack, health, is_head, last_attack, name, x, y):
        self.attack = attack
        self.health = health 
        self.id = id
        self.is_head = is_head 
        self.last_attack = last_attack
        self.name = name
        self.x = x 
        self.y = y


def enemy_from_json(enemy_data: dict) -> Enemy:
    return Enemy(
        enemy_data['attack'],
        enemy_data['health'],
        enemy_data['is_head'],
        enemy_data['last_attack'],
        enemy_data['name'],
        enemy_data['x'],
        enemy_data['y']
    )