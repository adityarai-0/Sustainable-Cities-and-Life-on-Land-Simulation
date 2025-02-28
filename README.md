# Sustainable-Cities-and-Life-on-Land-Simulation
Overview

This project is a Python-based simulation that integrates Sustainable Development Goals (SDG) 11 (Sustainable Cities and Communities) and SDG 15 (Life on Land). The simulation models a 2D grid where each cell represents either an urban area or a forest. Urban expansion, forest recovery, biodiversity dynamics, and environmental factors such as air quality, water quality, and noise level are all simulated over a series of time steps.

Features

Grid-Based Model:
The simulation uses a 2D grid (default 50x50 cells) where each cell can be urban or forest.
Dynamic Policy Adjustments:
Urban expansion and forest recovery probabilities are adjusted dynamically based on the average biodiversity in the grid.
Environmental Modeling:
An environmental model computes air quality, water quality, and noise levels based on the density of urban areas.
Urban Planning:
Periodic zoning changes are simulated to manage the balance between urban and forested areas.
Random Events:
Occasional forest fires are simulated as random events that impact the grid.
Data Export:
The simulation generates several output files including logs, CSV reports, and a detailed final report.
Generated Output Files

After running the simulation, the following files are created:

simulation_log.txt
Logs the details of each simulation step including the average biodiversity and current policy values.
results.txt
A CSV file with step-by-step data of average biodiversity and the number of urban cells.
stats_export.csv
Contains detailed statistical records over the simulation steps.
env_export.csv
Reports environmental metrics such as air quality, water quality, and noise level.
detailed_report.txt
A comprehensive report summarizing the final simulation metrics, including biodiversity, pollution level, diversity index, species richness, and habitat quality.
Requirements

Python 3.x
The simulation is built using Python 3 and only uses standard libraries such as random, math, csv, and time.
How to Run

Clone or Download the Repository:
Download the Python script (e.g., simulation.py) to your local machine.
Open a Terminal:
Navigate to the directory containing the script.
Execute the Script:
Run the following command in your terminal:
python simulation.py
The simulation will run and generate the output files listed above.
Simulation Parameters

Grid Dimensions: 50 x 50 cells
Simulation Steps: 100
Initial Urban Probability: 0.3 (30% chance that a cell starts as urban)
Policy Adjustments: Based on the grid’s average biodiversity
Environmental Metrics: Calculated using urban density to derive air quality, water quality, and noise levels
Random Forest Fires: Approximately a 2% chance per simulation step
Customization

You can customize the simulation by modifying parameters directly in the Python script:

Grid Size: Change the dimensions in the ExtendedSimulation initialization.
Number of Steps: Adjust the number of simulation steps.
Initial Urban Probability: Modify the probability in the grid initialization.
Policy Probabilities: The probabilities for urban expansion and forest recovery can be adjusted within the Policy class.
