#!/usr/bin/env python3

log_file_paths = ['../output/random_gen_log.txt', '../output/website_puzzle_log.txt', '../output/website_puzzle_log_random_search.txt', '../output/random_gen_log_random_search.txt', '../output/website_puzzle_log_BONUS.txt', '../output/random_gen_log_BONUS.txt']

for i in range(len(log_file_paths)):
    with open(log_file_paths[i], 'r') as log_file:
        # Create a list of lines from the log file, disregarding all config parmeters and empty lines
        log_text = log_file.read().split('\n')
        log_text = [line for line in log_text[log_text.index('Run 1'):] if not line == '']

        last_best_fits = []
        all_best_fits = []
        prev_run_count = 1

        # Scrape average fitness data from the log file
        for line in log_text:
            if line[0] == 'R':
                curr_run_count = int(line.split()[1])
                if not prev_run_count == curr_run_count:
                    last_best_fits.append(all_best_fits[-1])
                    prev_run_count = curr_run_count

            else:
                # This line has eval and fitness data
                line = line.split('\t')

                # Append the average fitness
                all_best_fits.append(line[2])

        last_best_fits.append(all_best_fits[-1])
        
    # Write the last (local) best fitnesses to a file
    with open(log_file_paths[i][:log_file_paths[i].find('.txt')] + '_last_best_local_fits.txt', 'w') as out:
        for fit in last_best_fits:
            out.write(fit + '\n')
