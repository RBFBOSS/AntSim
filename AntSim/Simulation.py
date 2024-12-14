from Colony import Colony
from FoodSource import FoodSource


class Simulation:
    def __init__(self):
        self.colonies = []
        self.food_sources = []
        self.speed = 2

    def add_colony(self, x: int, y: int) -> None:
        self.colonies.append(Colony(len(self.colonies), x, y, self.speed))

    def get_colony(self, colony_id: int) -> Colony:
        return self.colonies[colony_id]

    def add_food_source(self, x: int, y: int) -> None:
        self.food_sources.append(FoodSource(len(self.food_sources), x, y))

    def get_food_source(self, food_source_id: int) -> FoodSource:
        return self.food_sources[food_source_id]

    def update(self):
        for colony in self.colonies:
            colony.update()
