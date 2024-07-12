class Zpot:
    def __init__(self, x, y, type):
        self.x = x 
        self.y = y
        self.type = type 

class World:
    def __init__(self, realm_name, zpots):
        self.realm_name = realm_name
        self.zpots = zpots 


def world_from_json(world_data: dict) -> World:
    zpots = [Zpot(zpot_data['x'], zpot_data['y']) for zpot_data in world_data['zpots']]
    return World(world_data['realmName'], zpots)