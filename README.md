# Mubarak Adisa - Mesa GSoC 2026 Learning Space

Welcome to my learning space for Google Summer of Code 2026. My focus is on **Modernizing Mesa-Geo** by eliminating object overhead in spatial environments and building a high-performance, NumPy-backed Flyweight architecture.

## 🚀 My GSoC Models
This repository contains models built to test Mesa's boundaries and identify architectural bottlenecks:

* [**Kinematic Wave Flood Routing (Raster)**](./models/kinematic_flood_raster)
  * *Purpose:* A spatial hydrology model demonstrating the computational limitations and CPU lag of object-based `RasterLayers` at scale (200x200 grid). 
  * *Takeaway:* Proves the necessity of a vectorized, Pandas-style API and `scipy.ndimage` convolutions for spatial neighbor-checking.

## 🛠️ My Core Mesa Contributions
Alongside building models, I am actively contributing to Mesa-Geo's core architecture:
* **[Merged PR #309]**: Native continuous spatial random sampling (`get_random_xy`) inside raster cells using affine coordinate transformations.
* **[Issue/PR Review #310]**: Architectural audit of the current `RasterLayer` refactor attempt, identifying O(1) object identity loss and bypasses of `mesa.Agent` lifecycle hooks.

---
*My full GSoC 2026 Proposal focuses on Flyweight PropertyLayers, Fluent Aggregation, and SolaraViz Integration.*