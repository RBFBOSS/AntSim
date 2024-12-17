from Colony import Colony
from FoodSource import FoodSource
from Globals import Globals


class Simulation:
    def __init__(self, width: int, height: int):
        self.colonies = []
        self.food_sources = []
        self.width = width
        self.height = height
        self.matrix = [[None for _ in range(width)] for _ in range(height)]
        self.ants_FOV = Globals.ants_FOV
        self.update_count = 0
        self.pheromones = []

    def add_colony(self, x: int, y: int) -> None:
        self.colonies.append(Colony(len(self.colonies),
                                    x, y,
                                    self.ants_FOV, self.matrix,
                                    self.pheromones))

    def get_colony(self, colony_id: int) -> Colony:
        return self.colonies[colony_id]

    def add_food_source(self, x: int, y: int) -> None:
        self.food_sources.append(FoodSource(len(self.food_sources), x, y, self.matrix))

    def get_food_source(self, food_source_id: int) -> FoodSource:
        return self.food_sources[food_source_id]

    def update(self):
        Globals.increment_time_frame()
        for colony in self.colonies:
            colony.update()
        self.update_count += 1
        if self.update_count >= Globals.update_pheromones_count:
            self.delete_old_pheromones()
            self.update_count = 0
            # print("Ant stats:")
            # print('Object sighted -> ', Globals.avg_object_sighted_time / Globals.ant_operations)
            # # print('Move -> ', Globals.avg_move_time / Globals.ant_operations)
            # # print('Perform action -> ', Globals.avg_perform_action_time / Globals.ant_operations)
            # # print('Placement -> ', Globals.avg_placement_time / Globals.ant_operations)
            # # print('Pheromone drop -> ', Globals.avg_pheromone_drop_time / Globals.ant_operations)
            # print('Pheromones sighted -> ', Globals.pheromones_sighted)
            # print('Colonies sighted -> ', Globals.colonies_sighted)
            # print('Ants sighted -> ', Globals.ants_sighted)
            # print('Food sources sighted -> ', Globals.food_sources_sighted)
            # print('Objects sighted -> ', Globals.objects_sighted)
            # print('Entire time -> ', Globals.entire_time / Globals.ant_operations)
            # Globals.objects_sighted = 0
            # Globals.pheromones_sighted = 0
            # Globals.colonies_sighted = 0
            # Globals.ants_sighted = 0
            # Globals.food_sources_sighted = 0
            # print('-----------------------------------')

    def delete_old_pheromones(self):
        i = 0
        while i < len(self.pheromones):
            if (self.pheromones[i].creation_time + Globals.pheromone_lifespan <
                    Globals.global_time_frame):
                self.pheromones[i].clear()
                self.pheromones.pop(i)
            else:
                i += 1
