import numpy as np


class NpArray():
    pass

# Isolated numpy function wrappers:

def tanh(num: float) -> float:
    """ Return hyberbolic tangent of an input """
    return np.tanh(num)

def sign(num: float | int ) -> float | int:
    """ Return sign of an input """
    return np.sign(num)