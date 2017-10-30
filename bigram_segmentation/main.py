# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 15:06:16 2017

@author: Breixo
"""
from bigram_utils import find_bigrams, find_syllables, calculate_absolute_probabilities, calculate_syllable_statistics, clean_line, bigram_absolute_probabilities_from_data, bigram_transitional_probabilities_from_data
from segmentation_utils import segment_line_contiguous_probability, segment_line_threshold, line_2_bigrams
from file_utils import load_file, divide_data, prepare_training_test_data
from test_utils import compare_lines, test_rates

def print_test_rates(comparison):
    
    rates = test_rates(comparison)
    print("True positive rate (sensitivity): " + str(rates[0]))
    print("False positive rate:              " + str(rates[1]))
#    print("True negative rate (specificity): " + str(rates[2]))
    
def line_2_grams_w_boundaries(line, separator, boundary):
    if separator != "":
        line = line.split(separator)
        aux = []
        for item in line:
            if boundary in item:
                split_item = item.split(boundary)
                aux.append(split_item[0])
                for si in split_item[1:]:
                    aux.append(boundary)
                    aux.append(si)
            else:
                aux.append(item)
        line = [item for item in aux if item != ""]
    return line
    
def test(route, threshold, bg_separator, boundary):
    print("\n Route = {0}, Threshold = {1}, bg_separator = '{2}', boundary = '{3}'".format(route, threshold, bg_separator, boundary))
    #route = "../corpus/CGN-NL-50k-utt-syllables.txt"
    text = load_file(route)
    randomize = True

    full_comparison = [0, 0, 0, 0]

    divided_data = divide_data(text, randomize)
    for i in range(len(divided_data)):
        training_data, test_data = prepare_training_test_data(divided_data, i)
    #    training_data, test_data = prepare_training_test_data(divided_data, 0)
        bigram_probabilities = bigram_transitional_probabilities_from_data(training_data, bg_separator)
        test_comparison = [0, 0, 0, 0]
        for line in test_data:
            line = line.strip()
            bigram_line = line_2_bigrams(clean_line(line, bg_separator), bg_separator)
            if len(bigram_line) < 1:
                continue
            segmented_line = segment_line_contiguous_probability(bigram_probabilities, bigram_line, bg_separator, threshold)
            gram_line = line_2_grams_w_boundaries(line, bg_separator, boundary)
            gram_segmented_line = line_2_grams_w_boundaries(segmented_line, bg_separator, boundary)
                    
            line_comparison = compare_lines(gram_line, gram_segmented_line)
            for i_comparison in range(len(line_comparison)):
                test_comparison[i_comparison] += line_comparison[i_comparison]
#            print(line)
#            print(segmented_line)
#            print(line_comparison)

        #print("\nTEST " + str(i+1))
        #print(test_comparison)
        #print_test_rates(test_comparison)

        for i_comparison in range(len(test_comparison)):
            full_comparison[i_comparison] += test_comparison[i_comparison]

    print ("\nFULL TEST")
    print (full_comparison)
    print_test_rates(full_comparison)

####################################
# Main Method

if __name__ == "__main__":
    test("../corpus/CGN-NL-50k-utt.txt", -1, '', ' ') # Test for phonemes & neighbours
    #test("../corpus/CGN-NL-50k-utt.txt", 0.005, '', ' ')  # Test for phonemes & neighbours + threshold
    #test("../corpus/CGN-NL-50k-utt.txt", 0.01, '', ' ')  # Test for phonemes & neighbours + threshold
    #test("../corpus/CGN-NL-50k-utt.txt", 0.012, '', ' ')  # Test for phonemes & neighbours + threshold
    #test("../corpus/CGN-NL-50k-utt.txt", 0.015, '', ' ')  # Test for phonemes & neighbours + threshold
    #test("../corpus/syllabification_30-10.txt", -1, '-', ' ') # Test for syllables & neighbours

    print ("\nCurrent state: Segmentation with sentence boundaries hardcoded in segmentation")