from sim.sim_controller import SimController
from sim.types import SurvivalConditions


controller = SimController(
    population=100, 
    generation_steps=100, 
    genome_length=10, 
    internal_neuron_count=5, 
    x_size=30, 
    y_size=30, 
    survival_condition= SurvivalConditions.RIGHT_SIDE, 
    mutation_chance=0.01)
controller.setup_simulation()
controller.run_simulation(100)