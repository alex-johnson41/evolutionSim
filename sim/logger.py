from .individual import Individual
from .world import World
from os import mkdir


class Logger:

    def __init__(self, log: bool, name: str) -> None:
        self.log = log
        self.name = name
        mkdir(f"logs/{self.name}")

    def setup(self, generations: int):
        for i in range(generations):
            mkdir(f"logs/{self.name}/{i}")

    def log_step(self, generation_id: int, world: World):
        if not self.log: return
        with open(f"logs/{self.name}/{generation_id}/step_log_human.txt", "a") as file:
            for row in world.indiv_map:
                for item in row:
                    if not item:
                        file.write("-")
                    if isinstance(item, Individual):
                        file.write("*")
                file.write("\n")
            file.write("\n\n")
                    
    def log_generation(self, generation_id: int, survivors: list[Individual]):
        if not self.log: return
        with open(f"logs/{self.name}/{generation_id}/generation_log.txt", "a") as file:
            pass

    def log_simulation(self):
        if not self.log: return 
        with open(f"logs/{self.name}/_simulation_log.txt", "a") as file:
            pass