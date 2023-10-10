from sim.sim_controller import SimController
import pytest
from sim.types import SurvivalConditions


def test_small_simulation():
    controller = SimController(100, 300, 4, 2, 50, 50, 
                               SurvivalConditions.RIGHT_SIDE, 0.01)
    controller.setup_simulation()
    controller.run_simulation(10)