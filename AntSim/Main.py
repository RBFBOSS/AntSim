from Graphics import Graphics
from Simulation import Simulation

sim = Simulation(1520, 900)
sim.add_colony(500, 200)
sim.add_colony(200, 500)
col = sim.get_colony(0)
for _ in range(250):
    col.produce_ant('worker')
col1 = sim.get_colony(1)
for _ in range(250):
    col1.produce_ant('soldier')
sim.add_food_source(300, 300)
graphics = Graphics(sim)
