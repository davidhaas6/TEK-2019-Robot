class Cap:
    WIDTH_CM = 24.638

    def __init__(self, top_color, location_offset):
        """ Represents a Cap on the game field.

        Arguments:
        top_color -- The color of side of the cap that's facing up
        location_offset -- A tuple of the offset of the cap from the camera in polar coordinates where 
                           the first element is the distance in meters and the second element is the angular
                           offset in degrees.
        """
        self.TOP_COLOR = top_color
        self.LOCATION = location_offset

    def get_color(self):
        return self.TOP_COLOR

    def get_distance(self):
        return self.LOCATION[0]

    def get_heading(self):
        return self.LOCATION[1]
