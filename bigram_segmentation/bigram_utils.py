# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 11:24:06 2017

@author: Breixo
"""

import matplotlib.pyplot as plt

# text: Array of lines of the text
# @returns bigrams: Dictionary bigram -> number of occurrences
def find_bigrams(text, bg_separator):
    bigrams = {}
    for line in text:
        line = clean_line(line, bg_separator)
        line_bigrams = count_bigrams(line, bg_separator)
        update_bigrams(bigrams, line_bigrams)
    return bigrams
    #TODO # Save the db to a file for further use

def find_syllables(text, sb_separator):
    syllables = {}
    for line in text:
        line = clean_line(line, sb_separator)
        line = line_2_syllables(line, sb_separator)
        for sb in line:
            syllables[sb] = syllables.get(sb, 0) + 1
    return syllables

# Count bigrams in the line, return dictionary bigram -> number of occurrences
def count_bigrams(line, bg_separator):
    bigram_dict = {}
    bigram_line = line_2_bigrams(line, bg_separator)
    for bigram in bigram_line:
        bigram_dict[bigram] = bigram_dict.get(bigram, 0) +1
    return bigram_dict

# Converts a line in a list of bigrams
def line_2_bigrams(line, bg_separator):
    if bg_separator != "":
        line = line.split(bg_separator)
        line = [item for item in line if item != ""]
    if len(line) >= 2:
        bigram_list = []
        first_part = line[0]
        for part in line[1:]:
            bigram = first_part + bg_separator + part
            bigram_list.append(bigram)
            first_part = part
        return bigram_list
    else:
        return [] #There are no bigrams

def line_2_syllables(line, sb_separator):
    if sb_separator != "":
        line = line.replace(" ", sb_separator)
        line = line.split(sb_separator)
        line = [item for item in line if item != ""]
        return line
    else:
        return [] #There are no bigrams

def split_bigram(bigram, bg_separator):
    if bg_separator == "":
        return [bigram[0], bigram[1]]
    else:
        if bg_separator in bigram:
            split = bigram.split(bg_separator)
#            split = [gram for gram in split if gram != ""]
            if len(split) == 2 and not "" in split:
                return split
            else:
                print(split)
                raise ValueError("'" + bigram + "' is not a correct bigram separated with '" + bg_separator + "'")
            
        else:
            raise ValueError("Not possible to separate '" + bigram + "' with '" + bg_separator + "'")

# Updates the bigram database with the information from a line of text
def update_bigrams(bigrams, line_bigrams):
    for key, update in line_bigrams.items():
        current = bigrams.get(key, 0)
        bigrams[key] = current + update
    return bigrams

# Calculates the percentage of occurrences of each bigram
def calculate_statistics(bigrams, syllables, separator):
    statistics = {}
    for key, value in bigrams.items():
        syllableCount = syllables[key.split(separator)[0]]
        statistics[key] = value/syllableCount

    #x = []
    #for key, value in statistics.items():
    #    print(value)
    #    x.append(round(value, 4))

    #n, bins, patches = plt.hist(x, 50, normed=1, facecolor='g', alpha=0.75)
    #plt.xlabel('Probability')
    #plt.ylabel('Frequency')
    #plt.title('Probability Distribution')
    #plt.axis([0, 0.1, 0, 40])
    #plt.grid(True)
    #plt.show()
    return statistics

def bigram_probabilities_from_data(data, bg_separator):
    bigram_appearances = find_bigrams(data, bg_separator)
    syllables_appearances = find_syllables(data, bg_separator)
    return calculate_statistics(bigram_appearances, syllables_appearances, bg_separator)

# Removes trailing whitespaces and separators
def clean_line(line, bg_separator):
    clean = line.strip()
    clean = clean.replace(" ", bg_separator)
    return clean