from sim.sim_controller import SimController
import pytest


def test_small_simulation():
    controller = SimController(100, 1000, 4, 2, 50, 50)
    assert controller.generation_steps == 1000
    controller.setup_simulation()
    controller.run_generation()