from sim.sim_controller import SimController
import pytest
from sim.types import SurvivalConditions
from random import seed


def test_small_simulation():
    seed(1)
    controller = SimController(
        population=10, 
        generation_steps=100, 
        genome_length=4, 
        internal_neuron_count=1, 
        x_size=10, 
        y_size=10, 
        survival_condition= SurvivalConditions.RIGHT_SIDE, 
        mutation_chance=0.01)
    controller.setup_simulation()

    all_genomes = [indiv.genome for indiv in controller.individuals]
    assert all_genomes == ['18072e8c35bf992dc9e9c616612e7696', 'f1fd42a29755d4c13a902931cd447e35', '8712b8bc076f3787b9d179e06c0fd4f5', 'f3c64af775a89294c2cd789a380208a9', 'a46d6753ec148cb48e73ca47ea90a8f0', '3099fdf5ab99254ae901e35cd47d380d', '08d6af57da71144896c8da1964b2d2bc', '2c4a3698aa2ca1af6a107b75677f6cbd', '5fec898fbcfbb050acab1a6bc69d4bd8', 'bb968a437d5c8dfc5eda92d864ac5db9']
    assert controller.world.open_cells == {(0, 0): True, (0, 1): True, (0, 2): False, (0, 3): False, (0, 4): True, (0, 5): True, (0, 6): True, (0, 7): True, (0, 8): True, (0, 9): True, (1, 0): True, (1, 1): True, (1, 2): True, (1, 3): True, (1, 4): True, (1, 5): True, (1, 6): True, (1, 7): True, (1, 8): True, (1, 9): True, (2, 0): True, (2, 1): True, (2, 2): True, (2, 3): True, (2, 4): True, (2, 5): False, (2, 6): True, (2, 7): True, (2, 8): True, (2, 9): True, (3, 0): True, (3, 1): True, (3, 2): True, (3, 3): True, (3, 4): False, (3, 5): True, (3, 6): True, (3, 7): True, (3, 8): True, (3, 9): False, (4, 0): True, (4, 1): False, (4, 2): True, (4, 3): True, (4, 4): True, (4, 5): True, (4, 6): True, (4, 7): True, (4, 8): True, (4, 9): True, (5, 0): True, (5, 1): True, (5, 2): True, (5, 3): True, (5, 4): True, (5, 5): True, (5, 6): True, (5, 7): False, (5, 8): True, (5, 9): False, (6, 0): True, (6, 1): True, (6, 2): True, (6, 3): True, (6, 4): False, (6, 5): True, (6, 6): True, (6, 7): True, (6, 8): True, (6, 9): True, (7, 0): True, (7, 1): True, (7, 2): True, (7, 3): True, (7, 4): True, (7, 5): True, (7, 6): True, (7, 7): True, (7, 8): False, (7, 9): True, (8, 0): True, (8, 1): True, (8, 2): True, (8, 3): True, (8, 4): True, (8, 5): True, (8, 6): True, (8, 7): True, (8, 8): True, (8, 9): True, (9, 0): True, (9, 1): True, (9, 2): True, (9, 3): True, (9, 4): True, (9, 5): True, (9, 6): True, (9, 7): True, (9, 8): True, (9, 9): True}

    controller.run_simulation(10)
