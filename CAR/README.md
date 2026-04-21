# CAR System

This directory is intended for all software and configurations related to the mobile base (CAR) which runs on a separate device from the main animatronics robot (DINO).

## Contents
- `scripts/`: Control scripts for the cart (Python, C++, Arduino, etc.).
- `hardware/`: Wiring diagrams, schematics, and hardware documentation.
- `config/`: Specific configurations or calibration files for the cart.

## Setup Instructions

*(To be added)*

## Wiring Diagrams (WireViz)
We manage hardware wiring diagrams strictly using [WireViz](https://github.com/wireviz/WireViz).

**How to render diagrams:**
1. Install system dependencies: `sudo apt-get install graphviz` (Ubuntu/Raspi) or `brew install graphviz` (Mac)
2. Install WireViz: `python3 -m pip install wireviz`
3. Generate image/html: `~/.local/bin/wireviz hardware/example_wiring.yaml` (Path depends on your pip installation directory).

See `hardware/example_wiring.yaml` as a reference.
