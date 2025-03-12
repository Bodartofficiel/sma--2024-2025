# Group 9
# Bodart Thomas and Jacquemin Gaétan
# Created March 11

from agents import *
from mesa.visualization import SolaraViz, make_space_component
from model import RobotMission
from server import agent_portrayal

model_params = {
    "n_robots": 5,
    "n_wastes": 5,
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
