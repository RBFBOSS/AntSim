from MarkerType import MarkerType


class Marker:
    def __init__(self, m_type, target, creator, distance, creation_time):
        self.m_type = m_type
        if m_type != MarkerType.PHEROMONE:
            self.distance = 0
            self.target = None
            self.age = 0
        else:
            self.distance = distance
            self.target = target
            self.creation_time = creation_time
        self.ant_reference = None
        self.creator = creator
        self.age = 0
