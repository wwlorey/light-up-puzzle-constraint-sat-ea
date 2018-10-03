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


# Compare general improvements between penalty function EA, repair function EA,
# and plain-vanilla EA
test_cases = \
    [
        (
            '../output/random_gen/random_gen_validity_enforced_last_best_local_fits.txt',
            '../output/random_gen_bonus/random_gen_validity_enforced_bonus_last_best_local_fits.txt',
            # '../output/random_gen_vanilla/random_gen_validity_enforced_vanilla_last_best_local_fits.txt'
        ),
        (
            '../output/website_puzzle/website_puzzle_validity_enforced_last_best_local_fits.txt',
            '../output/website_puzzle_bonus/website_puzzle_validity_enforced_bonus_last_best_local_fits.txt',
            # '../output/website_puzzle_vanilla/website_puzzle_validity_enforced_vanilla_last_best_local_fits.txt'
        ),

# Compare uniform random EA vs validity enforced EA
        (
            '../output/random_gen/random_gen_uniform_random_last_best_local_fits.txt',
            '../output/random_gen/random_gen_validity_enforced_last_best_local_fits.txt'
        ),
        (
            '../output/random_gen_bonus/random_gen_uniform_random_bonus_last_best_local_fits.txt',
            '../output/random_gen_bonus/random_gen_validity_enforced_bonus_last_best_local_fits.txt'
        ),
        (
            '../output/random_gen_vanilla/random_gen_uniform_random_vanilla_last_best_local_fits.txt',
            '../output/random_gen_vanilla/random_gen_validity_enforced_vanilla_last_best_local_fits.txt'
        ),
        (
            '../output/website_puzzle/website_puzzle_uniform_random_last_best_local_fits.txt',
            '../output/website_puzzle/website_puzzle_validity_enforced_last_best_local_fits.txt'
        ),
        (
            '../output/website_puzzle_bonus/website_puzzle_uniform_random_bonus_last_best_local_fits.txt',
            '../output/website_puzzle_bonus/website_puzzle_validity_enforced_bonus_last_best_local_fits.txt',
        ),
        (
            '../output/website_puzzle_vanilla/website_puzzle_uniform_random_vanilla_last_best_local_fits.txt',
            '../output/website_puzzle_vanilla/website_puzzle_validity_enforced_vanilla_last_best_local_fits.txt',
        ),

# Compare the penalty function EA w/ multiple penalty coefficients
        (
            '../output/website_puzzle/website_puzzle_validity_enforced_last_best_local_fits.txt',
            '../output/website_puzzle/website_puzzle_validity_enforced_large_penalty_last_best_local_fits.txt'
        ),
        (
            '../output/website_puzzle/website_puzzle_validity_enforced_small_penalty_last_best_local_fits.txt',
            '../output/website_puzzle/website_puzzle_validity_enforced_large_penalty_last_best_local_fits.txt'
        ),
        (
            '../output/website_puzzle/website_puzzle_validity_enforced_small_penalty_last_best_local_fits.txt',
            '../output/website_puzzle/website_puzzle_validity_enforced_last_best_local_fits.txt'
        )
    ]


# t-critical two tailed table for CI = 95% (alpha = 0.05)
# List with index representing df, value representing t-critical
t_table = \
    [
        0,
        0,
        4.3027,
        3.1824,
        2.7765,
        2.5706,
        2.4469,
        2.3646,
        2.3060,
        2.2622,
        2.2281,
        2.2010,
        2.1788,
        2.1604,
        2.1448,
        2.1315,
        2.1199,
        2.1098,
        2.1009,
        2.0930,
        2.0860,
        2.0796,
        2.0739,
        2.0687,
        2.0639,
        2.0595,
        2.0555,
        2.0518,
        2.0484,
        2.0452,
        2.0423,
        2.0395,
        2.0369,
        2.0345,
        2.0322,
        2.0301,
        2.0281,
        2.0262,
        2.0244,
        2.0227,
        2.0211,
        2.0195,
        2.0181,
        2.0167,
        2.0154,
        2.0141,
        2.0129,
        2.0117,
        2.0106,
        2.0096,
        2.0086,
        2.0076,
        2.0066,
        2.0057,
        2.0049,
        2.0040,
        2.0032,
        2.0025,
        2.0017,
        2.0010,
        2.0003,
        1.9996,
        1.9990,
        1.9983,
        1.9977,
        1.9971,
        1.9966,
        1.9960,
        1.9955,
        1.9949,
        1.9944,
        1.9939,
        1.9935,
        1.9930,
        1.9925,
        1.9921,
        1.9917,
        1.9913,
        1.9908,
        1.9905,
        1.9901,
        1.9897,
        1.9893,
        1.9890,
        1.9886,
        1.9883,
        1.9879,
        1.9876,
        1.9873,
        1.9870,
        1.9867,
        1.9864,
        1.9861,
        1.9858,
        1.9855,
        1.9852,
        1.9850,
        1.9847,
        1.9845,
        1.9842,
        1.9840
    ]
