import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial import ConvexHull, Delaunay

# 8 points defining the cube corners
pts = np.array([[50, 0, 0], [150, 0, 0], [150, 100, 0], [50, 100, 0],
                [50, 0, 100], [150, 0, 100], [150, 100, 100], [50, 100, 100], [0, 50, 50], [200, 50, 50]])
inner_pts = np.array([[60, 20, 20], [140, 20, 20], [140, 80, 20], [60, 80, 20],
                [60, 20, 80], [140, 20, 80], [140, 80, 80], [60, 80, 80], [20, 50, 50], [180, 50, 50]])

hull = ConvexHull(pts)
inner_hull = ConvexHull(inner_pts)

def in_hull(p, hull):
    if not isinstance(hull, Delaunay):
        hull = Delaunay(hull)
        return hull.find_simplex(p) >= 0


xs = np.random.rand(100000) * 200
ys = np.random.rand(100000) * 100
zs = np.random.rand(100000) * 100
points = zip(xs, ys, zs)
inside_points = []
in_inside_points =[]
outside_points = []
for point in points:
    if in_hull(point, pts) and in_hull(point, inner_pts):
        in_inside_points.append(point)
    else:
        if in_hull(point, pts):
            inside_points.append(point)
        else:
            outside_points.append(point)
print(len(outside_points))

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
