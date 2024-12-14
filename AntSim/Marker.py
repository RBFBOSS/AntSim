from MarkerType import MarkerType


class Marker:
    def __init__(self, m_type, target, creator, time_target_observed, creation_time):
        self.m_type = m_type
        if m_type != MarkerType.PHEROMONE:
            self.time_target_observed = 0
            self.target = None
            self.age = 0
        else:
            self.time_target_observed = time_target_observed
            self.target = target
            self.creation_time = creation_time
        self.creator = creator
        self.age = 0
