from Colony import Colony


class Simulation:
    def __init__(self):
        self.colonies = []

    def add_colony(self, x: int, y: int) -> None:
        self.colonies.append(Colony(len(self.colonies), x, y))

    def get_colony(self, colony_id: int) -> Colony:
        return self.colonies[colony_id]

    def update(self):
        for colony in self.colonies:
            colony.update()
