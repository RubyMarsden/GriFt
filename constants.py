import numpy as np

STOPPING_DISTANCE = 20
# sphere resolution must be even. Additionally, runtime increases as sphere_resolution^2 because the resolution is used
# to determine how many particles are used when generating a shell of particles at the stopping distance
sphere_resolution = 30


### DEFINING THE SPHERE OF POINTS WHICH REPRESENT A SHELL AROUND A SOURCE AT LENGTH STOPPING DISTANCE ###

def sphere_points():
    r = STOPPING_DISTANCE
    points = []
    thetas = np.linspace(0, 2 * np.pi, sphere_resolution)
    phis = np.linspace(0, np.pi, sphere_resolution // 2)
    for theta in thetas:
        for phi in phis:
            x = r * np.cos(theta) * np.sin(phi)
            y = r * np.sin(theta) * np.sin(phi)
            z = r * np.cos(phi)
            point = np.array([x, y, z])
            points.append(point)
    return points


SPHERE_POINTS = sphere_points()
