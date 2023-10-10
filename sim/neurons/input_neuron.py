from sim.types import InputTypes
from .neuron import Neuron


class InputNeuron(Neuron):

    def __init__(self, type: InputTypes, id: int) -> None:
        """ Neuron that contains sensory data from the world or information about the individual """
        super().__init__(id)
        self.type = type

    def set_data(self, data: float) -> None:
        """ Initialize the data that the neuron contains """
        self.data = data

    def get_data(self) -> float:
        """ Return the data if it has been set """
        try:
            return self.data
        except:
            raise Exception("Data has not been set")