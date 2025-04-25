# Group 9
# Bodart Thomas and Jacquemin Gaétan
# Created March 11
import random as rd
from typing import Callable

from agents import GreenAgent, RedAgent, Robot, YellowAgent
from mesa import DataCollector, Model
from mesa.space import MultiGrid, PropertyLayer
from objects import Radioactivity, Waste, WasteDisposalZone
from datetime import datetime
import os

import logging

logger = logging.getLogger("mon_logger")


class RobotMission(Model):
    def __init__(
        self,
        n_green_robots: int = 1,
        n_yellow_robots: int = 1,
        n_red_robots: int = 1,
        n_green_wastes: int = 5,
        n_yellow_wastes: int = 3,
        n_red_wastes: int = 2,
        width: int = 9,
        height: int = 9,
        moore: bool = False,
        seed=None,
    ):
        super().__init__(seed=seed)
        rd.seed(seed)
        
        radiactivity_layer = PropertyLayer("radioactivity",width,height,default_value=0.)

        self.grid = MultiGrid(width, height, moore, property_layers=[radiactivity_layer])
        self.width = width
        self.height = height
        self.moore = moore
        self._is_running = True
        
        self.launch_time_stamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        data_path = os.path.join(os.path.dirname(__file__),"data")
        self.data_filename = os.path.join(data_path,f"{self.launch_time_stamp}_datadump.csv")

        self.datacollector = DataCollector(
            agent_reporters={"fuel": "fuel"},
            model_reporters={
                "green_wastes": lambda m: len(
                    [
                        agent
                        for agent in m.agents_by_type[Waste]
                        if agent.color == "green"
                    ]
                ),
                "yellow_wastes": lambda m: len(
                    [
                        agent
                        for agent in m.agents_by_type[Waste]
                        if agent.color == "yellow"
                    ]
                ),
                "red_wastes": lambda m: len(
                    [agent for agent in m.agents_by_type[Waste] if agent.color == "red"]
                ),
                "total_wastes": lambda m: len(
                    [agent for agent in m.agents_by_type[Waste]]
                ),
                "green_distance": lambda m: sum(
                    [agent.fuel for agent in m.agents_by_type[GreenAgent]]
                ),
                "yellow_distance": lambda m: sum(
                    [agent.fuel for agent in m.agents_by_type[YellowAgent]]
                ),
                "red_distance": lambda m: sum(
                    [agent.fuel for agent in m.agents_by_type[RedAgent]]
                ),
                "total_distance": lambda m: sum(
                    [agent.fuel for agent in m.agents if isinstance(agent, Robot)]
                ),
            },
        )

        waste_collector_pos = (self.width - 1, rd.randint(0, self.height - 1))
        self.green_zone = [
            (x, y) for x in range(0, self.width // 3) for y in range(self.height)
        ]
        self.yellow_zone = [
            (x, y)
            for x in range(self.width // 3, 2 * self.width // 3)
            for y in range(self.height)
        ]
        self.red_zone = [
            (x, y)
            for x in range(2 * self.width // 3, self.width)
            for y in range(self.height)
        ]

        # Create radioactivity zones
        for x in range(self.width):
            for y in range(height):
                zone = (
                    "z1"
                    if (x, y) in self.green_zone
                    else "z2" if (x, y) in self.yellow_zone else "z3"
                )
                if (x, y) == waste_collector_pos:
                    self.grid.place_agent(WasteDisposalZone(self), (x, y))
                
                radiactivity_agent = Radioactivity(zone, self)
                self.grid.place_agent( radiactivity_agent, (x, y))
                self.grid.properties["radioactivity"].set_cell((x,y),radiactivity_agent.radioactivity)

        # Place wastes
        for pos in rd.sample(self.green_zone, n_green_wastes):
            self.grid.place_agent(Waste("green", self), pos)

        for pos in rd.sample(self.yellow_zone, n_yellow_wastes):
            self.grid.place_agent(Waste("yellow", self), pos)

        for pos in rd.sample(self.red_zone, n_red_wastes):
            self.grid.place_agent(Waste("red", self), pos)

        # Place robots
        for pos in rd.sample(self.green_zone, n_green_robots):
            self.grid.place_agent(GreenAgent(self), pos)

        for pos in rd.sample(self.yellow_zone, n_yellow_robots):
            self.grid.place_agent(YellowAgent(self), pos)

        for pos in rd.sample(self.red_zone, n_red_robots):
            self.grid.place_agent(RedAgent(self), pos)


    def try_to_dispose_waste(self, agent):
        assert isinstance(
            agent, WasteDisposalZone
        ), "Selected agent is not a waste disposal zone!"
        for agent_at_pos in self.grid.get_cell_list_contents([agent.pos]):
            if isinstance(agent_at_pos, Waste):
                if agent_at_pos.color == "red":
                    self.grid.remove_agent(agent_at_pos)
                    agent_at_pos.remove()
                    return True
        return False

    def drop_waste(self, agent):
        assert isinstance(agent, Robot), "Selected agent is not a robot!"
        self.grid.place_agent(Waste(agent.dropped_waste_color, self), agent.pos)
        return True  # In the future, it may return False in some cases

    def get_perception(self, agent):
        assert isinstance(agent, Robot), "Selected agent is not a robot!"
        pos_acces = [
            pos
            for pos in self.grid.get_neighborhood(
                agent.pos, self.moore, include_center=True
            )
            if self.is_accessible(pos, agent)
        ]

        green_wastes_pos = []
        yellow_wastes_pos = []
        red_wastes_pos = []
        disposal_zone_pos = []

        for neighbor_agent in self.grid.get_neighbors(agent.pos, self.moore, True):
            if isinstance(neighbor_agent, Waste) and neighbor_agent.color == "green":
                green_wastes_pos.append(neighbor_agent.pos)

            if isinstance(neighbor_agent, Waste) and neighbor_agent.color == "yellow":
                yellow_wastes_pos.append(neighbor_agent.pos)

            if isinstance(neighbor_agent, Waste) and neighbor_agent.color == "red":
                red_wastes_pos.append(neighbor_agent.pos)

            if isinstance(neighbor_agent, WasteDisposalZone):
                disposal_zone_pos.append(neighbor_agent.pos)

        return {
            "pos_access": pos_acces,
            "waste": {
                "green": green_wastes_pos,
                "yellow": yellow_wastes_pos,
                "red": red_wastes_pos,
            },
            "diposal_zone_pos": disposal_zone_pos,
        }

    def do(self, agent, action: Callable):
        """Perform the action on the agent.
        an action is a function that takes the model and the agent as arguments"""
        action(self, agent)
        
    def _is_waste_present(self):
        """Check if there is waste in the grid."""
        if len(self.agents_by_type[Waste]) > 0:
            return True
        return False

    def step(self):
        if not self._is_running:
            return
        if self._is_waste_present():
            self.datacollector.collect(self)
            self.agents.shuffle_do("step_agent")
        else: # save at the end
            self._is_running = False
            self.datacollector.get_model_vars_dataframe().to_csv(self.data_filename)
            
        if self.steps%10 == 0: #save every 10 steps
            self.datacollector.get_model_vars_dataframe().to_csv(self.data_filename)
            
            

    def is_accessible(self, pos, agent):
        i, j = pos
        assert isinstance(agent, Robot), "Selected agent is not a robot!"
        if isinstance(agent, RedAgent):
            return (i, j) in self.green_zone + self.yellow_zone + self.red_zone
        if isinstance(agent, YellowAgent):
            return (i, j) in self.green_zone + self.yellow_zone
        if isinstance(agent, GreenAgent):
            return (i, j) in self.green_zone
