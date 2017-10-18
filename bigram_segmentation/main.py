# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 15:06:16 2017

@author: Breixo
"""
from bigram_utils import find_bigrams, calculate_statistics, clean_line
from segmentation_utils import segment_line
from file_utils import load_file


def test1():
    line = "pele roca mano roca pele mano pele"
    line = "pelo roca mano roca pelo mano pelo"
    text = [line]
    
    bigram_appearances = find_bigrams(text)
    bigram_probabilities = calculate_statistics(bigram_appearances)
    for line2 in text:
        print(line.split(" "))
        print(segment_line(bigram_probabilities, clean_line(line2)))
    
def test2():
    training_route = "../../../corpus/CGN-NL-50k-utt.txt"
    test_route = "../../../corpus/corpus_1st_100_lines.txt"
    with open(training_route) as training_text:
        bigram_appearances = find_bigrams(training_text)
        bigram_probabilities = calculate_statistics(bigram_appearances)
    with open(test_route) as test_text: 
        for line in test_text:
            print(line.strip().split(" "))
            print(segment_line(bigram_probabilities, clean_line(line)))
        
test1()
test2()