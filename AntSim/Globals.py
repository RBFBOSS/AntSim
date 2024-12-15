class Globals:
    global_time_frame = 0.0
    pheromone_drop_rate = 1
    update_pheromones_count = 50
    pheromone_lifespan = 10
    ants_FOV = 3

    @staticmethod
    def increment_time_frame():
        Globals.global_time_frame += 0.01
