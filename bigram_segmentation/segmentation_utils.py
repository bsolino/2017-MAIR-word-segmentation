# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 12:00:53 2017

@author: Breixo
"""
from bigram_utils import line_2_bigrams, split_bigram

def segment_line(bigrams_stats, line):
    #TODO Extend to other bigram types
    bigram_line = line_2_bigrams(line)
    n_bigrams = len(bigram_line)
    if n_bigrams >= 3:
        segmented_line = []
        current_item = bigram_line[0]
        for i in range(1, n_bigrams- 1):
            # TODO? Optimize
            # TODO Refactor variable names
            previous_bigram = bigram_line[i-1]
            current_bigram = bigram_line[i]
            next_bigram = bigram_line[i+1]
            
            # TODO Other default probability?
            prob_previous = bigrams_stats.get(previous_bigram, 0)
            prob_current = bigrams_stats.get(current_bigram, 0)
            prob_next = bigrams_stats.get(next_bigram, 0)
            
            second_part = split_bigram(current_bigram)[1]
            
            if prob_current < prob_previous and prob_current < prob_next:
                # Split the bigram in two and create a new item
                segmented_line.append(current_item)
                current_item = second_part
            else:
                current_item = current_item + second_part
            
            if i == n_bigrams-2:
                # Last item
                second_part = split_bigram(next_bigram)[1]
                current_item = current_item + second_part
                segmented_line.append(current_item)
        return segmented_line
    else:
        # This method can't segment with less than 3 bigrams
        return [line]