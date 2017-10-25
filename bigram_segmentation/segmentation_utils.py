# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 12:00:53 2017

@author: Breixo
"""
from bigram_utils import line_2_bigrams, split_bigram

def segment_line(bigrams_stats, line, separator):
    #TODO Extend to other bigram types
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
            if prob_current < 0.02:
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
