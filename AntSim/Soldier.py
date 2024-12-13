from Ant import Ant
from Action import Action


class Soldier(Ant):
    def __init__(self, destination: Action, attack: int, x: int, y: int, heading: int, state: int,
                 colony_id: int):
        super().__init__(10, destination, attack, x, y, heading, state, colony_id)
