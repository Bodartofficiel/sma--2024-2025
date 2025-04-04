# Group 9
# Bodart Thomas and Jacquemin Gaétan
# Created March 11

import logging
from collections import defaultdict
from enum import Enum
from random import choice
from typing import Literal

from mesa import Agent, Model

logger = logging.getLogger("mon_logger")

#### actions ####


class ACTION(Enum):
    MOVE = "move"
    COLLECT = "collect"
    DROP = "drop"
    WAIT = "wait"


class MOVEMENT(Enum):
    UP = (0, 1)
    DOWN = (0, -1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    STILL = (0, 0)


def compute_new_position(pos, movement):
    return pos[0] + movement.value[0], pos[1] + movement.value[1]


def euclidean_distance(pos1, pos2):
    return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5


class Robot(Agent):

    def __init__(
        self,
        model,
    ):
        super().__init__(model)
        self.knowledge = {
            "last_actions": [],
            "last_positions": [self.pos],
            "accessible": set(),
            "inaccessible": set(),
        }
        self.capacity = 2

        self.color = None
        self.collectable_waste_color = None
        self.dropped_waste_color = None

        self.waste_in_possession = 0
        self._is_full = False

        self.current_target_pos = None
        self.know_all_accessible_pos = False

    def step_agent(self):
        percepts = self.model.get_perception(self)
        self.update_knowledge(percepts)
        action = self.deliberate()
        self.act(action)

    def update_knowledge(self, percepts):
        self.knowledge["percept"] = percepts
        self.knowledge["accessible"] = self.knowledge["accessible"].union(
            percepts["pos_access"]
        )
        self.knowledge["inaccessible"] = self.knowledge["inaccessible"].union(
            percepts["pos_inaccess"]
        )
        logger.debug(self.knowledge)
        logger.debug(self.current_target_pos)

        self.update_special_knowledge()

    def update_special_knowledge(self):
        """pour définir des connaissances spécifiques à chaque type d' agent"""
        pass

    def deliberate(self):
        perception = self.knowledge["percept"]
        if self._is_full:
            return self.when_full_behavior()
        if len(perception["waste"][self.collectable_waste_color]) > 0:
            return self.when_seeing_waste_behavior()
        if not self.know_all_accessible_pos:
            return self.when_discover_behavior()
        if self.know_all_accessible_pos:
            return self.look_for_wastes_behavior()

    def act(self, action):
        match action[0]:
            case ACTION.MOVE:
                self.move(action[1])

            case ACTION.COLLECT:
                if self.model.pick_waste(self):
                    self.waste_in_possession += 1
                    logger.info(
                        f"{self.__class__.__name__} {self.unique_id} collected waste at {self.pos}. ({self.waste_in_possession}/{self.capacity})"
                    )
                    if self.waste_in_possession == self.capacity:
                        self._is_full = True
                        logger.info(
                            f"{self.__class__.__name__} {self.unique_id} is now full."
                        )
                else:
                    logger.warning(
                        f"{self.__class__.__name__} {self.unique_id} failed to collect waste at {self.pos}."
                    )

            case ACTION.DROP:
                assert self._is_full
                if self.model.drop_waste(self):
                    self._is_full = False
                    self.waste_in_possession = 0
                    logger.info(
                        f"{self.__class__.__name__} {self.unique_id} dropped waste at {self.pos}."
                    )
                else:
                    logger.warning(
                        f"{self.__class__.__name__} {self.unique_id} failed to drop waste at {self.pos}."
                    )

            case ACTION.WAIT:
                pass
        self.knowledge["last_actions"].append(action)

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
        return (ACTION.MOVE, case_to_move)

    def when_discover_behavior(self):
        known_pos = self.knowledge["accessible"].union(self.knowledge["inaccessible"])
        if self.current_target_pos in known_pos:
            self.current_target_pos = None

        if self.current_target_pos is None:

            target_positions = sorted(
                [
                    a
                    for pos in self.knowledge["accessible"]
                    for a in self.model.grid.get_neighborhood(
                        pos,
                        self.model.moore,
                    )
                    if a not in known_pos
                ],
                key=lambda x: euclidean_distance(x, self.pos),
            )
            if len(target_positions) == 0:
                self.know_all_accessible_pos = True
                return (ACTION.WAIT, None)

            self.current_target_pos = target_positions[0]
        logger.debug(
            f"Agent {self.__class__.__name__} is moving randomly to {self.current_target_pos} using discovery behaviour"
        )
        return self.compute_nearest_path_move(self.current_target_pos)

    def look_for_wastes_behavior(self):
        """Go from bot left to top right"""
        if not self.knowledge["accessible"]:
            return (ACTION.WAIT, None)

        top_border = min(self.knowledge["accessible"], key=lambda x: x[1])[1]
        bot_border = max(self.knowledge["accessible"], key=lambda x: x[1])[1]
        left_border = min(self.knowledge["accessible"], key=lambda x: x[0])[0]
        right_border = max(self.knowledge["accessible"], key=lambda x: x[0])[0]

        if not hasattr(self, "target_dir"):
            self.target_dir = (0, -1)

        if not hasattr(self, "walk_for"):
            self.walk_for = max(self.pos[1] - bot_border, 0)

        if self.walk_for > 0:
            return (
                ACTION.MOVE,
                (self.pos[0] + self.target_dir[0], self.pos[1] + self.target_dir[1]),
            )

    def when_seeing_waste_behavior(self):
        perception = self.knowledge["percept"]
        if self.pos in perception["waste"][self.collectable_waste_color]:
            return (ACTION.COLLECT, None)
        else:
            # print(perception["waste"][self.collectable_waste_color])
            return (
                ACTION.MOVE,
                choice(perception["waste"][self.collectable_waste_color]),
            )

    def when_full_behavior(self):
        assert self._is_full
        accessible_cases = self.knowledge["percept"]["pos_access"]
        right = compute_new_position(self.pos, MOVEMENT.RIGHT)
        if right in accessible_cases:
            return (ACTION.MOVE, right)
        else:
            return (ACTION.DROP, None)

    def _get_pos_neighboorhood(self):
        """Get the neighborhood of the agent
        return up, down, left, right"""
        up = compute_new_position(self.pos, MOVEMENT.UP)
        down = compute_new_position(self.pos, MOVEMENT.DOWN)
        left = compute_new_position(self.pos, MOVEMENT.LEFT)
        right = compute_new_position(self.pos, MOVEMENT.RIGHT)
        return (up, down, left, right)

    def compute_nearest_path_move(self, objective):
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
                    return (ACTION.MOVE, case)
        logger.error(f"Agent {self.__class__.__name__} cannot move towards {objective}")
        return (ACTION.MOVE, choice(accessible_cases))

    ### actions ###

    def move(self, new_pos):
        current_pos = self.pos
        try:
            self.model.grid.move_agent(self, new_pos)
            self.knowledge["last_positions"].append(current_pos)
        except Exception as e:
            logger.error(
                f"Error while moving {self.__class__.__name__} {self.unique_id} from {self.pos} to {new_pos}: {e}"
            )


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
        self.knowledge["disposal_zones_pos"] = set()

    def when_full_behavior(self):

        assert self._is_full
        accessible_cases = set(self.knowledge["percept"]["pos_access"])

        if self._has_disposal_zone_in_memory():
            objective = self.get_nearest_disposal_zone()
            if self.pos == objective:  # si il est sur la zone de décharge
                logger.info(
                    f"{self.__class__.__name__} {self.unique_id} is dropping waste at {self.pos}. ({self.waste_in_possession}/{self.capacity})"
                )
                return (ACTION.DROP, None)
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
                    return (ACTION.MOVE, direction)
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
