class Zombie:
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
        pass


def zombie_from_json(zombie_data: dict) -> Zombie:
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