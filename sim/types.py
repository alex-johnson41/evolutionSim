from enum import Enum


class InputTypes(Enum):
    """ All the input neuron types an individual will have """
    AGE = 0
    RANDOM = 1
    Y_DISTANCE = 2
    X_DISTANCE = 3
    Y_POSITION = 4
    X_POSITION = 5

class OutputTypes(Enum):
    """ All the output neuron types an individual will have """
    MOVE_FORWARD = 0
    MOVE_X = 0
    MOVE_Y = 0
    MOVE_RANDOM = 0
    
class MoveDirections(Enum):
    """ All possible directions an individual can move """
    N  = ( 0,  1)
    S  = ( 0, -1)
    E  = ( 1,  0)
    W  = (-1,  0)
    NE = ( 1,  1)
    SE = ( 1, -1)
    SW = (-1, -1)
    NW = ( 1, -1)

class SurvivalConditions(Enum):
    """All supported survial conditions for a generation """
    RIGHT_SIDE = 0