import numpy as np

import constants
import graphing
from FtCalculations import generate_sources, sample_total_Ft
from polyhedron import Polyhedron

# points defining the shapes - here two shapes are defined, a cube and a tetragonal crystal with two pyramidal terminations
xal_pts = np.array([[50, 0, 0], [150, 0, 0], [150, 100, 0], [50, 100, 0],
                    [50, 0, 100], [150, 0, 100], [150, 100, 100], [50, 100, 100], [0, 50, 50], [200, 50, 50]])
xal_inner_pts = np.array([[60, 20, 20], [140, 20, 20], [140, 80, 20], [60, 80, 20],
                          [60, 20, 80], [140, 20, 80], [140, 80, 80], [60, 80, 80], [20, 50, 50], [180, 50, 50]])
cube_pts = np.array([[0, 0, 0], [0, 0, 100], [100, 100, 100], [0, 100, 100], [100, 100, 0], [100, 0, 100], [0, 100, 0],
                     [100, 0, 0]])
cube_inner_pts = np.array([[20, 20, 20], [20, 20, 80], [80, 80, 80], [20, 80, 80], [80, 80, 20], [80, 20, 80],
                           [20, 80, 20], [80, 20, 20]])


# creating the 'crystal' polyhedra
inner_shape = Polyhedron(xal_inner_pts, None, 1)
shape = Polyhedron(xal_pts, inner_shape, 10)

# finding the smallest 'number of sources' with change of 0.1%

def test_precision(total_Ft, total_Ft_1, total_Ft_2, total_Ft_3):
    print(total_Ft, ", ", total_Ft_1, ", ", total_Ft_2, ", ", total_Ft_3)
    if total_Ft_1 and total_Ft_2 and total_Ft_3 is not None:
        print(total_Ft_2, total_Ft_1)
        if abs((total_Ft - total_Ft_1)/ total_Ft) < 0.001 and abs((total_Ft_1 - total_Ft_2)/ total_Ft_1) < 0.001 and\
                abs((total_Ft_2 - total_Ft_3)/total_Ft_2) < 0.001:
            return True
    else:
        return False


total_Ft_cache = {}
total_Ft_cache[0] = None
total_Ft_cache[1] = None
total_Ft_cache[2] = None
total_Ft_cache[3] = None
number_of_sources = 10000
sources = generate_sources(shape, number_of_sources)
n=3
while test_precision(total_Ft_cache[n], total_Ft_cache[n-1], total_Ft_cache[n-2], total_Ft_cache[n-3]) is False:
    number_of_sources += 10000
    sources = generate_sources(shape, number_of_sources)
    total_Ft = sample_total_Ft(shape, sources, shape.max_z)
    total_Ft_cache[n+1] = total_Ft
    n += 1

print(total_Ft_cache[n], total_Ft_cache[n-1], total_Ft_cache[n-2], total_Ft_cache[n-3], len(sources))

"""
# generate a random source spread
sources = generate_sources(shape, constants.number_of_sources)
# plotting the crystal shape with sources
graphing.plot_poly_with_sources(shape, sources)
"""
# calculating Ft for a range of polishing depths
"""
for z_cut_off in np.linspace(shape.min_z, shape.max_z, 51):
    total_Ft = sample_total_Ft(shape, sources, z_cut_off)
    print(z_cut_off, total_Ft)
"""