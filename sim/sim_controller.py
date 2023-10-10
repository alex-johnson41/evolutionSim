from typing import Any
from .utilities.numpy_wrapper import sign, tanh
from .world import World
from .individual import Individual
from random import choice, randrange, random, uniform
from .enums import InputTypes, MoveDirections, OutputTypes


class SimController:
    """ API for controlling a simulation """
    def __init__(self, population: int, generation_steps: int, genome_length: int, 
                 internal_neuron_count: int, x_size: int, y_size: int) -> None:
        self.world = World(x_size, y_size)
        self.generation_steps = generation_steps
        self.genome_length = genome_length
        self.internal_neuron_count = internal_neuron_count
        self.individuals = self._create_individuals(population)

    def setup_simulation(self):
        """ Set up first simulation generation """
        for indiv in self.individuals:
            x_coord, y_coord = self._add_indiv_to_world(indiv)
            data_dict = self._get_input_data(indiv, x_coord, y_coord)
            indiv.spawn(data_dict, self._create_random_genome())

    def run_simulation(self, generations: int) -> list[dict[str, int]]:
        """" Runs the simulation for x generations and returns basic data about each generation """
        for i in range(generations):
            self.run_generation()
            #TODO Add function to rebuild generation

    def run_generation(self) -> dict[str, int]:
        """ Simulates all steps of a single generation and returns a dictionary of basic data about the generation """
        for i in range(self.generation_steps):
            self.step()

    def step(self):
        """ Generate one step for all individuals """
        for individual in self.individuals:
            actions_dict = individual.step()
            self._perform_actions(individual, actions_dict)
            self._update_input_data(individual)

    def analyze_generation(self) -> dict[str, Any]:
        """ Returns more in depth data on a generation """
        pass
    
    def _perform_actions(self, individual: Individual, actions_dict: dict[OutputTypes, float]) -> None:
        """ Private method that calculates the probability of each action and performs it """    
        move_x = actions_dict[OutputTypes.MOVE_X] if OutputTypes.MOVE_X in actions_dict else 0
        move_y = actions_dict[OutputTypes.MOVE_Y] if OutputTypes.MOVE_Y in actions_dict else 0
        if OutputTypes.MOVE_FORWARD in actions_dict:
            x_dir, y_dir = individual.forward.value
            level = actions_dict[OutputTypes.MOVE_FORWARD]
            move_x += x_dir * level
            move_y += y_dir * level
        if OutputTypes.MOVE_RANDOM in actions_dict:
            x_dir, y_dir = choice(list(MoveDirections)).value
            level = actions_dict[OutputTypes.MOVE_RANDOM]
            move_x += x_dir * level
            move_y += y_dir * level
        probability_move_x = abs(tanh(move_x))
        probability_move_y = abs(tanh(move_y))
        move_x = int(uniform(0, 1) < probability_move_x) * sign(move_x)
        move_y = int(uniform(0, 1) < probability_move_y) * sign(move_y)
        if move_x and move_y:
            self.world.move_individual(move_x, move_y)
            individual.forward = MoveDirections((move_x, move_y)).name

    def _update_input_data(self, individual: Individual) -> None:
        data_dict = self._get_input_data(individual)
        individual.update_data(data_dict)

    def _get_input_data(self, individual: Individual, x_loc: int | None = None, 
                        y_loc: int | None = None) -> dict[InputTypes, float]:
        x_coord, y_coord = (individual.get_location()) if x_loc == None and y_loc == None else (x_loc, y_loc)
        data_dict = {}
        data_dict[InputTypes.X_POSITION] = x_coord / self.world.x_size
        data_dict[InputTypes.Y_POSITION] = y_coord / self.world.y_size
        data_dict[InputTypes.AGE] = 0
        data_dict[InputTypes.RANDOM]= random() 
        data_dict[InputTypes.X_DISTANCE] = round(x_coord / self.world.x_size)
        data_dict[InputTypes.Y_DISTANCE] = round(y_coord / self.world.y_size)
        return data_dict

    def _add_indiv_to_world(self, indiv: Individual) -> tuple[int, int]: 
        """ Private method that adds specific indiv to the world and returns it's location """
        x_coord, y_coord = self.world.find_open_cell()
        self.world.add_individual(indiv, x_coord, y_coord)
        return x_coord, y_coord

    def _create_individuals(self, population: int) -> list[Individual]:
        """ Private method that creates a list of individuals with neural networks from random genomes """
        indivs: list[Individual] = []
        for i in range(population):
            indiv = Individual(self.internal_neuron_count)
            indivs.append(indiv)
        return indivs

    def _create_random_genome(self) -> str:
        """ Private method that creates a random hexadecimal genome string for an individual """
        return f'%0{self.genome_length * 8}x' % randrange(16**self.genome_length * 8)