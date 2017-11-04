# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 12:00:53 2017

@author: Breixo
"""
from bigram_utils import line_2_bigrams, split_bigram
import random

# Returns a line with word boundaries set according to transitional probabilities and a threshold
def segment_line_contiguous_probability(bigrams_stats, bigram_line, separator, threshold = -1):
    n_bigrams = len(bigram_line)
    
    if n_bigrams > 0:
        segmented_line = split_bigram(bigram_line[0], separator)[0]
        for i in range(n_bigrams):
            if i > 0:
                previous_bigram = bigram_line[i - 1]
                prob_previous = bigrams_stats.get(previous_bigram, 0)
            else:
                prob_previous = 1.1 # set the probability high enough so it will be ignored in the if-statement later on
                
            current_bigram = bigram_line[i]
            prob_current = bigrams_stats.get(current_bigram, 0)
            
            if i < n_bigrams-1:
                next_bigram = bigram_line[i + 1]
                prob_next = bigrams_stats.get(next_bigram, 0)
            else:
                prob_next = 1.1
            
            second_part = split_bigram(current_bigram, separator)[1]

            # Split if there is a trough of probability values, or if the current probability is lower than the threshold
            if ((n_bigrams > 1 and prob_current < prob_previous and prob_current < prob_next)
                    or (prob_current <= threshold)):
                segmented_line += " "
                segmented_line += second_part
            else:
                segmented_line += separator + second_part
        return segmented_line
    else:
        return bigram_line

# Returns a line with word boundaries places at random
def segment_random(bigram_line, separator, probability):
    n_bigrams = len(bigram_line)
    segmented_line = split_bigram(bigram_line[0], separator)[0]

    for i in range(n_bigrams):
        current_bigram = bigram_line[i]
        second_part = split_bigram(current_bigram, separator)[1]

        #Split at random
        if random.random() <= probability:
            segmented_line += " "
            segmented_line += second_part
        else:
            segmented_line += separator + second_part
    return segmented_line