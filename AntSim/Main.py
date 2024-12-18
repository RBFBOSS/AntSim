from Globals import Globals
from Graphics import Graphics
from Simulation import Simulation

sim = Simulation()
sim.add_colony(500, 500)
sim.add_colony(1000, 500)
col = sim.get_colony(0)
for _ in range(Globals.col1_ants_generated):
    col.produce_ant('worker')
col1 = sim.get_colony(1)
for _ in range(Globals.col2_ants_generated):
    col1.produce_ant('soldier')
# sim.add_food_source(1300, 200)
sim.add_food_source(700, 300)
# sim.add_food_source(300, 300)
# sim.add_food_source(700, 700)
# sim.add_food_source(300, 700)
# sim.add_food_source(800, 500)
# sim.add_food_source(200, 500)
# sim.add_food_source(500, 800)
# sim.add_food_source(500, 200)
graphics = Graphics(sim)
