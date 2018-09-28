#!/usr/bin/env python3

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

log_file_paths = ['../output/random_gen_log.txt', '../output/website_puzzle_log.txt', '../output/website_puzzle_log_BONUS.txt', '../output/random_gen_log_BONUS.txt']

for q in range(len(log_file_paths)):
    with open(log_file_paths[q], 'r') as log_file:
        # Create a list of lines from the log file, disregarding all config parmeters and empty lines
        log_file = log_file.read().split('\n')
        log_file = [line for line in log_file[log_file.index('Run 1'):] if not line == '']


        # key: evaluation number, value: [average fitness, local best fitness]
        eval_dict = {}

        curr_run = 1

        # Scrape data from the log file
        for line in log_file:
            if not line[0] == 'R':
                # This line has eval and fitness data
                eval_num, avg_fit, best_fit = line.split('\t')

                eval_num = int(eval_num)
                avg_fit = float(avg_fit)
                best_fit = float(best_fit)

                if eval_num in eval_dict:
                    eval_dict[eval_num][0] += avg_fit
                    eval_dict[eval_num][1] += best_fit
                    eval_dict[eval_num][2] += 1
                else:
                    eval_dict[eval_num] = [avg_fit, best_fit, 1]

        evals = []
        avg_fits = []
        best_fits = []
        for eval_num in sorted(eval_dict.keys()):
            evals.append(eval_num)
            avg_fits.append(eval_dict[eval_num][0] / eval_dict[eval_num][2])
            best_fits.append(eval_dict[eval_num][1] / eval_dict[eval_num][2])

        # Plot the results
        fig, ax = plt.subplots()

        ax.step(evals, avg_fits, '-r')
        ax.step(evals, best_fits, '-b')

        plt.ylim(0, 1)

        red_patch = mpatches.Patch(color='red', label='Average Local Fitness')
        blue_patch = mpatches.Patch(color='blue', label='Local Best Fitness')
        plt.legend(handles=[blue_patch, red_patch])

        # Include necessary labels
        plt.xlabel('Evaluations')
        plt.ylabel('Fitness\n(ratio of lit white cells to total number of white cells)')


        # Save and close the plot
        plt.savefig(log_file_paths[q][:log_file_paths[q].find('.txt')] + '_graph.png')
        plt.close()
            