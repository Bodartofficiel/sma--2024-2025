# Group 9
# Bodart Thomas and Jacquemin Gaétan
# Created March 11

from matplotlib import pyplot as plt
from agents import *

# logger
from logging_config import configurer_logger
from mesa.visualization import SolaraViz, make_space_component
from model import RobotMission
from server import agent_portrayal

import solara
from matplotlib.figure import Figure

from mesa.visualization.utils import update_counter
from mesa.visualization import SolaraViz, make_plot_component, make_space_component

# logger

from logging_config import configurer_logger

logger = configurer_logger("mon_logger")


default_values = {
    "seed": 42,
    "width": 20,
    "height": 20,
    "n_green_robots": 3,
    "n_yellow_robots": 2,
    "n_red_robots": 1,
    "n_green_wastes": 8,
    "n_yellow_wastes": 4,
    "n_red_wastes": 2,
}

slider_params = {
    "width": {
        "name": "Width of the grid",
        "type": "SliderInt",
        "value": default_values["width"],
        "min": 5,
        "max": 100,
    },
    "height": {
        "name": "Height of the grid",
        "type": "SliderInt",
        "value": default_values["height"],
        "min": 5,
        "max": 100,
    },
    "seed": {
        "name": "Random seed",
        "type": "InputText",
        "value": default_values["seed"],
    },
    "n_green_robots": {
        "name": "Number of green robots",
        "type": "SliderInt",
        "value": default_values["n_green_robots"],
        "min": 1,
        "max": 10,
    },
    "n_yellow_robots": {
        "name": "Number of yellow robots",
        "type": "SliderInt",
        "value": default_values["n_yellow_robots"],
        "min": 1,
        "max": 10,
    },
    "n_red_robots": {
        "name": "Number of red robots",
        "type": "SliderInt",
        "value": default_values["n_red_robots"],
        "min": 1,
        "max": 10,
    },
    "n_green_wastes": {
        "name": "Number of green wastes",
        "type": "SliderInt",
        "value": default_values["n_green_wastes"],
        "min": 1,
        "max": 10,
    },
    "n_yellow_wastes": {
        "name": "Number of red robots",
        "type": "SliderInt",
        "value": default_values["n_yellow_wastes"],
        "min": 1,
        "max": 10,
    },
    "n_red_wastes": {
        "name": "Number of red robots",
        "type": "SliderInt",
        "value": default_values["n_red_wastes"],
        "min": 1,
        "max": 10,
    },
}

# sliders:

model = RobotMission(**default_values)


SpaceGraph = make_space_component(agent_portrayal)



# @solara.component
# def pistance_plot(model: RobotMission):
#     update_counter.get() # This is required to update the counter
#     fig = plt.Figure()
#     ax = fig.subplots()
#     red_data = model.datacollector.get_agenttype_vars_dataframe(RedAgent)
#     print("REDDATA:",red_data)
#     # yellow_data = model.datacollector.get_agenttype_vars_dataframe(YellowAgent)["fuel"].sum()
#     # green_data = model.datacollector.get_agenttype_vars_dataframe(GreenAgent)["fuel"].sum()
    

distance_plot = make_plot_component(
    ["total_distance","yellow_distance", "green_distance","red_distance" ],
)

wastes_plot = make_plot_component(
    [ "total_wastes","yellow_wastes", "green_wastes", "red_wastes" ],
)


# page = SolaraViz(model, components=[SpaceGraph], name="Robot Mission")


if __name__ == "__main__":
    page = SolaraViz(
        model=model,
        components=[SpaceGraph, wastes_plot,distance_plot],
        name="Robot Mission",
        model_params={**slider_params},
    )
    # page
