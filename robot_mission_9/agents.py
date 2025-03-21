# Group 9
# Bodart Thomas and Jacquemin Gaétan
# Created March 11

from collections import defaultdict
from typing import Literal

from mesa import Agent, Model
from random import choice
from enum import Enum

#### actions ####

# class Action(Enum):
#     MOVE = 1
#     COLLECT = 3

class MOVE(Enum):
    UP = (0, 1)
    DOWN = (0, -1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class Robot(Agent):
    
    def __init__(
        self,
        model,
    ):
        super().__init__(model)
        self.knowledge = defaultdict(list)
        self.color = None

    def step_agent(self):
        pass
    
    def act(self, action):
        if action[0] in MOVE:
            self.move(action[0].value)
        
    @staticmethod
    def update(knowledge, percepts):
        pass

    @staticmethod
    def deliberate(knowledge):
        pass
            
    def move(self, direction: MOVE):
        new_pos = (self.pos[0] + direction[0], self.pos[1] + direction[1])
        try :
            self.model.grid.move_agent(self, new_pos)
        except Exception as e:
            print(e)
            print("Can't move to this position")
            


class GreenAgent(Robot):
    def __init__(self, model):
        super().__init__(model)
        self.color = "green"

    def step_agent(self):
        percepts = self.model.get_perception(self)
        self.update(self.knowledge, percepts)
        action = self.deliberate(self.knowledge)
        self.act(action)
        
    @staticmethod
    def update(knowledge, percepts):
        pass

    @staticmethod
    def deliberate(knowledge):
        """ form of an action : (fct, args) """
        return [choice(list(MOVE))]


class YellowAgent(Robot):
    def __init__(self, model):
        super().__init__(model)
        self.color = "yellow"

    def step_agent(self):
        percepts = self.model.get_perception(self)
        self.update(self.knowledge, percepts)
        action = self.deliberate(self.knowledge)
        self.act(action)

    @staticmethod
    def update(knowledge, percepts):
        pass

    @staticmethod
    def deliberate(knowledge):
        return [choice(list(MOVE))]  


class RedAgent(Robot):
    def __init__(self, model):
        super().__init__(model)
        self.color = "red"

    def step_agent(self):
        percepts = self.model.get_perception(self)
        self.update(self.knowledge, percepts)
        action = self.deliberate(self.knowledge)
        self.act(action)

    @staticmethod
    def update(knowledge, percepts):
        pass

    @staticmethod
    def deliberate(knowledge):
        return [choice(list(MOVE))]
