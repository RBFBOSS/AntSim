import random

from Action import Action
from Globals import Globals
from Marker import Marker
from MarkerType import MarkerType
from Worker import Worker
from Soldier import Soldier


class Colony:
    def __init__(self, colony_id, x: int, y: int,
                 matrix, pheromones):
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
        self.updates = 0
        self.nr_of_workers = 0
        self.nr_of_soldiers = 0
        self.matrix = matrix
        above = int(max(0, self.y - 30))
        below = int(min(899, self.y + 30))
        left = int(max(0, self.x - 30))
        right = int(min(1519, self.x + 30))
        for i in range(above, below):
            for j in range(left, right):
                self.matrix[i][j] = Marker(MarkerType.COLONY,
                                           None, self.colony_id,
                                           0, Globals.global_time_frame)
        self.pheromones = pheromones

    def produce_ant(self, ant_type) -> None:
        heading_x = random.choice([-1, 0, 1])
        if heading_x == 0:
            heading_y = random.choice([-1, 1])
        else:
            heading_y = random.choice([-1, 0, 1])
        if ant_type.lower() == 'worker':
            self.ants.append(Worker(Action.FOOD, 10,
                                    self.x, self.y,
                                    heading_x, heading_y,
                                    0, self.colony_id,
                                    self.matrix, self.pheromones))
            self.nr_of_workers += 1
        else:
            self.ants.append(Soldier(Action.IDLE, 20,
                                     self.x, self.y,
                                     heading_x, heading_y,
                                     0, self.colony_id,
                                     self.matrix, self.pheromones))
            self.nr_of_soldiers += 1

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

    def send_ants(self, percentage, destination: Action) -> None:
        if percentage > 1:
            percentage = 1

        if destination == Action.FOOD:
            nr_of_ants = int(percentage * self.nr_of_workers)
            for ant in self.ants:
                if isinstance(ant, Worker):
                    ant.destination = destination
                    nr_of_ants -= 1
                    if not nr_of_ants:
                        break
