# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 11:24:06 2017

@author: Breixo
"""


# text: Array of lines of the text
# @returns bigrams: Dictionary bigram -> number of occurrences
def find_bigrams(text):
    bigrams = {}
    for line in text:
        line_bigrams = count_bigrams(line)
        update_bigrams(bigrams, line_bigrams)
    return bigrams
    #TODO # Save the db to a file for further use

# Count bigrams in the line, return dictionary bigram -> number of occurrences
def count_bigrams(line):
    #TODO Refactor to a) separate in bigrams, b) count them
    bigram_dict = {}
    bigram_line = line_2_bigrams(line)
    for bigram in bigram_line:
        bigram_dict[bigram] = bigram_dict.get(bigram, 0) +1
    return bigram_dict

# Converts a line in a list of bigrams
def line_2_bigrams(line):
    # TODO Adapt this to other kinds of bigrams
    if len(line) >= 2:
        bigram_list = []
        old_c = None
        for c in line:
            if old_c != None:
                bigram = old_c + c
                bigram_list.append(bigram)
            old_c = c
        return bigram_list
    else:
        return [] #This is not a bigram
    

# Updates the bigram database with the information from a line of text
def update_bigrams(bigrams, line_bigrams):
    for key, update in line_bigrams.items():
#        update = line_bigrams[key]
        current = bigrams.get(key, 0)
        bigrams[key] = current + update
    return bigrams