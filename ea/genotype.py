import copy


class Genotype:
    def __init__(self, bulbs=None):
        """Initializes the Genotype class."""
        if bulbs:
            self.bulbs = copy.deepcopy(bulbs)
        else:
            self.bulbs = set([])

        self.fitness = 0.0
