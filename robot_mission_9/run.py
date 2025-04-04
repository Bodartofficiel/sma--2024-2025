# Group 9
# Bodart Thomas and Jacquemin Gaétan
# Created March 11

import random

import numpy as np
from agents import *
from logging_config import configurer_logger
from mesa.visualization import SolaraViz, make_space_component
from model import RobotMission
from server import agent_portrayal

# logger


logger = configurer_logger("mon_logger")

model_params = {
    "n_green_robots": 1,
    "n_yellow_robots": 1,
    "n_red_robots": 1,
    "n_green_wastes": 9,
    "n_yellow_wastes": 3,
    "n_red_wastes": 2,
    "width": 9,
    "height": 9,
}

model = RobotMission(**model_params)


SpaceGraph = make_space_component(agent_portrayal)

# page = SolaraViz(model, components=[SpaceGraph], name="Robot Mission")


if __name__ == "__main__":
    page = SolaraViz(
        model, components=[SpaceGraph], name="Robot Mission", model_params=model_params
    )
    page
