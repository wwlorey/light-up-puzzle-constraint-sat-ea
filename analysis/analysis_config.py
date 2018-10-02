log_file_paths = [
                    'random_gen/random_gen_uniform_random',
                    'random_gen/random_gen_validity_enforced', 
                    'random_gen_bonus/random_gen_uniform_random_bonus',
                    'random_gen_bonus/random_gen_validity_enforced_bonus',
                    'random_gen_vanilla/random_gen_uniform_random_vanilla',
                    'random_gen_vanilla/random_gen_validity_enforced_vanilla',
                    'website_puzzle/website_puzzle_uniform_random', 
                    'website_puzzle/website_puzzle_validity_enforced', 
                    'website_puzzle_bonus/website_puzzle_uniform_random_bonus',
                    'website_puzzle_bonus/website_puzzle_validity_enforced_bonus',
                    'website_puzzle_vanilla/website_puzzle_uniform_random_vanilla',
                    'website_puzzle_vanilla/website_puzzle_validity_enforced_vanilla',
                    'website_puzzle/website_puzzle_validity_enforced_small_penalty',
                    'website_puzzle/website_puzzle_validity_enforced_large_penalty'
                 ]

log_file_paths = ['../output/' + filename + '_log.txt' for filename in log_file_paths]
