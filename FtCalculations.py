from constants import *


# this function generates a random spread of 'source particles' in a polyhedron bounding cuboid and then rejects the
# particles outside of the polyhedron
def generate_sources(poly, number_of_sources):
    sources = []
    batch_size = number_of_sources
    while len(sources) < number_of_sources:
        xs = np.random.uniform(poly.min_x, poly.max_x, batch_size)
        ys = np.random.uniform(poly.min_y, poly.max_y, batch_size)
        zs = np.random.uniform(poly.min_z, poly.max_z, batch_size)
        points = [point for point in zip(xs, ys, zs) if poly.contains(point)]
        sources.extend(points)
        batch_size = (number_of_sources - len(sources)) * 2

    return sources[0:number_of_sources]


# this function calculates the Ft for a single 'source particle' as a fraction of the number of particles in the shell
# surrounding the 'source particle' which are inside the polyhedron
def _sample_local_Ft(poly, source_location, z_cut_off):
    local_Ft = 0
    # the following code is commented out - it is a time saving piece of code which only works if the shape being tested
    # has planes in the z axis which are parallel to the z axis (e.g. a cuboid)
    """
    if shape.is_interior(point) and point[2] < z_cut_off - STOPPING_DISTANCE:
    return 1
    """

    if source_location[2] > z_cut_off + STOPPING_DISTANCE:
        return 0
    # the following code tests whether or not it is possible to save information about previous localFts calculated
    # already so they do not need to be calculated again, saving time
    can_cache = source_location[2] < z_cut_off - STOPPING_DISTANCE

    if can_cache:
        value = poly.local_Ft_cache.get(source_location)
        if value is not None:
            return value

    for delta in SPHERE_POINTS:
        alpha_location = source_location + delta
        if poly.contains(alpha_location) and source_location[2] < z_cut_off:
            local_Ft += 1
    local_Ft /= len(SPHERE_POINTS)

    if can_cache:
        poly.local_Ft_cache[source_location] = local_Ft

    return local_Ft


# this function sums the total Ft below the assigned z cut-off value
def sample_total_Ft(poly, sources, z_cut_off):
    total_Ft = 0
    total_sources = 0
    for source in sources:
        concentration = poly.concentration_at_point(source)
        local_Ft = _sample_local_Ft(poly, source, z_cut_off) * concentration
        total_Ft += local_Ft
        if source[2] <= z_cut_off:
            total_sources += concentration
    if total_sources == 0:
        return 0

    Ft = total_Ft / total_sources
    return Ft
