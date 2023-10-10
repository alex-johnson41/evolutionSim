from sim.sim_controller import SimController
from sim.types import SurvivalConditions
from random import seed
from time import time
import cProfile


start = time()

seed(1)
controller = SimController(
    population=50, 
    generation_steps=50, 
    genome_length=4, 
    internal_neuron_count=1, 
    x_size=20, 
    y_size=20, 
    survival_condition= SurvivalConditions.RIGHT_SIDE, 
    mutation_chance=0.01,
    log=True,
    log_name=round(start))
controller.setup_simulation()
controller.run_simulation(50)

end = time()
print(f"RUNTIME: {end-start} seconds")