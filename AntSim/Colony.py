import random

from Action import Action
from Globals import Globals
from Marker import Marker
from MarkerType import MarkerType
from Worker import Worker
from Soldier import Soldier


class Colony:
    def __init__(self, colony_id, x: int, y: int,
                 matrix, pheromones, simulation):
        self.simulation = simulation
        self.colony_id = colony_id
        self.is_making_soldiers = False
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

    def produce_ant_init(self, ant_type) -> None:
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
                                    self.matrix, self.pheromones, self.simulation))
            self.nr_of_workers += 1
        else:
            self.ants.append(Soldier(Action.IDLE, 20,
                                     self.x, self.y,
                                     heading_x, heading_y,
                                     0, self.colony_id,
                                     self.matrix, self.pheromones, self.simulation))
            self.nr_of_soldiers += 1

    def produce_ant(self, ant_type) -> None:
        self.produce_ant_init(ant_type)
        if ant_type.lower() == 'worker':
            if len(self.ants) >= Globals.max_workers_per_colony:
                return
            self.food_supply -= Globals.worker_production_cost
        else:
            if len(self.ants) >= Globals.max_soldiers_per_colony:
                return
            self.food_supply -= Globals.soldier_production_cost

    def delete_ant(self, ant) -> None:
        self.ants.remove(ant)
        if isinstance(ant, Worker):
            self.nr_of_workers -= 1
        else:
            self.nr_of_soldiers -= 1

    def add_food(self, amount):
        self.food_supply += amount
        if self.food_supply > self.food_supply_size:
            self.food_supply = self.food_supply_size

    def remove_food(self):
        self.food_supply = max(0, self.food_supply - self.nr_of_workers * Globals.worker_maintenance_cost
                               - self.nr_of_soldiers * Globals.soldier_maintenance_cost)

    def check_for_starvation(self):
        if (self.food_supply < self.nr_of_workers * Globals.worker_maintenance_cost
                + self.nr_of_soldiers * Globals.soldier_maintenance_cost):
            dif = (self.nr_of_workers * Globals.worker_maintenance_cost
                   + self.nr_of_soldiers * Globals.soldier_maintenance_cost - self.food_supply)
            for ant in self.ants:
                if isinstance(ant, Soldier):
                    self.delete_ant(ant)
                    dif -= Globals.soldier_maintenance_cost
                    if dif <= 0:
                        break
            if dif > 0:
                for ant in self.ants:
                    if isinstance(ant, Worker):
                        self.delete_ant(ant)
                        dif -= Globals.worker_maintenance_cost
                        if dif <= 0:
                            break

    def print_ants(self):
        for ant in self.ants:
            if isinstance(ant, Worker):
                print("Worker")
            elif isinstance(ant, Soldier):
                print("Soldier")

    def start_making_soldiers(self):
        self.is_making_soldiers = True

    def defend(self) -> None:
        # Implement the logic to defend the colony if invaders are found within boundaries
        pass

    def update(self):
        if self.is_making_soldiers:
            while ((self.nr_of_workers * Globals.worker_maintenance_cost
                    + self.nr_of_soldiers * Globals.soldier_maintenance_cost) * 2 <=
                   self.food_supply):
                cond1 = False
                if self.nr_of_soldiers < Globals.max_soldiers_per_colony:
                    self.produce_ant('soldier')
                else:
                    cond1 = True
                cond2 = False
                if self.nr_of_workers < Globals.max_workers_per_colony:
                    self.produce_ant('worker')
                else:
                    cond2 = True
                if cond1 and cond2:
                    break
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
