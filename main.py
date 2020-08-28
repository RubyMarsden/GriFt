import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial import ConvexHull, Delaunay
import time

STOPPING_DISTANCE = 20
parent_points_per_dimension = 30
# sphere resolution must be even
sphere_resolution = 30


# 8 points defining the cube corners
xal_pts = np.array([[50, 0, 0], [150, 0, 0], [150, 100, 0], [50, 100, 0],
                [50, 0, 100], [150, 0, 100], [150, 100, 100], [50, 100, 100], [0, 50, 50], [200, 50, 50]])
xal_inner_pts = np.array([[60, 20, 20], [140, 20, 20], [140, 80, 20], [60, 80, 20],
                [60, 20, 80], [140, 20, 80], [140, 80, 80], [60, 80, 80], [20, 50, 50], [180, 50, 50]])
cube_pts = np.array([[0, 0, 0], [0, 0, 100], [100, 100, 100], [0, 100, 100], [100, 100, 0], [100, 0 ,100], [0, 100, 0],
                     [100, 0, 0]])
cube_inner_pts = np.array([[20, 20, 20], [20, 20, 80], [80, 80, 80], [20, 80, 80], [80, 80, 20], [80, 20, 80],
                           [20, 80, 20], [80, 20, 20]])
class Polyhedron:
    def __init__(self, points, inner_shape, concentration):
        self.inner_shape = inner_shape
        self.concentration = concentration

        self.points = points
        self.shape = ConvexHull(points)

    def in_hull(self, p, hull):
        if not isinstance(hull, Delaunay):
            hull = Delaunay(hull)
            return hull.find_simplex(p) >= 0

    def concentration_at_point(self, point):
        if not self.contains_point(point):
            return 0

        if self.inner_shape is not None and self.inner_shape.contains_point(point):
            return self.inner_shape.concentration

        return self.concentration

def sphere_points():
    r = STOPPING_DISTANCE
    points = []
    thetas = np.linspace(0, 2*np.pi, sphere_resolution)
    phis = np.linspace(0, np.pi, sphere_resolution//2)
    for theta in thetas:
        for phi in phis:
            x = r*np.cos(theta)*np.sin(phi)
            y = r*np.sin(theta)*np.sin(phi)
            z = r*np.cos(phi)
            point = np.array([x, y, z])
            points.append(point)
    return points


SPHERE_POINTS = sphere_points()

inner_shape = Polyhedron(cube_inner_pts, None, 1)
shape = Polyhedron(cube_pts, inner_shape, 1)

xs = np.random.rand(100000) * 105
ys = np.random.rand(100000) * 100
zs = np.random.rand(100000) * 100
points = zip(xs, ys, zs)
inside_points = []
in_inside_points =[]
outside_points = []
for point in points:
    if in_hull(point, cube_pts) and in_hull(point, cube_inner_pts):
        in_inside_points.append(point)
    else:
        if in_hull(point, cube_pts):
            inside_points.append(point)
        else:
            outside_points.append(point)
print(len(outside_points))

def plot_things(inside_points, in_inside_points, outside_points, pts, inner_pts, hull, inner_hull):
    ixs, iys, izs = zip(*inside_points)
    oxs, oys, ozs = zip(*in_inside_points)
    bxs, bys, bzs = zip(*outside_points)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    ax.plot(ixs, iys, izs, "bo", markersize=0.3)
    ax.plot(oxs, oys, ozs, "ro", markersize=0.3)
    ax.plot(bxs, bys, bzs, "ko", markersize=0.3)

    # Plot defining corner points
    ax.plot(pts.T[0], pts.T[1], pts.T[2], "ko")
    ax.plot(inner_pts.T[0], inner_pts.T[1], inner_pts.T[2], "ko", markersize=0.5)

    # 12 = 2 * 6 faces are the simplices (2 simplices per square face)
    for s in hull.simplices:
        s = np.append(s, s[0])  # Here we cycle back to the first coordinate
        ax.plot(pts[s, 0], pts[s, 1], pts[s, 2], "r-")

    for s in inner_hull.simplices:
        s = np.append(s, s[0])
        ax.plot(inner_pts[s,0], inner_pts[s, 1], inner_pts[s, 2], "k-")
    # Make axis label
    for i in ["x", "y", "z"]:
        eval("ax.set_{:s}label('{:s}')".format(i, i))

    plt.show()

plot_things(inside_points, in_inside_points, outside_points, cube_pts, cube_inner_pts, hull, inner_hull)
