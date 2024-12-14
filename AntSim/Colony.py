from Action import Action
from Worker import Worker
from Soldier import Soldier


class Colony:
    def __init__(self, colony_id, x: int, y: int, speed: float):
        self.colony_id = colony_id
        self.speed = speed
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

    def produce_ant(self, ant_type) -> None:
        if ant_type.lower() == 'worker':
            self.ants.append(Worker(Action.IDLE, 10,
                                    self.x, self.y,
                                    0, 0,
                                    0, self.colony_id,
                                    self.speed))
            self.nr_of_workers += 1
        else:
            self.ants.append(Soldier(Action.IDLE, 20,
                                     self.x, self.y,
                                     0, 0,
                                     0, self.colony_id,
                                     self.speed))
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
        self.updates += 1
        if not self.updates % 10:
            print(f'Colony {self.colony_id} updated')

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
