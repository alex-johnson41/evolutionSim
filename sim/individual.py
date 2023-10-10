import re
from random import choice
from .neural_network.neural_network import NeuralNetwork
from .neural_network.synapse import Synapse
from .neurons.input_neuron import InputNeuron
from .neurons.output_neuron import OutputNeuron
from .neurons.internal_neuron import InternalNeuron
from .types import InputTypes, OutputTypes, MoveDirections


class Individual:

    def __init__(self, internal_neuron_count: int) -> None:
        """ An individual unit in the simulation """
        self.input_neurons_dict = {id: InputNeuron(type, id) for id, type in enumerate(InputTypes)}
        self.output_neurons_dict = {id: OutputNeuron(type, id) for id, type in enumerate(OutputTypes)}
        self.internal_neurons_dict = {id: InternalNeuron(id) for id in range(internal_neuron_count)}
        self.forward = choice(list(MoveDirections))

    def spawn(self, input_data: dict[InputTypes, float], genome_hex: str) -> None:
        """ Sets all the input data of the individual's input neurons and creates it's neural network """
        self._set_input_data(input_data)
        self._create_nnet(genome_hex)

    def update_data(self, input_data: dict[InputTypes, float]) -> None:
        """ Updates internal neuron data to new input data """
        self._set_input_data(input_data)

    def step(self) -> dict[OutputTypes, float]:
        """ Calculates action(s) from input neuron data using neural network """
        for synapse in self.nnet.synapses: 
            synapse.send_data()
        return self.nnet.get_actions()
    
    def get_location(self) -> tuple[float, float]:
        """ Retrieves the individuals location from it's input nodes """
        try:
            for neuron in self.input_neurons_dict.values():
                if neuron.type == InputTypes.X_POSITION:
                    x_coord = neuron.data
                if neuron.type == InputTypes.Y_POSITION:
                    y_coord = neuron.data
            return x_coord, y_coord
        except:
            raise Exception("Neural network hasn't been created - no data to pull from")
    
    def _create_nnet(self, genome_hex: str) -> None:
        """ Creates neural network from hexadecimal genome string """
        self.genome = genome_hex
        self.nnet = self._decode_genome_hex(genome_hex)

    def _set_input_data(self, input_data: dict[InputTypes, float]) -> None:
        """ Private method that sets input neurons input data """
        for neuron in self.input_neurons_dict.values():
            neuron.set_data(input_data[neuron.type])

    def _decode_genome_hex(self, genome_hex: str) -> NeuralNetwork:
        """ Private method that decodes hexadecimal genome string into a neural network of synapses """
        synapses = []
        binary_genome = re.findall('.{1,32}', bin(int(genome_hex, 16))[2:].zfill(4*len(genome_hex)))
        for binary_gene in binary_genome:
            input_type = int(binary_gene[0], 2)
            input_id = int(binary_gene[1:8], 2)
            output_type = int(binary_gene[8], 2)
            output_id = int(binary_gene[9:16], 2)
            weight_sign = int(binary_gene[16], 2)
            unsigned_weight = int(binary_gene[17:], 2) / 10000
            weight = unsigned_weight * -1 if weight_sign else unsigned_weight
            input_neuron = self.internal_neurons_dict[input_id % len(self.internal_neurons_dict)] if input_type else self.input_neurons_dict[input_id % len(self.input_neurons_dict)]
            output_neuron = self.internal_neurons_dict[output_id % len(self.internal_neurons_dict)] if output_type else self.output_neurons_dict[output_id % len(self.output_neurons_dict)]
            synapses.append(Synapse(input_neuron, output_neuron, weight))
        return NeuralNetwork(synapses)