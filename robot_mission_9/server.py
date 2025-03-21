# Group 9
# Bodart Thomas and Jacquemin Gaétan
# Created March 11

from agents import *
from objects import Radioactivity, Waste, WasteDisposalZone


def agent_portrayal(agent):
    if isinstance(agent, WasteDisposalZone):
        print("TURLMUTRTR")
        return {"color": f"black", "marker": "s", "size": 1000, "alpha": 0.5}
    if isinstance(agent, Radioactivity):
        zone_to_color_mapping = {"z1": "green", "z2": "yellow", "z3": "red"}
        color = zone_to_color_mapping[agent.zone]
        return {"color": f"{color}", "marker": "s", "size": 1000, "alpha": 0.5}

    if isinstance(agent, Robot):
        return {
            "color": f"{agent.color}",
            "size": 40,
            "alpha": 1,
        }
    if isinstance(agent, Waste):
        return {
            "color": f"{agent.color}",
            "alpha": 1,
            "size": 20,
            "marker": "*",
        }
