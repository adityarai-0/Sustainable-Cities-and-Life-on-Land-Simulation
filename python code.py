import random
import math
import csv
import time

class Cell:
    def __init__(self, cell_type="forest", biodiversity=1.0):
        self.type = cell_type
        self.biodiversity = biodiversity
    def update_biodiversity(self, change):
        self.biodiversity += change
        if self.biodiversity < 0.0:
            self.biodiversity = 0.0
        if self.biodiversity > 1.0:
            self.biodiversity = 1.0

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = [[Cell() for _ in range(width)] for _ in range(height)]
    def initialize(self, urban_probability):
        for i in range(self.height):
            for j in range(self.width):
                if random.random() < urban_probability:
                    self.cells[i][j] = Cell("urban", 0.0)
                else:
                    self.cells[i][j] = Cell("forest", 1.0)
    def count_urban_neighbors(self, x, y):
        count = 0
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if i == x and j == y:
                    continue
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.cells[i][j].type == "urban":
                        count += 1
        return count
    def average_biodiversity(self):
        total = 0.0
        cnt = 0
        for row in self.cells:
            for cell in row:
                total += cell.biodiversity
                cnt += 1
        return total / cnt if cnt > 0 else 0.0
    def update_grid(self, urban_expand_prob, forest_recovery_prob):
        new_cells = [[Cell() for _ in range(self.width)] for _ in range(self.height)]
        for i in range(self.height):
            for j in range(self.width):
                cell = self.cells[i][j]
                urban_neighbors = self.count_urban_neighbors(i, j)
                new_cell = Cell(cell.type, cell.biodiversity)
                if cell.type == "forest":
                    if urban_neighbors > 0:
                        chance = (urban_neighbors / 8.0) * urban_expand_prob
                        if random.random() < chance:
                            new_cell.type = "urban"
                            new_cell.biodiversity = 0.0
                else:
                    if urban_neighbors < 3:
                        if random.random() < forest_recovery_prob:
                            new_cell.type = "forest"
                            new_cell.biodiversity = 1.0
                new_cells[i][j] = new_cell
        self.cells = new_cells
    def update_biodiversity(self, heat_index, rainfall_impact):
        for i in range(self.height):
            for j in range(self.width):
                cell = self.cells[i][j]
                if cell.type == "forest":
                    change = (rainfall_impact - heat_index * 0.01) * 0.001
                    cell.update_biodiversity(change)

class Policy:
    def __init__(self):
        self.urban_expand_prob = 0.3
        self.forest_recovery_prob = 0.1
    def adjust_policy(self, grid):
        avg = grid.average_biodiversity()
        if avg < 0.5:
            self.urban_expand_prob = 0.2
            self.forest_recovery_prob = 0.2
        else:
            self.urban_expand_prob = 0.3
            self.forest_recovery_prob = 0.1

class Logger:
    def __init__(self, filename):
        self.filename = filename
        self.file = open(filename, "w")
    def log_step(self, step, grid, policy):
        self.file.write("Step {}: AvgBiodiversity = {:.4f}, UrbanProb = {:.2f}, ForestProb = {:.2f}\n".format(
            step, grid.average_biodiversity(), policy.urban_expand_prob, policy.forest_recovery_prob))
    def close(self):
        self.file.close()

class Statistics:
    def __init__(self):
        self.avg_biodiversity_history = []
        self.urban_count_history = []
    def record(self, grid):
        total_biod = 0.0
        urban_count = 0
        for i in range(grid.height):
            for j in range(grid.width):
                total_biod += grid.cells[i][j].biodiversity
                if grid.cells[i][j].type == "urban":
                    urban_count += 1
        self.avg_biodiversity_history.append(total_biod / (grid.width * grid.height))
        self.urban_count_history.append(urban_count)

class EnvironmentalModel:
    def __init__(self):
        self.pollution_level = 0.0
    def update_pollution(self, grid):
        urban_count = 0
        for i in range(grid.height):
            for j in range(grid.width):
                if grid.cells[i][j].type == "urban":
                    urban_count += 1
        self.pollution_level = urban_count / (grid.width * grid.height)
    def compute_air_quality_index(self, grid):
        aq = 100.0 - 50.0 * self.pollution_level
        return aq if aq >= 0 else 0
    def compute_water_quality_index(self, grid):
        wq = 100.0 - 30.0 * self.pollution_level
        return wq if wq >= 0 else 0
    def compute_noise_level(self, grid):
        return 20.0 + 80.0 * self.pollution_level

class UrbanPlanner:
    def __init__(self):
        self.planning_interval = 10
    def rezone(self, grid, policy, current_step):
        if current_step % self.planning_interval == 0:
            urban_cells = 0
            forest_cells = 0
            for i in range(grid.height):
                for j in range(grid.width):
                    if grid.cells[i][j].type == "urban":
                        urban_cells += 1
                    else:
                        forest_cells += 1
            if urban_cells > forest_cells:
                policy.urban_expand_prob = 0.25
                policy.forest_recovery_prob = 0.15
            else:
                policy.urban_expand_prob = 0.35
                policy.forest_recovery_prob = 0.05

class BiodiversityCalculator:
    def compute_diversity_index(self, grid):
        return grid.average_biodiversity() * 100.0
    def compute_species_richness(self, grid):
        richness = 0.0
        for i in range(grid.height):
            for j in range(grid.width):
                if grid.cells[i][j].type == "forest":
                    richness += grid.cells[i][j].biodiversity
        return richness
    def compute_habitat_quality(self, grid):
        quality = 0.0
        for i in range(grid.height):
            for j in range(grid.width):
                if grid.cells[i][j].type == "forest":
                    quality += grid.cells[i][j].biodiversity
                else:
                    quality += 0.2
        return quality / (grid.width * grid.height)

