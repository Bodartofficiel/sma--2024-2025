# Group 9
# Bodart Thomas and Jacquemin Gaétan
# Created March 11

from collections import defaultdict

from mesa import Agent, Model


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

    @staticmethod
    def update(knowledge, percepts):
        pass

    @staticmethod
    def deliberate(knowledge):
        pass


class GreenAgent(Robot):
    def __init__(self, model):
        super().__init__(model)
        self.color = "green"

    def step_agent(self):
        self.update(self.knowledge, percepts)
        action = self.deliberate(self.knowledge)
        percepts = self.model.do(self, action)

    @staticmethod
    def update(knowledge, percepts):
        pass

    @staticmethod
    def deliberate(knowledge):
        pass


class YellowAgent(Robot):
    def __init__(self, model):
        super().__init__(model)
        self.color = "yellow"

    def step_agent(self):
        self.update(self.knowledge, percepts)
        action = self.deliberate(self.knowledge)
        percepts = self.model.do(self, action)

    @staticmethod
    def update(knowledge, percepts):
        pass

    @staticmethod
    def deliberate(knowledge):
        pass


class RedAgent(Robot):
    def __init__(self, model):
        super().__init__(model)
        self.color = "red"

    def step_agent(self):
        self.update(self.knowledge, percepts)
        action = self.deliberate(self.knowledge)
        percepts = self.model.do(self, action)

    @staticmethod
    def update(knowledge, percepts):
        pass

    @staticmethod
    def deliberate(knowledge):
        pass
