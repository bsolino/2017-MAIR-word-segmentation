# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 12:00:53 2017

@author: Breixo
"""
from bigram_utils import line_2_bigrams, split_bigram


# TODO Other segmentation method?

def segment_line_contiguous_probability(bigrams_stats, line, separator, threshold = 0):
    bigram_line = line_2_bigrams(line, separator)
    n_bigrams = len(bigram_line)
    if n_bigrams >= 3:
        segmented_line = bigram_line[0]
        for i in range(1, n_bigrams- 1):
            # TODO? Optimize
            # TODO Refactor variable names
            previous_bigram = bigram_line[i-1]
            current_bigram = bigram_line[i]
            next_bigram = bigram_line[i+1]
            
            prob_previous = bigrams_stats.get(previous_bigram, 0)
            prob_current = bigrams_stats.get(current_bigram, 0)
            prob_next = bigrams_stats.get(next_bigram, 0)
            
            second_part = split_bigram(current_bigram, separator)[1]
            
            if ((prob_current < prob_previous and prob_current < prob_next)
                    or (prob_current < threshold)):
                # Add separation between words
                segmented_line += " "
                segmented_line += second_part
            else:
                segmented_line += separator + second_part
            
            if i == n_bigrams-2:
                # Last item
                second_part = split_bigram(next_bigram, separator)[1]
                segmented_line += separator + second_part
        return segmented_line
    else:
        # This method can't segment with less than 3 bigrams
        return line

def segment_line_threshold(bigrams_stats, line, separator, threshold = 0.02):
    bigram_line = line_2_bigrams(line, separator)
    n_bigrams = len(bigram_line)
    if n_bigrams >= 3:
        segmented_line = bigram_line[0]
        for i in range(1, n_bigrams):
            # TODO? Optimize
            # TODO Refactor variable names
            #previous_bigram = bigram_line[i-1]
            current_bigram = bigram_line[i]
            #next_bigram = bigram_line[i+1]
            
            # TODO Other default probability?
            #prob_previous = bigrams_stats.get(previous_bigram, 0)
            prob_current = bigrams_stats.get(current_bigram, 0)
            #prob_next = bigrams_stats.get(next_bigram, 0)
            
            second_part = split_bigram(current_bigram, separator)[1]
            
            #if prob_current < prob_previous and prob_current < prob_next:
            if prob_current < threshold:
                # Add separation between words
                segmented_line += " "
                segmented_line += second_part
            else:
                segmented_line += separator + second_part
            
            #if i == n_bigrams-2:
                # Last item
                #second_part = split_bigram(next_bigram, separator)[1]
                #segmented_line += separator + second_part
        return segmented_line
    else:
        # This method can't segment with less than 3 bigrams
        return line
