# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 12:00:53 2017

@author: Breixo
"""

# Calculates the percentage of occurrences of each bigram
def calculate_statistics(bigrams):
    total = sum(bigrams.values())
    statistics = {}
    for key, value in bigrams.items():
        statistics[key] = value/total
    return statistics

def segment_line(bigram_stats, line):
    #TODO This also reads the line in bigrams, refactor again?
    #TODO Extend to other bigram types
    if len(line) >= 2:
        old_c = None
        for c in line:
            if old_c != None:
                bigram = old_c + c
                bigram_dict[bigram] = bigram_dict.get(bigram, 0) +1
            old_c = c
        return bigram_dict
    else:
        return line