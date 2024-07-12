class Base:
    def __init__(self, attack, health, id, is_head, last_attack, range, x, y):
        self.attack = attack
        self.health = health
        self.id = id
        self.is_head = is_head
        self.last_attack = last_attack
        self.range = range
        self.x = x
        self.y = y


def base_from_json(base_data: dict) -> Base:
    return Base(
        base_data['attack'],
        base_data['health'],
        base_data['id'],
        base_data['isHead'],
        base_data['lastAttack'],
        base_data['range'],
        base_data['x'],
        base_data['y']
    )