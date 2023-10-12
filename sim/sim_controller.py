from typing import Any
from .utilities.numpy_wrapper import sign, tanh
from .world import World
from .individual import Individual
from random import choice, randrange, random, uniform
from collections import Counter
from .types import InputTypes, MoveDirections, OutputTypes, SurvivalConditions
from .logger import Logger


class SimController:
    """ API for controlling a simulation """
    def __init__(self, population: int, generation_steps: int, genome_length: int, 
                 internal_neuron_count: int, x_size: int, y_size: int, survival_condition: SurvivalConditions,
                 mutation_chance: float, log_name: str = "log_", log: bool = False) -> None:
        self.world = World(x_size, y_size)
        self.population = population
        self.generation_steps = generation_steps
        self.genome_length = genome_length
        self.internal_neuron_count = internal_neuron_count
        self.individuals = self._create_individuals(population)
        self.survival_condition = survival_condition
        self.mutation_chance = mutation_chance
        self.logger = Logger(log, log_name)
        self.pause = False

    def setup_simulation(self):
        """ Set up first simulation generation """
        for indiv in self.individuals:
            x_coord, y_coord = self._add_indiv_to_world(indiv)
            data_dict = self._get_input_data(indiv, 0, x_coord, y_coord)
            indiv.spawn(data_dict, self._create_random_genome())

    def run_simulation(self, generations: int) -> list[dict[str, int]]:
        """" Runs the simulation for x generations and returns basic data about each generation """
        self.logger.setup(generations)
        for i in range(generations):
            self.run_generation(i)
            self._setup_next_generation()
        self.logger.log_simulation()

    def run_generation(self, generation_id: str) -> dict[str, int]:
        """ Simulates all steps of a single generation and returns a dictionary of basic data about the generation """
        for i in range(self.generation_steps):
            self.step(i, generation_id)
        self.logger.log_generation(generation_id, len(self._find_survivors()))

    def step(self, generation_step: int, generation_id: int):
        """ Generate tne step for all individuals """
        for individual in self.individuals:
            actions_dict = individual.step()
            new_x_int, new_y_int = self._perform_actions(individual, actions_dict)
            self._update_input_data(individual, generation_step, new_x_int, new_y_int)
        self.logger.log_step(generation_id, self.world)

    def analyze_generation(self) -> dict[str, Any]:
        """ Returns more in depth data on a generation """
        pass

    def pause_resume_simulation(self) -> None:
        """ Modifies flag to pause the simulation """
        self.pause = not self.pause
    
    def _setup_next_generation(self) -> None:
        original = len(self.individuals)
        self.individuals = self._find_survivors()
        print(len(self.individuals)/original * 100)
        new_indivs = self._new_indivs()
        self.individuals += new_indivs
        self.world.clear_map()
        for indiv in self.individuals:
            x_coord, y_coord = self._add_indiv_to_world(indiv)
            data_dict = self._get_input_data(indiv, 0, x_coord, y_coord)
            indiv._set_input_data(data_dict)

    def _new_indivs(self) -> list[Individual]:
        """ Creates individuals with potential mutations replacing the ones that died in past generation """
        indivs = []
        for i in range(self.population - len(self.individuals)):
            mutation_chance = random()
            genome_hex = choice(self.individuals).genome
            if mutation_chance < self.mutation_chance:
                genome_hex = list(genome_hex)
                genome_hex[randrange(0, len(genome_hex))] = str(choice("0123456789ABCDEF"))
                genome_hex = ''.join(genome_hex)
            indiv = Individual(self.internal_neuron_count)
            indiv._create_nnet(genome_hex)
            indivs.append(indiv)
        return indivs

    def _find_survivors(self) -> list[Individual]:
        survivors = []
        match self.survival_condition:
            case SurvivalConditions.RIGHT_SIDE:
                for indiv in self.individuals:
                    x_coord, y_coord = self.world._find_individual(indiv)
                    if x_coord >= self.world.x_size / 2:
                        survivors.append(indiv)
            case SurvivalConditions.LEFT_SIDE:
                for indiv in self.individuals:
                    x_coord, y_coord = self.world._find_individual(indiv)
                    if x_coord <= self.world.x_size / 2:
                        survivors.append(indiv)
        return survivors

    def _perform_actions(self, individual: Individual, actions_dict: dict[OutputTypes, float]) -> tuple[int|None, int|None]:
        """ Private method that calculates the probability of each action and performs it """    
        x_offset = actions_dict[OutputTypes.MOVE_X] if OutputTypes.MOVE_X in actions_dict else 0
        y_offset = actions_dict[OutputTypes.MOVE_Y] if OutputTypes.MOVE_Y in actions_dict else 0
        if OutputTypes.MOVE_FORWARD in actions_dict:
            x_dir, y_dir = individual.forward.value
            level = actions_dict[OutputTypes.MOVE_FORWARD]
            x_offset += x_dir * level
            y_offset += y_dir * level
        if OutputTypes.MOVE_RANDOM in actions_dict:
            x_dir, y_dir = choice(list(MoveDirections)).value
            level = actions_dict[OutputTypes.MOVE_RANDOM]
            x_offset += x_dir * level
            y_offset += y_dir * level
        probability_x_offset = abs(tanh(x_offset))
        probability_y_offset = abs(tanh(y_offset))
        x_offset = int((uniform(0, 1) < probability_x_offset) * sign(x_offset))
        y_offset = int((uniform(0, 1) < probability_y_offset) * sign(y_offset))
        if x_offset or y_offset:
            new_x_int, new_y_int = self.world.move_individual(individual, x_offset, y_offset)
            individual.forward = MoveDirections((x_offset, y_offset))
            return new_x_int, new_y_int
        return None, None

    def _update_input_data(self, individual: Individual, generation_step: int, new_x_int: int | None = None, new_y_int: int | None = None) -> None:
        data_dict = self._get_input_data(individual, generation_step, new_x_int, new_y_int)
        individual.update_data(data_dict)

    def _get_input_data(self, individual: Individual, generation_step: int, 
                        x_loc: int | None = None, y_loc: int | None = None) -> dict[InputTypes, float]:
        """ Gathers and returns sensory information for an individual """
        if x_loc is not None and y_loc is not None:
            x_coord_int = x_loc
            y_coord_int = y_loc
        else:
            x_coord_int, y_coord_int = self.world._find_individual(individual)
        data_dict = {}
        data_dict[InputTypes.X_POSITION] = x_coord_int / self.world.x_size
        data_dict[InputTypes.Y_POSITION] = y_coord_int / self.world.y_size
        data_dict[InputTypes.AGE] = generation_step
        data_dict[InputTypes.RANDOM]= random() 
        data_dict[InputTypes.X_DISTANCE] = round(x_coord_int / self.world.x_size)
        data_dict[InputTypes.Y_DISTANCE] = round(y_coord_int / self.world.y_size)
        return data_dict

    def _add_indiv_to_world(self, indiv: Individual) -> tuple[int, int]: 
        """ Method that adds specific indiv to the world and returns it's location """
        x_coord_int, y_coord_int = self.world.find_open_cell()
        self.world.add_individual(indiv, x_coord_int, y_coord_int)
        return x_coord_int, y_coord_int

    def _create_individuals(self, population: int) -> list[Individual]:
        """ Private method that creates a list of individuals with neural networks from random genomes """
        indivs: list[Individual] = []
        for i in range(population):
            indiv = Individual(self.internal_neuron_count)
            indivs.append(indiv)
        return indivs

    def _create_random_genome(self) -> str:
        """ Private method that creates a random hexadecimal genome string for an individual """
        return f'%0{self.genome_length * 8}x' % randrange(16**(self.genome_length*8))