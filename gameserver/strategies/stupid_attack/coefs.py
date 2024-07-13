from dataclasses import dataclass

from model.state import LocationType


@dataclass
class Preset:
    empty: float = 1.0
    wall: float = 1.0
    zpot: float = 1.0
    zombie: float = 1.0
    enemy: float = 1.0
    my_base: float = 1.0

    def get_coef(self, count: dict[LocationType, int]) -> float:
        s = sum(
            (
                self.empty * count[LocationType.EMPTY],
                self.wall * count[LocationType.WALL],
                self.zpot * count[LocationType.ZPOT],
                self.zombie * count[LocationType.ZOMBIE],
                self.enemy * count[LocationType.ENEMY],
                self.my_base * count[LocationType.MY_BASE],
            )
        )
        c = sum(count.values())
        return s / c
