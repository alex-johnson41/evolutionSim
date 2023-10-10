from sim.individual import Individual
from sim.types import InputTypes, OutputTypes
from sim.neural_network.neural_network import NeuralNetwork
from sim.neural_network.synapse import Synapse
import pytest
from random import seed


def test_indiv():
    seed(1)
    num_internal_neurons = 3
    indiv = Individual(num_internal_neurons)
    assert len(indiv.input_neurons_dict) == len(InputTypes)
    assert len(indiv.output_neurons_dict) == len(OutputTypes)
    assert len(indiv.internal_neurons_dict) == num_internal_neurons
    
    input_data = {InputTypes.AGE: 0, 
                  InputTypes.RANDOM: 0.1,
                  InputTypes.X_POSITION: 0.4345,
                  InputTypes.Y_POSITION: .345,
                  InputTypes.X_DISTANCE: 0.28,
                  InputTypes.Y_DISTANCE: .97}
    indiv.spawn(input_data, '9F1CE661AFFCE661A362517886c664676e6abc754dafbc016a3032383339343567683739') 
    
    for neuron in indiv.input_neurons_dict.values():
        ntype = neuron.type
        assert neuron.get_data() == input_data[ntype] 
    
    for i in range(len(indiv.nnet.synapses) - 1):
        assert indiv.nnet.synapses[i].sorting_rank <= indiv.nnet.synapses[i+1].sorting_rank 

    assert indiv.step() == {OutputTypes.MOVE_FORWARD: -0.9942877617090972}