from sim.utilities.numpy_wrapper import tanh
from .neuron import Neuron
from random import uniform
from sim.types import OutputTypes


class OutputNeuron(Neuron):

    def __init__(self, type: OutputTypes, id: int) -> None:
        """ Output neuron that decides whether or not an action is taken """
        super().__init__(id)
        self.type = type
        self.data = []

    def perform_action(self) -> float:
        """ Processes data into the probability that it will perform the action """
        try:
            data = self.data
            self.data = []
            return tanh(sum(data))
        except:
            raise Exception("No data has been set")
    
    def add_data(self, data: float):
        """ Add a new data value to the neurons total data """
        self.data.append(data)