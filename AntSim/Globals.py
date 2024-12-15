class Globals:
    global_time_frame = 0.0
    pheromone_drop_rate = 1

    @staticmethod
    def increment_time_frame():
        Globals.global_time_frame += 0.01
