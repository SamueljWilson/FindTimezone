class Polygon:
    def __init__(self, boundary_coords):
        # boundary_coords is a list of [lon, lat] pairs (GeoJSON format)
        self.boundary_coords = boundary_coords

    def is_in_polygon(self, coord):
        # coord = [lat, lon]
        lat, lon = coord[0], coord[1]
        inside = False
        n = len(self.boundary_coords)
        for i in range(n):
            # GeoJSON stores as [lon, lat]
            x1, y1 = self.boundary_coords[i][0], self.boundary_coords[i][1]
            x2, y2 = self.boundary_coords[(i + 1) % n][0], self.boundary_coords[(i + 1) % n][1]
            # Ray casting: shoot ray in +x direction from (lon, lat)
            if ((y1 > lat) != (y2 > lat)) and (lon < (x2 - x1) * (lat - y1) / (y2 - y1) + x1):
                inside = not inside
        return inside