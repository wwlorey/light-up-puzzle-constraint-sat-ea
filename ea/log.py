class Log:
    def __init__(self, config, seed, puzzle, overwrite=False):
        """Initializes the Log class.
        
        Where config is a Config object and overwrite determines if the file will be
        appended to or overwritten.
        """

        def write_config_params():
            """Writes all config file parameters to file."""

            random_puzzle_init_keys = set([
                'generate_uniform_random_puzzle',
                'black_square_placement_prob',
                'bulb_placement_prob', 
                'min_random_board_dimension', 
                'max_random_board_dimension', 
                'override_random_board_dimensions', 
                'override_num_rows', 
                'override_num_cols', 
                'black_square_value_weights'
            ])

            special_keys = set([
                'input_file_path',
                'log_file_path',
                'soln_file_path',
                'seed'
            ])


            if int(self.config.settings['generate_uniform_random_puzzle']):
                self.write('Randomly Generated Puzzle')

                for key in random_puzzle_init_keys:
                    self.write(key + ': ' + self.config.settings[key])
                
                self.write()
            
            else:
                self.write('Puzzle Source: ' + self.config.settings["input_file_path"])
                self.write()


            self.write('board size (#cols x #rows): ' + str(self.puzzle.num_cols) + ' x ' + str(self.puzzle.num_rows))
            self.write('seed: ' + str(self.seed.val))


            for key, val in self.config.settings.items():
                if key not in special_keys.union(random_puzzle_init_keys):
                    self.write(key + ': ' + val)

            self.write()            


        self.config = config

        self.file = open(self.config.settings['log_file_path'], 'w' if overwrite else 'a')

        self.seed = seed
        self.puzzle = puzzle

        write_config_params()
        self.write('Result Log')

    
    def write(self, write_string=''):
        """Writes the contents of write_string to file."""
        self.file.write(write_string + '\n')


    def write_run_header(self, run_count):
        """Writes the given run count to file and to the screen."""
        run_header = '\nRun %i' % (run_count)
        self.write(run_header)
        print(run_header)


    def write_run_data(self, eval_count, average_fitness, best_fitness):
        """Writes the given run data to file and to the screen."""
        run_data = str(eval_count) + '\t' + str(average_fitness) + '\t' + str(best_fitness)
        self.write(run_data)
        print(run_data)
