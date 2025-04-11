# Group 9
# Bodart Thomas and Jacquemin Gaétan
# Created March 11


import logging
from random import choice

from mesa import Agent
from objects import Waste
from typing_extensions import Any, Dict, Tuple

logger = logging.getLogger("mon_logger")


########## usefull ###########


def euclidean_distance(pos1, pos2):
    return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5


######### GENERIC ROBOT AGENT CLASS #########


class Robot(Agent):
    def __init__(
        self,
        model,
    ):
        super().__init__(model)
        self.knowledge = {
            "wastes_position": [],
            "last_actions": [],
            "last_positions": [self.pos],
            "is_full": False,
        }
        self.capacity = 2

        self.color = None
        self.collectable_waste_color = None
        self.dropped_waste_color = None
        self.compacting_ratio = 2

        self.waste_in_possession = 0
        self.horizontal_direction = choice([(1, 0), (-1, 0)])
        self.vertical_direction = choice([(0, 1), (0, -1)])
        self.vertical_walk = 0

    def step_agent(self):
        percepts = self.model.get_perception(self)
        self.update_knowledge(percepts)
        action = self.deliberate(self.knowledge)
        self.model.do(self, action)

    def update_knowledge(self, percepts):
        self.is_full()
        self.knowledge["percept"] = percepts
        self.update_special_knowledge()

    def update_special_knowledge(self):
        """pour définir des connaissances spécifiques à chaque type d'agent"""
        pass

    def is_full(self):
        if self.waste_in_possession >= self.capacity:
            self.knowledge["is_full"] = True
        else:
            self.knowledge["is_full"] = False
        return self.knowledge["is_full"]

    def deliberate(self, knowledge: Dict[str, Any]):
        perception = knowledge["percept"]
        if knowledge["is_full"]:
            return self.when_full_behavior()
        if len(perception["waste"][self.collectable_waste_color]) > 0:
            return self.when_seeing_waste_behavior()
        else:
            return self.snake_move()
            # return self.when_random_move()

    def get_last_action(self):
        if len(self.knowledge["last_actions"]) > 0:
            return self.knowledge["last_actions"][-1]
        else:
            return (None, None)

    ### behaviors ###

    def when_random_move(self):
        """return an anction to move randomly in the accessible cases"""
        accessible_cases = self.knowledge["percept"]["pos_access"]
        accessible_cases.remove(self.pos)
        # print(self.pos, accessible_cases)
        case_to_move = choice(accessible_cases)
        logger.debug(
            f"Agent {self.__class__.__name__} is moving randomly to {case_to_move}"
        )
        return MOVE(case_to_move)

    def snake_move(self):
        """Walks as a snake on the accessible positions, and look for wastes"""
        accessible_pos = self.knowledge["percept"]["pos_access"]

        if self.vertical_walk > 0:
            objective_pos = (
                self.pos[0] + self.vertical_direction[0],
                self.pos[1] + self.vertical_direction[1],
            )
            if objective_pos in accessible_pos:
                self.vertical_walk -= 1
                return MOVE(objective_pos)
            else:
                self.vertical_direction = (
                    -self.vertical_direction[0],
                    -self.vertical_direction[1],
                )
                self.vertical_walk = 1
                return self.snake_move()

        else:
            objective_pos = (
                self.pos[0] + self.horizontal_direction[0],
                self.pos[1] + self.horizontal_direction[1],
            )
            if objective_pos in accessible_pos:
                return MOVE(objective_pos)

            else:
                self.horizontal_direction = (
                    -self.horizontal_direction[0],
                    -self.horizontal_direction[1],
                )
                self.vertical_walk = 3
                return self.snake_move()

    def when_seeing_waste_behavior(self):
        perception = self.knowledge["percept"]
        if self.pos in perception["waste"][self.collectable_waste_color]:
            return PICK_WASTE()
        else:
            return MOVE(choice(perception["waste"][self.collectable_waste_color]))

    def when_full_behavior(self):
        assert self.knowledge["is_full"]
        accessible_cases = self.knowledge["percept"]["pos_access"]
        right = self.pos[0] + 1, self.pos[1]
        if right in accessible_cases:
            return MOVE(right)
        else:
            return DROP_WASTE()

    def _get_pos_neighboorhood(self):
        """Get the neighborhood of the agent
        return up, down, left, right"""
        up = self.pos[0], self.pos[1] + 1
        down = self.pos[0], self.pos[1] - 1
        left = self.pos[0] - 1, self.pos[1]
        right = self.pos[0] + 1, self.pos[1]
        return (up, down, left, right)

    def compute_nearest_path_move(self, objective: Tuple[int, int]):
        """Compute the next move to lead to the objective
        For now it is very simple and simply decide to move in a neighboor
        case it it is closer to the objective
        """
        # Compute the next move to lead to the objective
        accessible_cases = self.knowledge["percept"]["pos_access"]
        accessible_cases.remove(self.pos)
        neigboorhood = self._get_pos_neighboorhood()
        current_distance_to_objective = euclidean_distance(self.pos, objective)
        for case in neigboorhood:
            if case in accessible_cases:
                if euclidean_distance(case, objective) < current_distance_to_objective:
                    logger.debug(
                        f"Agent {self.__class__.__name__} is moving towards {objective} to {case}"
                    )
                    return MOVE(case)
        logger.error(f"Agent {self.__class__.__name__} cannot move towards {objective}")
        return MOVE(choice(accessible_cases))


