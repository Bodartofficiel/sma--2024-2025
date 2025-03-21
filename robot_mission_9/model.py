# Group 9
# Bodart Thomas and Jacquemin Gaétan
# Created March 11
from random import choice, randint

from agents import GreenAgent, RedAgent, YellowAgent, Robot
from mesa import DataCollector, Model
from mesa.space import MultiGrid
from objects import Radioactivity, Waste, WasteDisposalZone


class RobotMission(Model):
    def __init__(
        self,
        n_robots: int,
        n_wastes: int,
        width: int,
        height: int,
        seed=None,
    ):
        super().__init__(seed=seed)
        self.grid = MultiGrid(width, height, False)

        waste_collector_pos = (width - 1, randint(0, height - 1))
        # Create radioactivity zones
        for x in range(width):
            zone = "z1" if x < width / 3 else "z2" if x < 2 * width / 3 else "z3"
            for y in range(height):
                if (x, y) == waste_collector_pos:
                    self.grid.place_agent(WasteDisposalZone(self), (x, y))
                    print("YOUYOU")
                    continue
                self.grid.place_agent(Radioactivity(zone, self), (x, y))

        # Place wastes
        for _ in range(n_wastes):
            color = choice(["green", "red", "yellow"])
            x = randint(0, width - 1)
            y = randint(0, height - 1)

            self.grid.place_agent(Waste(color, self), (x, y))

        # Place robots
        for _ in range(n_robots):
            x = randint(0, width - 1)
            y = randint(0, height - 1)
            agent_type = choice(["green", "red", "yellow"])
            if agent_type == "green":
                self.grid.place_agent(GreenAgent(self), (x, y))
            elif agent_type == "red":
                self.grid.place_agent(RedAgent(self), (x, y))
            elif agent_type == "yellow":
                self.grid.place_agent(YellowAgent(self), (x, y))
                
    def move_robot(self, agent, pos):
        assert isinstance(agent, Robot)
        self.grid.move_agent(agent, pos)
                
    def get_perception(self, agent):
        return self.grid.get_neighbors(agent.pos, moore=True, include_center=True)

    def do(self, agent, action):
        action.execute(self, agent)

    def step(self):
        self.agents.shuffle_do("step_agent")
        
