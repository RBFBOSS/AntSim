from Action import Action
from Worker import Worker
from Soldier import Soldier


class Colony:
    def __init__(self, colony_id, x: int, y: int):
        self.colony_id = colony_id
        self.ants = []
        self.food_supply = 0
        self.food_supply_size = 1000
        self.health = 500
        self.ant_production = 5  # Ants produces per minute
        self.ant_production_ratio = 0  # How many soldiers produced/100 ants
        self.x = x
        self.y = y
        self.boundary_radius = 100

    def produce_ant(self, ant_type) -> None:
        if ant_type.lower() == 'worker':
            self.ants.append(Worker(Action.IDLE, 10, self.x, self.y, 0, 0, self.colony_id))
        else:
            self.ants.append(Soldier(Action.IDLE, 20, self.x, self.y, 0, 0, self.colony_id))

    def print_ants(self):
        for ant in self.ants:
            if isinstance(ant, Worker):
                print("Worker")
            elif isinstance(ant, Soldier):
                print("Soldier")

    def defend(self) -> None:
        # Implement the logic to defend the colony if invaders are found within boundaries
        pass

    def update(self):
        for ant in self.ants:
            ant.update()
