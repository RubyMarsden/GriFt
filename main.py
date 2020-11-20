import numpy as np

import graphing
from FtCalculations import generate_sources, sample_total_Ft
from polyhedron import Polyhedron

### CRYSTAL SPECIFICATIONS ###
# Specify the crystal shapes as a list of 3D points which form a convex polyhedron
# Here two shapes are defined, a cube and a tetragonal crystal with two pyramidal terminations

zircon_pts = np.array([[50, 0, 0], [150, 0, 0], [150, 100, 0], [50, 100, 0],
                    [50, 0, 100], [150, 0, 100], [150, 100, 100], [50, 100, 100], [0, 50, 50], [200, 50, 50]])
zircon_inner_pts = np.array([[60, 20, 20], [140, 20, 20], [140, 80, 20], [60, 80, 20],
                          [60, 20, 80], [140, 20, 80], [140, 80, 80], [60, 80, 80], [20, 50, 50], [180, 50, 50]])
cube_pts = np.array([[0, 0, 0], [0, 0, 100], [100, 100, 100], [0, 100, 100], [100, 100, 0], [100, 0, 100], [0, 100, 0],
                     [100, 0, 0]])
cube_inner_pts = np.array([[20, 20, 20], [20, 20, 80], [80, 80, 80], [20, 80, 80], [80, 80, 20], [80, 20, 80],
                           [20, 80, 20], [80, 20, 20]])

# SPECIFY which shape to use here

xal_pts = zircon_pts
xal_inner_pts = zircon_inner_pts

# SPECIFY the relative concentration of parent isotopes

concentration = 10
inner_concentration = 1

# creating the 'crystal' polyhedra
inner_shape = Polyhedron(points = xal_inner_pts, inner_shape = None, concentration = inner_concentration)
shape = Polyhedron(points = xal_pts, inner_shape = inner_shape, concentration = concentration)

# SPECIFY number of alpha particle sources

number_of_sources = 1000

# generate a random source spread
sources = generate_sources(shape, number_of_sources)

# SPECIFY if plot of shape and sources shown

show_plot = False

if show_plot:
    # plotting the crystal shape with sources
    graphing.plot_poly_with_sources(shape, sources)

# SPECIFY number of steps for z_cut_off values

z_cut_off_resolution = 51

# calculating Ft for a range of polishing depths
print("Calculating...")

for z_cut_off in np.linspace(shape.min_z, shape.max_z, z_cut_off_resolution):
    total_Ft = sample_total_Ft(shape, sources, z_cut_off)
    print("z cut-off", z_cut_off, "Ft value", total_Ft)
