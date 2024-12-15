class Globals:
    global_time_frame = 0.0
    pheromone_drop_rate = 3
    update_pheromones_count = 10
    pheromone_lifespan = 10
    ants_FOV = 2

    @staticmethod
    def increment_time_frame():
        Globals.global_time_frame += 0.01