class ResourceManager:
    def __init__(self):
        self.resources = 1000.0
    def allocate_resources(self, grid):
        urban_count = 0
        for i in range(grid.height):
            for j in range(grid.width):
                if grid.cells[i][j].type == "urban":
                    urban_count += 1
        self.resources += urban_count * 0.5
    def invest_in_green_spaces(self, grid):
        for i in range(grid.height):
            for j in range(grid.width):
                if grid.cells[i][j].type == "urban" and random.random() < 0.05:
                    grid.cells[i][j].type = "forest"
                    grid.cells[i][j].biodiversity = 1.0

class DataExporter:
    def export_stats(self, stats):
        with open("stats_export.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Step", "AvgBiodiversity", "UrbanCount"])
            for i in range(len(stats.avg_biodiversity_history)):
                writer.writerow([i, "{:.4f}".format(stats.avg_biodiversity_history[i]), stats.urban_count_history[i]])
    def export_environmental_data(self, env_model, grid):
        with open("env_export.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["AirQuality", "WaterQuality", "NoiseLevel"])
            air = env_model.compute_air_quality_index(grid)
            water = env_model.compute_water_quality_index(grid)
            noise = env_model.compute_noise_level(grid)
            writer.writerow(["{:.2f}".format(air), "{:.2f}".format(water), "{:.2f}".format(noise)])

class ClimateModel:
    def __init__(self):
        self.temperature = 25.0
        self.precipitation = 50.0
    def update_climate(self, grid, step):
        self.temperature = 25.0 + 5.0 * math.sin(step * 0.1)
        self.precipitation = 50.0 + 20.0 * math.cos(step * 0.1)
    def compute_heat_index(self, grid):
        urban_factor = 0.0
        for i in range(grid.height):
            for j in range(grid.width):
                if grid.cells[i][j].type == "urban":
                    urban_factor += 1.0
        urban_factor /= (grid.width * grid.height)
        return self.temperature + urban_factor * 5.0
    def compute_rainfall_impact(self, grid):
        return self.precipitation * 0.1

class RandomEvent:
    def __init__(self):
        self.trigger_forest_fire = False
        self.fire_intensity = 0.0
    def simulate_event(self, grid):
        if random.random() < 0.02:
            self.trigger_forest_fire = True
            self.fire_intensity = random.random()
            for i in range(grid.height):
                for j in range(grid.width):
                    if grid.cells[i][j].type == "forest":
                        if random.random() < self.fire_intensity * 0.5:
                            grid.cells[i][j].type = "urban"
                            grid.cells[i][j].biodiversity = 0.0
        else:
            self.trigger_forest_fire = False
            self.fire_intensity = 0.0

class ExtendedSimulation:
    def __init__(self, width, height, steps, initial_urban_prob, log_filename):
        self.grid = Grid(width, height)
        self.grid.initialize(initial_urban_prob)
        self.policy = Policy()
        self.logger = Logger(log_filename)
        self.stats = Statistics()
        self.steps = steps
        self.env_model = EnvironmentalModel()
        self.planner = UrbanPlanner()
        self.bio_calc = BiodiversityCalculator()
        self.res_manager = ResourceManager()
        self.exporter = DataExporter()
        self.climate_model = ClimateModel()
        self.rand_event = RandomEvent()
    def run(self):
        for step in range(self.steps):
            self.policy.adjust_policy(self.grid)
            self.planner.rezone(self.grid, self.policy, step)
            self.res_manager.allocate_resources(self.grid)
            self.env_model.update_pollution(self.grid)
            self.climate_model.update_climate(self.grid, step)
            self.rand_event.simulate_event(self.grid)
            heat = self.climate_model.compute_heat_index(self.grid)
            rain = self.climate_model.compute_rainfall_impact(self.grid)
            self.grid.update_biodiversity(heat, rain)
            self.grid.update_grid(self.policy.urban_expand_prob, self.policy.forest_recovery_prob)
            self.stats.record(self.grid)
            self.logger.log_step(step, self.grid, self.policy)
            if step % 5 == 0:
                self.res_manager.invest_in_green_spaces(self.grid)
        self.logger.close()
        self.export_results()
    def export_results(self):
        with open("results.txt", "w") as out:
            out.write("Step,AvgBiodiversity,UrbanCount\n")
            for i in range(len(self.stats.avg_biodiversity_history)):
                out.write("{},{:.4f},{}\n".format(i, self.stats.avg_biodiversity_history[i], self.stats.urban_count_history[i]))
        self.exporter.export_stats(self.stats)
        self.exporter.export_environmental_data(self.env_model, self.grid)
        with open("detailed_report.txt", "w") as report:
            report.write("Detailed Report\n")
            report.write("Final Average Biodiversity: {:.4f}\n".format(self.grid.average_biodiversity()))
            report.write("Final Pollution Level: {:.4f}\n".format(self.env_model.pollution_level))
            report.write("Diversity Index: {:.4f}\n".format(self.bio_calc.compute_diversity_index(self.grid)))
            report.write("Species Richness: {:.4f}\n".format(self.bio_calc.compute_species_richness(self.grid)))
            report.write("Habitat Quality: {:.4f}\n".format(self.bio_calc.compute_habitat_quality(self.grid)))

if __name__ == "__main__":
    sim = ExtendedSimulation(50, 50, 100, 0.3, "simulation_log.txt")
    sim.run()
