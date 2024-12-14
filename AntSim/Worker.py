from Ant import Ant
from Action import Action


class Worker(Ant):
    def __init__(self, destination: Action, attack: int, x: int, y: int, heading_x: int, heading_y: int, state: int,
                 colony_id: int, speed: int):
        super().__init__(10, destination, attack, x, y, heading_x, heading_y, state, colony_id, speed)
