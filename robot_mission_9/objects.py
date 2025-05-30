# Group 9
# Bodart Thomas and Jacquemin Gaétan
# Created March 11

from random import random
from typing import Literal

from mesa import Agent, Model

import logging
logger = logging.getLogger("mon_logger")


class Radioactivity(Agent):
    def __init__(self, zone: Literal["z1", "z2", "z3"], model: Model, *args, **kwargs):
        super().__init__(model, *args, **kwargs)
        zones = ["z1", "z2", "z3"]
        self.zone = zone
        self.radioactivity = (random() + zones.index(self.zone)) / 3
        
    def step_agent(self):
        pass


class WasteDisposalZone(Agent):
    def __init__(self, model: Model, *args, **kwargs):
        super().__init__(model, *args, **kwargs)
        self.zone = "z3"
        self.radioactivity = (2 + random()) / 3
        self.storage = 0
        
    def step_agent(self):
        if self.model.try_to_dispose_waste(self):
            self.storage += 1
            logger.info(f"Waste disposed in zone {self.pos} - Storage: {self.storage}")
            


class Waste(Agent):
    def __init__(
        self, color: Literal["green", "yellow", "red"], model: Model, *args, **kwargs
    ):
        super().__init__(model, *args, **kwargs)
        self.color = color
        
    def step_agent(self):
        pass
