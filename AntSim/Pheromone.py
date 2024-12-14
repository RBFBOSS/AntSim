class Pheromone:
    def __init__(self, target, creator, time_target_observed, creation_time):
        self.target = target
        self.creator = creator
        self.time_target_observed = time_target_observed
        self.creation_time = creation_time
