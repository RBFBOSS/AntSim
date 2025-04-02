from enum import Enum


class Action(Enum):
    IDLE = 0
    FOOD = 1
    COLONY = 2
    ATTACK = 3
    TO_ENEMY = 4
    PATROL = 5
