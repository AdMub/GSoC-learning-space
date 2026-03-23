import mesa
import mesa_geo as mg
import numpy as np
import time

class WaterVolume(mesa.Agent):
    """An agent representing a discrete volume of floodwater."""
    def __init__(self, model, initial_pos):
        # ✅ MESA 3.0 UPDATE: unique_id is now handled automatically
        super().__init__(model)
        self.pos = initial_pos
        self.volume = 1.0

    def step(self):
        # 🚨 THE BOTTLENECK: Pure Python neighbor iteration
        # In my GSoC proposal (Pillar 2), this entire block is replaced 
        # by a single vectorized scipy.ndimage.minimum_filter convolution.
        
        raster = self.model.space.layers[0] 
        neighbors = raster.get_neighborhood(self.pos, moore=True)
        
        current_cell = raster.cells[self.pos[0]][self.pos[1]]
        lowest_elevation = current_cell.elevation
        best_move = self.pos

        for neighbor_pos in neighbors:
            # 🚨 THE OBJECT OVERHEAD: Accessing Python objects in a tight loop
            neighbor_cell = raster.cells[neighbor_pos[0]][neighbor_pos[1]]
            if neighbor_cell.elevation < lowest_elevation:
                lowest_elevation = neighbor_cell.elevation
                best_move = neighbor_pos

        # Flow downhill and accumulate risk on the target cell
        if best_move != self.pos:
            self.pos = best_move # Update position directly
            raster.cells[best_move[0]][best_move[1]].flood_risk += self.volume

class TerrainCell(mg.Cell):
    """A raster cell containing topography and risk metrics."""
    def __init__(self, *args, **kwargs):
        # Pass all backend arguments up to the parent Cell class safely
        super().__init__(*args, **kwargs)
        
        # The parent __init__ automatically sets self.indices
        # Generate procedural terrain (higher in top-left, lower in bottom-right)
        self.elevation = (50 - self.rowcol[0]) + (50 - self.rowcol[1]) + np.random.randint(-5, 5)
        self.flood_risk = 0.0

class KinematicFloodModel(mesa.Model):
    """
    A spatial hydrology model demonstrating the computational 
    limitations of object-based RasterLayers in Mesa-Geo.
    """
    def __init__(self, width=200, height=200, rainfall_agents=5000):
        super().__init__()
        self.space = mg.GeoSpace()
        
        # Initialize the heavy object-based RasterLayer
        # Provide dummy geographic bounds and CRS required by newer Mesa-Geo versions
        raster_layer = mg.RasterLayer(
            width=width, 
            height=height, 
            crs="epsg:4326",  # Standard WGS84 coordinate system
            total_bounds=[0, 0, width, height],  # [min_x, min_y, max_x, max_y]
            model=self, 
            cell_cls=TerrainCell
        )
        self.space.add_layer(raster_layer)

        # Spawn rainfall (WaterVolume agents) uniformly across the grid
        for _ in range(rainfall_agents):
            x = self.random.randrange(width)
            y = self.random.randrange(height)
            # Agents are automatically added to the model in Mesa 3.0
            water = WaterVolume(self, (x, y))

        # Collect data to prove we understand Mesa's core lifecycle
        self.datacollector = mesa.DataCollector(
            model_reporters={"Total_System_Risk": self.calculate_total_risk}
        )

    def calculate_total_risk(self):
        # Another O(N) iteration highlighting the need for NumPy .sum() aggregations
        raster = self.space.layers[0]
        return sum(cell.flood_risk for row in raster.cells for cell in row)

    def step(self):
        # ✅ MESA 3.0 "CLEAN SLATE" SCHEDULING
        # Replacing the deprecated RandomActivation with the new AgentSet API
        self.agents.shuffle_do("step")
        self.datacollector.collect(self)

if __name__ == "__main__":
    print("🌊 Initializing Kinematic Flood Routing Model...")
    model = KinematicFloodModel(width=200, height=200, rainfall_agents=5000)
    
    start_time = time.time()
    
    print("⏳ Running 20 simulation steps (Watch the CPU lag...)")
    for i in range(20):
        model.step()
        
    end_time = time.time()
    df = model.datacollector.get_model_vars_dataframe()
    
    print(f"✅ Simulation complete in {end_time - start_time:.2f} seconds.")
    print(f"📊 Final System Risk Score: {df.iloc[-1]['Total_System_Risk']}")
    print("\n💡 Conclusion: The iteration overhead is immense. A Flyweight NumPy refactor will execute this instantly.")