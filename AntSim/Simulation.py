from Colony import Colony
from FoodSource import FoodSource
from Globals import Globals


class Simulation:
    def __init__(self, width: int, height: int):
        self.colonies = []
        self.food_sources = []
        self.speed = 1
        self.exploration_rate = 0.05
        self.width = width
        self.height = height
        self.matrix = [[None for _ in range(width)] for _ in range(height)]
        self.ants_FOV = 20
        self.update_count = 0
        self.pheromones = []

    def add_colony(self, x: int, y: int) -> None:
        self.colonies.append(Colony(len(self.colonies),
                                    x, y, self.speed,
                                    self.exploration_rate,
                                    self.ants_FOV, self.matrix,
                                    self.pheromones))

    def get_colony(self, colony_id: int) -> Colony:
        return self.colonies[colony_id]

    def add_food_source(self, y: int, x: int) -> None:
        self.food_sources.append(FoodSource(len(self.food_sources), y, x, self.matrix))

    def get_food_source(self, food_source_id: int) -> FoodSource:
        return self.food_sources[food_source_id]

    def update(self):
        Globals.increment_time_frame()
        for colony in self.colonies:
            colony.update()
        self.update_count += 1
        if self.update_count >= 20:
            self.delete_old_pheromones()
            self.update_count = 0

    def delete_old_pheromones(self):
        i = 0
        while i < len(self.pheromones):
            if (self.pheromones[i].creation_time + 50 <
                    Globals.global_time_frame):
                self.pheromones[i].clear()
                self.pheromones.pop(i)
            else:
                i += 1
