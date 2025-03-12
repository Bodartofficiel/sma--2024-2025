# Multi-Agent System Course
This is a repository for the Multi-Agent System (MAS) project for the academic year 2024-2025. 

## Project Overview

Thanks to the concepts presented in the previous sessions, you now have all the keys in hand to model and simulate your own Agent-based model. In this project, you will model the mission of robots that have to collect dangerous waste, transform it, and then transport it to a secure area. The robots navigate in an environment broken down into several zones where the level of radioactivity varies from low radioactive to highly radioactive. Not all robots have access to all areas.

### Environment

The environment is decomposed into three zones (from west to east):
1. **Zone 1**: Area with low radioactivity, containing a random number of initial (green) waste.
2. **Zone 2**: Area with medium radioactivity.
3. **Zone 3**: The last area with high radioactivity, where completely transformed wastes must be stored.

### Waste Types

We have three different types of waste:
- Green waste
- Yellow waste
- Red waste

### Robot Types

We have three different types of robots:

#### Green Robot
- Walk to pick up 2 initial wastes (i.e., green).
- If in possession of 2 green wastes, then transform them into 1 yellow waste.
- If in possession of 1 yellow waste, transport it further east.
- Green robot cannot exceed Zone 1.

#### Yellow Robot
- Walk to pick up 2 initial yellow wastes.
- If in possession of 2 yellow wastes, then transform them into 1 red waste.
- If in possession of 1 red waste, transport it further east.
- Yellow robot can move in Zones 1 and 2.

#### Red Robot
- Walk to pick up 1 red waste.
- If in possession of 1 red waste, transport it further east to the “waste disposal zone”, where the waste is then “put away”.
- Red robot can move in Zones 1, 2, and 3.

### Implementation Instructions

You have to create a folder named `robot_mission_9`, which will contain different files. Each file should include the number of the group, the date of creation, and the names of the members of the group at the top.
