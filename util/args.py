import sys


class Arguments:
    def __init__(self, num_expected_args, default_values):
        """Initializes the Arguments class."""
        self.num_expected_args = num_expected_args
        self.default_values = default_values
    

    def get_args(self): 
        """Returns the arguments provided by the command line if there are
        num_expected_args (not including the script name).

        Returns default_values otherwise.
        """
        if len(sys.argv) != self.num_expected_args + 1:
            # There are not enough arguments
            # Default to default_values 
            return self.default_values
    
        # Use the provided arguments
        return sys.argv[1:]
