class Ball:
    WIDTH_CM = 7.600

    def __init__(self, location_offset):
        """ Represents a Ball on the game field.

        Arguments:
        location_offset --  A tuple of the offset of the ball from the camera in polar 
                            coordinates where the first element is the distance in 
                            meters and the second element is the angular offset in
                            degrees.
        """
        self.LOCATION = location_offset

    def get_distance(self):
        return self.LOCATION[0]

    def get_heading(self):
        return self.LOCATION[1]
