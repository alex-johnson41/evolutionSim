from abc import ABC


class Neuron(ABC):
    
    def __init__(self, id: int):
        """ Abstract base class that all neurons inherit from """
        self.id = id