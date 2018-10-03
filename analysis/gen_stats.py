#!/usr/bin/env python3

from enum import Enum
import analysis_config as config
import math
import numpy as np
import scipy.stats as stats


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

    Returns ASSUME_EQUAL_VARIANCES or ASSUME_UNEQUAL_VARIANCES
    """
    # Calculate each mean and variance
    mean_a = mean(a)
    mean_b = mean(b)
    var_a = var(a)
    var_b = var(b)
    std_dev_a = std_dev(var_a)
    std_dev_b = std_dev(var_b)

    # Calculate test statistic
    if var_a == 0 or var_b == 0:
        return Assumptions.ASSUME_UNEQUAL_VARIANCES
    else:
        F = var_a / var_b

    # Calculate degrees of freedom
    df_a = len(a) - 1
    df_b = len(b) - 1

    # Significance level
    alpha = 0.05

    # Calculate F-Critical
    F_crit = stats.f.ppf(alpha, dfn=df_a, dfd=df_b)

    # Print information
    print('mean, ' + str(mean_a) + ', ' + str(mean(b)))
    print('variance, ' + str(var_a) + ', ' + str(var_b))
    print('standard deviation, ' + str(std_dev_a) + ', ' + str(std_dev_b))
    print('observations, ' + str(len(a)) + ', ' + str(len(b)))
    print('df, ' + str(df_a) + ', ' + str(df_b))
    print('F, ' + str(F))
    print('F critical, ' + str(F_crit))

    # Determine the assumption
    if mean_a > mean_b and F < F_crit:
        return Assumptions.ASSUME_EQUAL_VARIANCES

    if mean_a > mean_b and F > F_crit:
        return Assumptions.ASSUME_UNEQUAL_VARIANCES

    if mean_a < mean_b and F > F_crit:
        return Assumptions.ASSUME_EQUAL_VARIANCES

    if mean_a < mean_b and F < F_crit:
        return Assumptions.ASSUME_UNEQUAL_VARIANCES
    
    return None # Error


def t_test(a, b, assumption):
    """Performs the t-test two-sample with assumption provided by the
    assumption parameter.

    Returns the list representing the 'better' algorithm.
    Returns None if neither algorithm can be deemed 'better'.
    """
    # Calculate the t statistic and p two-tail value
    if assumption == Assumptions.ASSUME_EQUAL_VARIANCES:
        t_stat, p = stats.ttest_ind(a, b, equal_var=True)
        df = len(a) + len(b) - 2

    else: # Assume unequal variances
        t_stat, p = stats.ttest_ind(a, b, equal_var=False)
        df = len(a) + 1

    # Calculate the t critical two-tail value
    # Note: an alpha value of 0.05 is assumed
    t_crit = config.t_table[df]

    # Print information
    print('observations, ' + str(len(a)))
    print('df, ' + str(df))
    print('t Stat, ' + str(t_stat))
    print('P two-tail, ' + str(p))
    print('t Critical two-tail, ' + str(t_crit))

    if abs(t_stat) > abs(t_crit):
        # Reject the null hypothesis that the mean difference is zero
        # Conclude that the variable w/ the better mean represents a better algorithm for this problem
        if mean(a) > mean(b):
            return a
        if mean(a) < mean(b):
            return b
        else:
            # Undefined behavior
            return -1
    
    else:
        # Accept the null hypothesis
        # The algorithms are too similar to call a clear winner
        return None


# Perform the statistical comparisons
for test_case in config.test_cases:
    # Open and process the test files
    test_data = []
    for file in test_case:
        output_name = file
        output_name = output_name[output_name.replace('/', ' ', 2).find('/') + 1:output_name.find('_last')]
        test_data.append(([float(d) for d in open(file, 'r').read().split('\n') if d], output_name))
    
    a_data = test_data[0][0]
    b_data = test_data[1][0]

    a_name = test_data[0][1]
    b_name = test_data[1][1]

    print(' ,' + a_name + ', ' + b_name)

    assumption = f_test(a_data, b_data)

    if assumption == Assumptions.ASSUME_EQUAL_VARIANCES:
        print('Equal variances assumed')
    else:
        print('Unequal variances assumed')

    print()

    result = t_test(a_data, b_data, assumption)

    if result == a_data:
        print(a_name + ' is statistically better than ' + b_name)
    elif result == b_data:
        print(b_name + ' is statistically better than ' + a_name)
    else:
        print('Nether ' + b_name + ' nor ' + a_name + ' is statistically better')

    print('\n\n')
    