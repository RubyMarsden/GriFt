import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial.qhull import ConvexHull


def plot_poly_with_sources(poly, points):
    points_by_innermost_poly = {poly: [] for poly in poly.all_nested_polygons()}
    for point in points:
        innermost_poly = poly.innermost_poly_at(point)
        points_by_innermost_poly[innermost_poly].append(point)
    _plot_graph(points_by_innermost_poly)

def _plot_graph(points_by_innermost_poly):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    for poly, poly_points in points_by_innermost_poly.items():
        xs, ys, zs = zip(*poly_points)
        ax.plot(xs, ys, zs, "o", markersize=0.3)

        ax.plot(poly.points.T[0], poly.points.T[1], poly.points.T[2], "ko")

        for s in ConvexHull(poly.points).simplices:
            s = np.append(s, s[0])  # Here we cycle back to the first coordinate
            ax.plot(poly.points[s, 0], poly.points[s, 1], poly.points[s, 2], "r-")

    # Make axis label
    for i in ["x", "y", "z"]:
        eval("ax.set_{:s}label('{:s}')".format(i, i))

    plt.show()
