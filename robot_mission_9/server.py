# Group 9
# Bodart Thomas and Jacquemin Gaétan
# Created March 11

from agents import *
from objects import Radioactivity, Waste, WasteDisposalZone


def agent_portrayal(agent):
    if isinstance(agent, WasteDisposalZone):
        return {
            "color": f"black",
            "marker": "s",
            "size": 1000,
            "alpha": 0.4,
        }

    if isinstance(agent, Radioactivity):
        zone_to_color_mapping = {"z1": "green", "z2": "yellow", "z3": "red"}
        color = zone_to_color_mapping[agent.zone]
        return {
            "color": f"{color}",
            "marker": "s",
            "size": 1000,
            "alpha": 0.1,
        }

    if isinstance(agent, Robot):
        if agent.color == "yellow":
            return {"color": "#FFA07A", "size": 40, "alpha": 1}
        elif agent.color == "red":
            return {"color": "#8B0000", "size": 40, "alpha": 1}
        return {"color": "#006400", "size": 40, "alpha": 1}
    if isinstance(agent, Waste):
        if agent.color == "yellow":
            return {
                "color": "orange",
                "size": 100,
                "alpha": 1,
                "marker": "*",
            }
        return {
            "color": f"{agent.color}",
            "alpha": 1,
            "size": 100,
            "marker": "*",
        }
