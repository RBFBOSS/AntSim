from enum import Enum


class PheromoneType(Enum):
    TO_ENEMY = 0
    TO_FOOD = 1
    TO_ENEMY_COLONY = 2
    TO_COLONY = 3
    BLOOD = 4
