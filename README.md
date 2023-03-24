# Simulation of eigen mode in type III laser-written waveguide

The project simulates the eigen mode of the single mode waveguide used in [arXiv:2210.10835](https://arxiv.org/abs/2210.10835). The waveguide is composed of constant refractive index core that is surrounded by several ellipsoids with slightly changed refractive index.

The project uses finite-difference time-domain (FDTD) eigen mode solver from [meep](https://meep.readthedocs.io/en/latest/) package.

The project has the following structure:

- Simulation.py is script that defines the geometry of the waveguide and initialize the eigen mode solver.
- Example.ipynb runs the simulation and visualize the resulted field distrubition of the mode. 
