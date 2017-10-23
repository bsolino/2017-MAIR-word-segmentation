# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 15:06:16 2017

@author: Breixo
"""
from bigram_utils import find_bigrams, calculate_statistics, clean_line, bigram_probabilities_from_data
from segmentation_utils import segment_line
from file_utils import load_file, divide_data, prepare_training_test_data
from test_utils import compare_lines, test_rates

def print_test_rates(comparison):
    
    rates = test_rates(comparison)
    print("True positive rate (sensitivity): " + rates[0])
    print("False positive rate:              " + rates[1])
    print("True negative rate (specificity): " + rates[2])

def test1():
    line1 = "peli roca mano roca peli mano peli"
    line2 = "pelo roca mano roca pelo mano pelo"
    text = [line1, line2]
    
    bigram_appearances = find_bigrams(text[0:1])
    bigram_probabilities = calculate_statistics(bigram_appearances)
    test_comparison = [0, 0, 0, 0]
    for line in text:
        segmented_line = segment_line(bigram_probabilities, clean_line(line))
        line_comparison = compare_lines(line, segmented_line)
        
        for i_comparison in range(len(line_comparison)):
            test_comparison[i_comparison] += line_comparison[i_comparison]
        
        print(line)
        print(segmented_line)
        print(line_comparison)
        print_test_rates(line_comparison)
    print(test_comparison)
    print_test_rates(test_comparison)

# Overfitting test
def test2():
    route = "../corpus/CGN-NL-50k-utt.txt"
    text = load_file(route)
    bigram_probabilities = bigram_probabilities_from_data(text)
    test_comparison = [0, 0, 0, 0]
    for line in text:
        line = line.strip()
        if len(line) < 3:
            continue
        segmented_line = segment_line(bigram_probabilities, clean_line(line))
#        result_line = ""
#        is_first_word = True
#        for word in segmented_line:
#            if not is_first_word:
#                result_line += " "
#            else:
#                is_first_word = False
#            result_line += word
        line_comparison = compare_lines(line, segmented_line)
        for i_comparison in range(len(line_comparison)):
            test_comparison[i_comparison] += line_comparison[i_comparison]
#        print(line)
#        print(segmented_line)
#        print(line_comparison)
    print(test_comparison)
    print_test_rates(test_comparison)

    
    
def test3():
    route = "../corpus/CGN-NL-50k-utt.txt"
    text = load_file(route)
    randomize = True

    full_comparison = [0, 0, 0, 0]

    divided_data = divide_data(text, randomize)
    for i in range(len(divided_data)):
        training_data, test_data = prepare_training_test_data(divided_data, i)
    #    training_data, test_data = prepare_training_test_data(divided_data, 0)
        bigram_probabilities = bigram_probabilities_from_data(training_data)
        test_comparison = [0, 0, 0, 0]
        for line in test_data:
            line = line.strip()
            if len(line) < 3:
                continue
            segmented_line = segment_line(bigram_probabilities, clean_line(line))
            line_comparison = compare_lines(line, segmented_line)
            for i_comparison in range(len(line_comparison)):
                test_comparison[i_comparison] += line_comparison[i_comparison]
#            print(line)
#            print(segmented_line)
#            print(line_comparison)
        print("\nTEST " + str(i+1))
        print(test_comparison)
        print_test_rates(test_comparison)
        for i_comparison in range(len(test_comparison)):
            full_comparison[i_comparison] += test_comparison[i_comparison]
    print ("\nFULL TEST")
    print (full_comparison)
    print_test_rates(full_comparison)
    

    
#test1()
#test2()
#test3()