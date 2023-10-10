from sim.utilities.numpy_wrapper import tanh
from .neuron import Neuron


class InternalNeuron(Neuron):

    def __init__(self, id: int) -> None:
        """ Internal neuron that takes data from input/internal neurons and processes it """
        super().__init__(id)
        self.data = []
        self.self_input: float = 0

    def get_data(self) -> float:
        """ Processes data from input/internal neurons, resets all data, and returns processed data """
        data = sum(self.data) + self.self_input
        self.self_input = 0
        self.data = []
        return tanh(data)
    
    def add_data(self, data: float) -> None:
        """ Add new data value to the neurons total data """
        self.data.append(data)
    
    def add_self_data(self, data: float) -> None:
        """ Add new data value from itself """
        self.self_input = data