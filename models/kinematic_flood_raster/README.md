# Kinematic Wave Flood Routing (Raster Model)

### What this model does:
This model simulates floodwater propagating across a terrain grid. It uses `Mesa-Geo`'s `RasterLayer` to generate procedural elevation data. `WaterVolume` agents are spawned onto the grid and use iterative neighbor-checking to flow downhill, accumulating `flood_risk` on the cells they traverse. A `DataCollector` tracks the total risk of the system over time.

### What Mesa features it uses:
* `mesa_geo.GeoSpace` and `mesa_geo.RasterLayer` for the spatial environment.
* `mesa_geo.Cell` inheritance to store custom spatial properties (`elevation`, `flood_risk`).
* `mesa.Agent` for the dynamic water entities.
* `mesa.DataCollector` to aggregate system-level metrics.
* `self.agents.shuffle_do("step")` for Mesa 4.0 "Clean Slate" scheduling.

### What I learned & Architectural Observations:
Building this model highlighted exactly why I am proposing to modernize `Mesa-Geo`. 
1. **The Object Overhead:** Instantiating a 200x200 grid creates **40,000 individual `TerrainCell` objects** in memory. If I were to load a real-world GeoTIFF of the Ona River Basin, this object-instantiation approach would crash the script due to RAM exhaustion. 
2. **The Iteration Bottleneck:** In the `WaterVolume.step()` function, checking neighbors requires a pure Python `for` loop, constantly accessing Python objects to read the `.elevation` attribute. As the agent count scales (tested with 5,000 agents), the CPU lag becomes severe.

### What I would do differently (My GSoC Focus):
Writing this code confirmed the necessity of my GSoC proposal. If the `RasterLayer` was backed by a single NumPy `PropertyLayer` (using a Flyweight pattern for the cells), the water agents could find the lowest neighbor instantly using a vectorized `scipy.ndimage.minimum_filter`, bypassing the Python `for` loop entirely and accelerating the simulation by orders of magnitude.