######### SPECIFIC ROBOT AGENT CLASSES ##########


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
        self.compacting_ratio = 1
        self.last_move = None
        self.knowledge["disposal_zones_pos"] = set()

    def when_full_behavior(self):
        assert self.knowledge["is_full"]
        accessible_cases = set(self.knowledge["percept"]["pos_access"])

        if self._has_disposal_zone_in_memory():
            objective = self.get_nearest_disposal_zone()
            if self.pos == objective:  # si il est sur la zone de décharge
                logger.info(
                    f"{self.__class__.__name__} {self.unique_id} is dropping waste at {self.pos}. ({self.waste_in_possession}/{self.capacity})"
                )
                return DROP_WASTE()
            else:
                return self.compute_nearest_path_move(objective)
        else:
            accessible_cases.discard(self.pos)
            accessible_cases.discard(self.knowledge["last_positions"][-1])
            (up, down, left, right) = self._get_pos_neighboorhood()
            for direction in (right, down, up):
                if direction in accessible_cases:
                    logger.debug(
                        f"{self.__class__.__name__} {self.unique_id} is full, looking for a disposal zone, moving to {direction}"
                    )
                    return MOVE(direction)
        logger.error(
            f"Agent {self.__class__.__name__} is full and cannot perform normaly."
        )
        return self.when_random_move()

    def update_special_knowledge(self):
        # mise à jour des positions des zones de décharges
        if len(self.knowledge["percept"]["diposal_zone_pos"]) > 0:
            self.knowledge["disposal_zones_pos"].update(
                set(self.knowledge["percept"]["diposal_zone_pos"])
            )

    def get_nearest_disposal_zone(self):
        """Get the nearest disposal zone position"""
        if len(self.knowledge["disposal_zones_pos"]) > 0:
            return min(
                self.knowledge["disposal_zones_pos"],
                key=lambda x: euclidean_distance(self.pos, x),
            )
        else:
            return None

    def _has_disposal_zone_in_memory(self):
        return len(self.knowledge["disposal_zones_pos"]) > 0


########## ACTIONS ##########

# action are function that take the model and the agent
# as first arguments and call functions or modify attributes on it

# action should then be returned by the deliberate function like that : MOVE(new_pos)


# Decorator for the actions
def action(func):
    """Decorator that handle the other arguments of the action than the model and the agent.
    handles also the Exception and log it if some occur"""

    def wrapper(*args, **kwargs):
        def func2(model, agent):
            try:
                func(model, agent, *args, **kwargs)
            except Exception as e:
                logger.error(f"Error in action {func.__name__}: {e}")
                return False
            return True

        return func2

    return wrapper


@action
def MOVE(model, agent, new_pos):
    """Move the agent to the right"""
    assert new_pos in agent.model.grid.get_neighborhood(
        agent.pos, include_center=True, moore=model.moore
    ), "New position is not in the neighborhood"
    model.grid.move_agent(agent, new_pos)


@action
def DROP_WASTE(model, agent):
    """Drop the waste in the disposal zone"""
    assert isinstance(agent, Robot), "Agent is not a Robot"
    assert agent.waste_in_possession >= agent.compacting_ratio, (
        "Agent does not have enough waste to drop"
    )
    waste_color = agent.dropped_waste_color
    model.grid.place_agent(Waste(color=waste_color, model=model), agent.pos)
    agent.waste_in_possession -= agent.compacting_ratio
    logger.info(
        f"Agent {agent.__class__.__name__} {agent.unique_id} dropped waste at {agent.pos}. ({agent.waste_in_possession}/{agent.capacity})"
    )


@action
def PICK_WASTE(model, agent):
    """Pick the waste in the disposal zone"""
    assert isinstance(agent, Robot), "Agent is not a Robot"
    assert not agent.is_full(), "Agent is full"
    waste_color = agent.collectable_waste_color
    for agent_at_pos in model.grid.get_cell_list_contents([agent.pos]):
        if isinstance(agent_at_pos, Waste) and agent_at_pos.color == waste_color:
            model.grid.remove_agent(agent_at_pos)
            agent.waste_in_possession += 1
            logger.info(
                f"Agent {agent.__class__.__name__} {agent.unique_id} picked up waste at {agent.pos}. ({agent.waste_in_possession}/{agent.capacity})"
            )
            return
    raise ValueError("No waste to pick up in the disposal zone")
