class Coordinate:
    def __init__(self, x, y):
        """Initializes the Coordinate class."""
        self.x = x
        self.y = y


    def __str__(self):
        """Returns an ordered pair in string form."""
        return '(' + str(self.x) + ', ' + str(self.y) + ')'


    def __eq__(self, other):
        """Returns True if the x & y member variables are equal, False otherwise."""
        return self.x == other.x and self.y == other.y


    def __ne__(self, other):
        """Returns True if neither the x nor y member variables are equal, False otherwise."""
        return not self == other


    def __lt__(self, other):
        """Returns True if self is less than other, False otherwise.

        Comparison priority: y then x.
        """
        if self.y == other.y:
            return self.x < other.x

        return self.y < other.y


    def __gt__(self, other):
        """Returns True if self is greater than other, False otherwise.

        Comparison priority: y then x.
        """
        if self.y == other.y:
            return self.x > other.x

        return self.y > other.y


    def __hash__(self):
        """Returns a hash representation of a coordinate."""
        return (self.x + 1) * 100000 + self.y
