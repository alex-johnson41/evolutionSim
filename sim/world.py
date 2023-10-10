from random import choice
from .individual import Individual


class World:
    
    def __init__(self, x_size: int, y_size: int) -> None:
        self.x_size = x_size
        self.y_size = y_size
        self.indiv_map: list[list[Individual | None]] = [[0 for y in range(y_size)] for x in range(x_size)]
        self.open_cells: dict[tuple[int, int], bool] = self._initialize_open_cells()

    def add_individual(self, individual: Individual, x_coord: int, y_coord: int) -> None:
        """ Adds an individual to the world at a specific x and y coordinate """
        self.indiv_map[x_coord][y_coord] = individual
        self.open_cells[(x_coord, y_coord)] = False

    def remove_individual(self, coords: tuple[int, int] | None = None, indiv: Individual | None = None) -> None:
        """ Removes a single individual from the world """
        if not coords and not indiv:
            raise Exception("Either coordinates to remove at or individual to remove must be specified")
        if coords and indiv:
            raise Exception("Only one of the params is allowed, not both")
        if coords:
            self.indiv_map[coords[0]][coords[1]] = None
            self.open_cells[(coords[0], coords[1])] = True
        if indiv:
            raise Exception("Removing by indiv currently not supported")

    def move_individual(self, individual: Individual, move_x: int, move_y: int):
        """ Find an individual in the world and move them if the desired cell is available"""
        start_x, start_y = self._find_individual(individual)
        end_x = start_x + move_x
        end_y = start_y + move_y
        if self.open_cells[(end_x, end_y)]:
            self.remove_individual((start_x, start_y))
            self.add_individual(individual, end_x, end_y)

    def clear_map(self) -> None:
        """ Removes all items from the map """
        self.indiv_map = [[]]
        self.open_cells = dict.fromkeys(self.open_cells, True)

    def cell_open(self, x_coord, y_coord) -> bool:
        """ Checks to see if a cell in the world is occupied """
        return self.open_cells[(x_coord, y_coord)]
    
    def find_open_cell(self) -> tuple[int, int]:
        """ Finds a random spot in the world that's empty and returns the coordinates """
        return choice(list([key for key, value in self.open_cells.items() if value]))
    
    def _find_individual(self, individual: Individual) -> tuple[int, int]:
        """ Private method to find an individual's x and y coordinates """
        x_coord, y_coord = individual.get_location()
        return x_coord * self.x_size, y_coord * self.y_size

    def _initialize_open_cells(self) -> dict[tuple[int, int], bool]:
        """ 
        Private method that returns dictionary of all x, y coordinates that aren't occupied 
        """
        open_cells = {}
        for x in range(self.x_size):
            for y in range(self.y_size):
                open_cells[(x,y)] = True
        return open_cells