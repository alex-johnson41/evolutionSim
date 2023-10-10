from sim.neurons.input_neuron import InputNeuron
from sim.neurons.output_neuron import OutputNeuron
from sim.neurons.internal_neuron import InternalNeuron


class Synapse:

    def __init__(self, input: InputNeuron | InternalNeuron,
                 output: OutputNeuron | InternalNeuron, weight: float) -> None:
        """ A connection between two neurons, and a weight to apply to the connection """
        self.input = input
        self.output = output
        self.weight = weight
        self.sorting_rank = self._get_sorting_rank()

    def send_data(self) -> None:
        """ Applys the weight to the input data and sends it to the output or internal neuron """
        weighted_data = self.input.get_data() * self.weight
        if self.input == self.output: # Edge case when internal neuron feeds itself
            self.output.add_self_data(weighted_data)
        else:
            self.output.add_data(weighted_data)

    def _get_sorting_rank(self) -> int:
        """ Determines where among the other synapses that the synapse should be fired """
        if isinstance(self.input, InputNeuron) and isinstance(self.output, InternalNeuron):
            return 0
        if self.input == self.output: # This is out of order becuase it's easier to check if 
            return 2                  # they're identical before seeing if they're both internal neurons
        if isinstance(self.input, InternalNeuron) and isinstance(self.output, InternalNeuron):
            return 1
        return 3