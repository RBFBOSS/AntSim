from Graphics import Graphics
from Simulation import Simulation

sim = Simulation()
sim.add_colony(10, 10)
sim.add_colony(200, 10)
col = sim.get_colony(0)
col.produce_ant('worker')
col.produce_ant('worker')
col1 = sim.get_colony(1)
col1.produce_ant('soldier')
col1.produce_ant('soldier')
col1.print_ants()
graphics = Graphics(sim)
