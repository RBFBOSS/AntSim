from Colony import Colony
from FoodSource import FoodSource
from Globals import Globals
import threading
import time


class Simulation:
    def __init__(self):
        self.update_count = 0
        Globals.initialize_matrix()
        self.pheromone_thread = threading.Thread(target=self.run_pheromone_cleanup)
        self.pheromone_thread.daemon = True
        self.pheromone_thread.start()

    def run_pheromone_cleanup(self):
        while True:
            if not Globals.pause_event.is_set():
                Globals.waiting_event.set()
                self.delete_old_pheromones()
                time.sleep(0.01)
            else:
                Globals.waiting_event.clear()
                time.sleep(0.01)

    @staticmethod
    def add_colony(x: int, y: int) -> None:
        Globals.colonies.append(Colony(len(Globals.colonies),
                                       x, y, Globals.matrix,
                                       Globals.pheromones))

    @staticmethod
    def get_colony(colony_id: int) -> Colony:
        return Globals.colonies[colony_id]

    @staticmethod
    def add_food_source(x: int, y: int) -> None:
        Globals.food_sources.append(FoodSource(len(Globals.food_sources), x, y, Globals.matrix))

    @staticmethod
    def get_food_source(food_source_id: int) -> FoodSource:
        return Globals.food_sources[food_source_id]

    @staticmethod
    def get_pheromone_by_position(x: int, y: int):
        for pheromone in Globals.pheromones:
            if pheromone.x == x and pheromone.y == y:
                return pheromone

    def update(self):
        Globals.increment_time_frame()
        # if Globals.global_time_frame >= 10:
        #     print('100 seconds passed')
        for colony in Globals.colonies:
            colony.update()
        self.update_count += 1
        if self.update_count >= Globals.update_pheromones_count:
            # self.delete_old_pheromones()
            self.update_count = 0
            print("Ant stats:")
            print('Object sighted -> ', Globals.avg_object_sighted_time / Globals.ant_operations)
            print('Move -> ', Globals.avg_move_time / Globals.ant_operations)
            print('Perform action -> ', Globals.avg_perform_action_time / Globals.ant_operations)
            print('Placement -> ', Globals.avg_placement_time / Globals.ant_operations)
            print('Pheromone drop -> ', Globals.avg_pheromone_drop_time / Globals.ant_operations)
            print('Pheromones sighted -> ', Globals.pheromones_sighted)
            print('Colonies sighted -> ', Globals.colonies_sighted)
            print('Ants sighted -> ', Globals.ants_sighted)
            print('Food sources sighted -> ', Globals.food_sources_sighted)
            print('Objects sighted -> ', Globals.objects_sighted)
            print('Entire time -> ', Globals.entire_time / Globals.ant_operations)
            Globals.objects_sighted = 0
            Globals.pheromones_sighted = 0
            Globals.colonies_sighted = 0
            Globals.ants_sighted = 0
            Globals.food_sources_sighted = 0
            print('-----------------------------------')

    @staticmethod
    def delete_old_pheromones():
        i = 0
        while i < len(Globals.pheromones):
            if (Globals.pheromones[i].creation_time + Globals.pheromone_lifespan <
                    Globals.global_time_frame):
                Globals.pheromones[i].clear()
                Globals.pheromones.pop(i)
            else:
                i += 1
