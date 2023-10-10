from ..enums import OutputTypes
from .synapse import Synapse
from ..neurons.output_neuron import OutputNeuron


class NeuralNetwork:

    def __init__(self, synapses: list[Synapse]) -> None:
        """ 
        List of synapses connecting neurons 
        
        self.output_neurons is all the output neurons that have a connection to them
        """
        self.synapses = self._sort_synapses(synapses)
        self.output_neurons = list(set([synapse.output for synapse in self.synapses if isinstance(synapse.output, OutputNeuron)]))

    def get_actions(self) -> dict[OutputTypes, float]:
        """ Returns dictionary with likelihood that each output neuron with a connection to it will perform it's action """
        return {output_neuron.type: output_neuron.perform_action() for output_neuron in self.output_neurons}

    def _sort_synapses(self, synapses: list[Synapse]) -> list[Synapse]:
        """ 
        Private method to sort synapses so that input synapses are placed before output ones 
        
        This is done so that input neurons send their data to output/internal neurons before they try to output data
        """
        return sorted(synapses, key = lambda synapse: synapse.sorting_rank)