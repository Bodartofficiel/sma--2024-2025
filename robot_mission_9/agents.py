# Group 9
# Bodart Thomas and Jacquemin Gaétan
# Created March 11

from collections import defaultdict
from typing import Literal

from mesa import Agent, Model
from random import choice
from enum import Enum

#### actions ####

class ACTION(Enum):
    MOVE = "move"
    COLLECT = "collect"
    DROP = "drop"
    
class MOVEMENT(Enum):
    UP = (0,1)
    DOWN = (0,-1)
    LEFT = (-1,0)
    RIGHT = (1,0)

def compute_new_position(pos, movement):
    return pos[0] + movement.value[0], pos[1] + movement.value[1]

class Robot(Agent):
    
    def __init__(
        self,
        model,
    ):
        super().__init__(model)
        self.knowledge = {}
        self.capacity = 2
        
        self.color = None
        self.collectable_waste_color = None
        self.dropped_waste_color = None
        
        self.waste_in_possession = 0
        self._is_full = False
        self.last_move = None

    def step_agent(self):
        percepts = self.model.get_perception(self)
        self.update_knowledge(percepts)
        action = self.deliberate()
        self.act(action)
        
    def update_knowledge(self, percepts):
        self.knowledge["percept"] = percepts
    
    def deliberate(self):
        perception = self.knowledge[-1]
        if self._is_full:
            return self.when_full_behavior(self.knowledge)
        if  len(perception["waste"][self.collectable_waste_color]) > 0:
            return self.when_seeing_waste_behavior(self.knowledge)
        else:
            return self.when_random_move(self.knowledge)
        
    def act(self, action):
        match action[0]:
            case ACTION.MOVE: self.move(action[1])
            case ACTION.COLLECT: 
                if self.model.pick_waste(self):
                    self.waste_in_possession += 1
                    if self.waste_in_possession == self.capacity:
                        self._is_full = True
            case ACTION.DROP: 
                assert self._is_full
                if self.model.drop_waste(self):
                    self._is_full = False
                    self.waste_in_possession = 0
                    

        
    ### behaviors ###
        
    def when_random_move(self):
        accessible_cases = self.knowledge["percept"]["pos_access"]
        return (ACTION.MOVE, choice(accessible_cases))
            
    def when_seeing_waste_behavior(self, knowledge):
        perception = knowledge[-1]
        if self.pos in perception["waste"][self.collectable_waste_color]:
            return (ACTION.COLLECT,None)
        else:
            print(perception["waste"][self.collectable_waste_color])
            return (ACTION.MOVE, choice(perception["waste"][self.collectable_waste_color]))
        
    def when_full_behavior(self, knowledge):
        assert self._is_full
        accessible_cases = knowledge[-1]["pos_access"]
        right = compute_new_position(self.pos, MOVEMENT.RIGHT)
        if right in accessible_cases:
            return (ACTION.MOVE, right)
        else:
            return (ACTION.DROP,None)
        
    ### actions ### 

    def move(self, new_pos):
        try :
            # if self.model.is_case_accessible(self, new_pos):
            self.model.grid.move_agent(self, new_pos)
        except Exception as e:
            print(e)
            print("Can't move to this position")
        self.last_move = MOVEMENT((new_pos[0] - self.pos[0], new_pos[1] - self.pos[1]))


class GreenAgent(Robot):
    def __init__(self, model):
        super().__init__(model)
        self.color = "green"
        self.collectable_waste_color = "green"
        self.dropped_waste_color = "yellow"

class YellowAgent(Robot):
    def __init__(self, model):
        super().__init__(model)
        self.color = "yellow"
        self.collectable_waste_color = "yellow"
        self.dropped_waste_color = "red"

class RedAgent(Robot):
    def __init__(self, model):
        super().__init__(model)
        self.color = "red"
        self.collectable_waste_color = "red"
        self.dropped_waste_color = "red"
        self.capacity = 1
        self.last_move = None
        
    def when_full_behavior(self):
        assert self._is_full
        accessible_cases = self.knowledge["perception"]["pos_access"]
        right = compute_new_position(self.pos, MOVEMENT.RIGHT)
        up = compute_new_position(self.pos, MOVEMENT.UP)
        down = compute_new_position(self.pos, MOVEMENT.DOWN)
        if len(self.perception["diposal_zone_pos"]) > 0:
            return (ACTION.MOVE, self.perception["diposal_zone_pos"][0])
        elif right in accessible_cases:
            return (ACTION.MOVE, right)
        elif up in accessible_cases and self.last_move != MOVEMENT.DOWN:
            return (ACTION.MOVE, up)
        elif down in accessible_cases and self.last_move != MOVEMENT.UP:
            return (ACTION.MOVE, down)
