class Globals:
    global_time_frame = 0.0
    pheromone_drop_rate = 2
    update_pheromones_count = 10
    pheromone_lifespan = 5
    ants_FOV = 1

    @staticmethod
    def increment_time_frame():
        Globals.global_time_frame += 0.01
