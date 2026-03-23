# Motivation

## Who I am
I am Mubarak Adisa, a Civil Engineering graduate (University of Ibadan) and current Computer Science undergraduate (University of the People). My engineering background is rooted in hydraulic modeling, spatial data processing (GIS), and stochastic risk analysis. Recently, I developed `Hydro-Flow CLI`, an AI-augmented terminal tool that utilizes SciPy and NumPy to solve inverse hydraulic design problems and run Monte Carlo flood simulations. 

## Why Mesa
In civil engineering, agent-based modeling (ABM) is critical for simulating dynamic physical systems—like urban sprawl, traffic grids, and flood propagation. I was drawn to Mesa because it represents the perfect intersection of Python accessibility and complex systems simulation. However, coming from a background of processing heavy GeoTIFFs, I noticed that applying ABM to massive geospatial grids often leads to severe CPU bottlenecks or out-of-memory crashes due to object overhead. I want to help bridge that gap.

## What I want to learn
I want to deeply understand the internal mechanics of Mesa. Specifically, I am focused on how Mesa-Core's new `PropertyLayer` architecture interacts with the core event scheduler, and how `Mesa-Geo` currently wraps those concepts. I want to learn exactly where the framework helps modellers, and where the Python object-oriented overhead gets in the way of high-performance spatial analysis.

## Where I want to go
My goal is to lead the modernization of `Mesa-Geo`'s raster data structures for my GSoC 2026 project. I want to contribute a high-performance, NumPy-backed Flyweight architecture (with a vectorized Fluent API) that brings C-level execution speeds to researchers, without sacrificing the intuitive, agent-centric API that makes Mesa so great to use. Ultimately, I want to be a long-term maintainer who helps make Mesa the gold standard for geospatial ABM.