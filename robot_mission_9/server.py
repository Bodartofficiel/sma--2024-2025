# Group 9
# Bodart Thomas and Jacquemin Gaétan
# Created March 11

from agents import *
from objects import Radioactivity, Waste, WasteDisposalZone


def agent_portrayal(agent):
    if isinstance(agent, WasteDisposalZone):
        return {
            "color": f"black",
            "marker": "x",
            "size": 100,
            "alpha": 1,
        }

    if isinstance(agent, Radioactivity):
        zone_to_color_mapping = {"z1": "green", "z2": "yellow", "z3": "red"}
        color = zone_to_color_mapping[agent.zone]
        return {
            "color": "white",
            # "marker": "s",
            "size": 0,
            "alpha": 1,
        }

    if isinstance(agent, Robot):
        if agent.color == "yellow":
            return {"color": "#FFA07A", "size": 35, "alpha": 1}
        elif agent.color == "red":
            return {"color": "#8B0000", "size": 35, "alpha": 1}
        return {"color": "#006400", "size": 35, "alpha": 1}
    if isinstance(agent, Waste):
        if agent.color == "yellow":
            return {
                "color": "orange",
                "size": 60,
                "alpha": 1,
                "marker": "*",
            }
        return {
            "color": f"{agent.color}",
            "alpha": 1,
            "size": 60,
            "marker": "*",
        }