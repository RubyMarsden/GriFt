from scipy.spatial import Delaunay

class Polyhedron:
    def __init__(self, points, inner_shape, concentration):
        self.inner_shape = inner_shape
        self.concentration = concentration

        self.points = points
        self.shape = Delaunay(points)
        self.min_x, self.min_y, self.min_z, self.max_x, self.max_y, self.max_z = self._get_bounding_box()
        self.local_Ft_cache = {}

    def all_nested_polygons(self):
        all_nested_polygons = [self]
        if self.inner_shape is not None:
            all_nested_polygons.extend(self.inner_shape.all_nested_polygons())
        return all_nested_polygons

    def innermost_poly_at(self, point):
        if not self.contains(point):
            return None

        if self.inner_shape is not None:
            innermost_poly = self.inner_shape.innermost_poly_at(point)
            if innermost_poly is not None:
                return innermost_poly

        return self

    def contains(self, point):
        return self.shape.find_simplex(point) >= 0

    def concentration_at_point(self, point):
        if not self.contains(point):
            return None

        if self.inner_shape is not None:
            concentration = self.inner_shape.concentration_at_point(point)
            if concentration is not None:
                return concentration

        return self.concentration

    def _get_bounding_box(self):
        xs, ys, zs = zip(*self.points)
        min_x, min_y, min_z = min(xs), min(ys), min(zs)
        max_x, max_y, max_z = max(xs), max(ys), max(zs)
        return min_x, min_y, min_z, max_x, max_y, max_z
