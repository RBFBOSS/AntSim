from Graphics import Graphics
from Simulation import Simulation

sim = Simulation()
sim.add_colony(500, 200)
sim.add_colony(200, 500)
col = sim.get_colony(0)
for _ in range(1000):
    col.produce_ant('worker')
col1 = sim.get_colony(1)
for _ in range(1000):
    col1.produce_ant('worker')
sim.add_food_source(300, 300)
graphics = Graphics(sim)
