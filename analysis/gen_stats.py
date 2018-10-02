#!/usr/bin/env python3

from enum import Enum
import math
import numpy as np
import scipy.stats as stats

# Compare general improvements between penalty function EA, repair function EA,
# and plain-vanilla EA
general_tests_cases = \
    [
        (
            '../output/random_gen/random_gen_validity_enforced_last_best_local_fits.txt',
            '../output/random_gen_bonus/random_gen_validity_enforced_bonus_last_best_local_fits.txt',
            '../output/random_gen_vanilla/random_gen_validity_enforced_vanilla_last_best_local_fits.txt'
        ),
        (
            '../output/website_puzzle/website_puzzle_validity_enforced_last_best_local_fits.txt',
            '../output/website_puzzle_bonus/website_puzzle_validity_enforced_bonus_last_best_local_fits.txt',
            '../output/website_puzzle_vanilla/website_puzzle_validity_enforced_vanilla_last_best_local_fits.txt'
        )
    ]

# Compare uniform random EA vs validity enforced EA
initialization_test_cases = \
    [
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
            '../output/website_puzzle_vanilla/website_puzzle_uniform_random_vanilla_last_best_local_fits.txt'
            '../output/website_puzzle_vanilla/website_puzzle_validity_enforced_vanilla_last_best_local_fits.txt'
        )
    ]

# Compare the penalty function EA w/ multiple penalty coefficients
penalty_test_cases = \
    [
        (
            '../output/website_puzzle/website_puzzle_validity_enforced_small_penalty_last_best_local_fits.txt',
            '../output/website_puzzle/website_puzzle_validity_enforced_last_best_local_fits.txt',
            '../output/website_puzzle/website_puzzle_validity_enforced_large_penalty_last_best_local_fits.txt'
        )
    ]


triplet_coord_pairs = \
    [
        (0, 1),
        (1, 2),
        (0, 2)
    ]


class Assumptions(Enum):
    ASSUME_EQUAL_VARIANCES = 0
    ASSUME_UNEQUAL_VARIANCES = 1


def mean(lst):
    """Computes the mean of lst."""
    return sum(lst) / len(lst)


def var(lst):
    """Computes the variance of lst."""
    return np.var(lst)
    

def std_dev(var):
    """Computes the std. deviation given variance."""
    return math.sqrt(var)
    

def f_test(a, b):
    """Computes the f-test and related information.

    H0: var1 == var2
    H1: var1 != var2

    Returns ASSUME_EQUAL_VARIANCES or
            ASSUME_UNEQUAL_VARIANCES
    """
    # Calculate each mean and variance
    mean_a = mean(a)
    mean_b = mean(b)
    var_a = var(a)
    var_b = var(b)
    std_dev_a = std_dev(var_a)
    std_dev_b = std_dev(var_b)

    # Calculate F critical, placing the largest variance in the 
    # numerator and the smallest in the denominator
    if var_a == 0 or var_b == 0:
        return Assumptions.ASSUME_UNEQUAL_VARIANCES
    else:
        f_crit = max(var_a, var_b) / min(var_a, var_b)

    # Calculate degrees of freedom
    df_a = len(a) - 1
    df_b = len(b) - 1

    # Select alpha, divide by two for the 2-tailed test
    alpha = 0.05 / 2

    # Calculate f-value from a 'table'
    f = stats.f.ppf(q=1-alpha, dfn=df_a, dfd=df_b)

    # Determine the assumption
    if mean_a > mean_b and f < f_crit:
        return Assumptions.ASSUME_EQUAL_VARIANCES

    if mean_a > mean_b and f > f_crit:
        return Assumptions.ASSUME_UNEQUAL_VARIANCES

    if mean_a < mean_b and f > f_crit:
        return Assumptions.ASSUME_EQUAL_VARIANCES

    if mean_a < mean_b and f < f_crit:
        return Assumptions.ASSUME_UNEQUAL_VARIANCES
    
    return None # Error


def t_test(a, b, assumption):
    """Performs the t-test two-sample with assumption provided by the
    assumption parameter.
    """
    if assumption == Assumptions.ASSUME_EQUAL_VARIANCES:
        t_stat, t_crit = stats.ttest_ind(a, b, equal_var=True)

    else: # Assume unequal variances
        t_stat, t_crit = stats.ttest_ind(a, b, equal_var=False)
    
    if abs(t_stat) > abs(t_crit):
        # Reject the null hypothesis that the mean difference is zero
        # Conclude that the variable w/ the better mean represents a better algorithm for this problem
        if var(a) > var(b):
            return a
        if var(a) < var(b):
            return b
        else:
            # Not sure what happens here
            return None
    
    else:
        # Accept the null hypothesis
        # The algorithms are too similar to call a clear winner
        return None


for test_case in general_tests_cases:
    # Open and process the test files
    test_data = []
    for file in test_case:
        output_name = file
        output_name = output_name[output_name.replace('/', '', 2).find('/') + 3:output_name.replace('.', '', 2).find('.') + 1]
        test_data.append(([float(d) for d in open(file, 'r').read().split('\n') if d], output_name))

    for coord_pair in triplet_coord_pairs:
        a_data = test_data[coord_pair[0]][0]
        b_data = test_data[coord_pair[1]][0]

        a_name = test_data[coord_pair[0]][1]
        b_name = test_data[coord_pair[1]][1]

        assumption = f_test(a_data, b_data)
        result = t_test(a_data, b_data, assumption)
        if result == a_data:
            print(a_name + ' is better than ' + b_name)
        elif result == b_data:
            print(b_name + ' is better than ' + a_name)
        else:
            print('Nether ' + b_name + ' nor ' + a_name + ' is better')
