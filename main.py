import numpy as np

import constants
import graphing
from FtCalculations import generate_sources, sample_total_Ft
from polyhedron import Polyhedron

# 8 points defining the shapes
xal_pts = np.array([[50, 0, 0], [150, 0, 0], [150, 100, 0], [50, 100, 0],
                    [50, 0, 100], [150, 0, 100], [150, 100, 100], [50, 100, 100], [0, 50, 50], [200, 50, 50]])
xal_inner_pts = np.array([[60, 20, 20], [140, 20, 20], [140, 80, 20], [60, 80, 20],
                          [60, 20, 80], [140, 20, 80], [140, 80, 80], [60, 80, 80], [20, 50, 50], [180, 50, 50]])
cube_pts = np.array([[0, 0, 0], [0, 0, 100], [100, 100, 100], [0, 100, 100], [100, 100, 0], [100, 0, 100], [0, 100, 0],
                     [100, 0, 0]])
cube_inner_pts = np.array([[20, 20, 20], [20, 20, 80], [80, 80, 80], [20, 80, 80], [80, 80, 20], [80, 20, 80],
                           [20, 80, 20], [80, 20, 20]])





inner_shape = Polyhedron(xal_inner_pts, None, 1)
shape = Polyhedron(xal_pts, inner_shape, 10)

sources = generate_sources(shape, constants.number_of_sources)
graphing.plot_poly_with_sources(shape, sources)

for z_cut_off in np.linspace(shape.min_z, shape.max_z, 51):
    total_Ft = sample_total_Ft(shape, sources, z_cut_off)
    print(z_cut_off, total_Ft)
