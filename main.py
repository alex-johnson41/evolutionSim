from sim.sim_controller import SimController
from sim.types import SurvivalConditions
from random import seed
from time import time
import cProfile


start = time()

seed(1)
controller = SimController(
    population=100, 
    generation_steps=300, 
    genome_length=6, 
    internal_neuron_count=2, 
    x_size=100, 
    y_size=100, 
    survival_condition= SurvivalConditions.RIGHT_SIDE, 
    mutation_chance=0.01)
controller.setup_simulation()
controller.run_simulation(50)

end = time()
print(f"RUNTIME: {end-start} seconds")