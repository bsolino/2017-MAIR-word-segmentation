# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 15:06:16 2017

@author: Breixo
"""
from bigram_utils import find_bigrams, find_syllables, calculate_statistics, clean_line, bigram_probabilities_from_data
from segmentation_utils import segment_line
from file_utils import load_file, divide_data, prepare_training_test_data
from test_utils import compare_lines, test_rates

def print_test_rates(comparison):
    
    rates = test_rates(comparison)
    print("True positive rate (sensitivity): " + str(rates[0]))
    print("False positive rate:              " + str(rates[1]))
    print("True negative rate (specificity): " + str(rates[2]))
    
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

def test1():
    line1 = "peli roca mano roca peli mano peli roca"
    line2 = "pelo roca mano roca pelo mano pelo roca"
    text = [line1, line2]
    
    bigram_appearances = find_bigrams(text[0:1], " ")
    bigram_probabilities = calculate_statistics(bigram_appearances)
    test_comparison = [0, 0, 0, 0]
    for line in text:
        segmented_line = segment_line(bigram_probabilities, clean_line(line, " "), "")
        line_comparison = compare_lines(line, segmented_line)
        
        for i_comparison in range(len(line_comparison)):
            test_comparison[i_comparison] += line_comparison[i_comparison]
        
        print(line)
        print(segmented_line)
        print(line_comparison)
        print_test_rates(line_comparison)
    print(test_comparison)
    print_test_rates(test_comparison)
    
#    peli roca mano roca peli mano peli
#    peli roca mano roca peli mano peli
#    (6, 21, 0, 0)
#    True positive rate (sensitivity): 1.0
#    False positive rate:              0.0
#    True negative rate (specificity): 1.0
#    pelo roca mano roca pelo mano pelo
#    pel oroca mano roca pelomano pelo
#    (4, 20, 1, 2)
#    True positive rate (sensitivity): 0.6666666666666666
#    False positive rate:              0.047619047619047616
#    True negative rate (specificity): 0.9523809523809523
#    [10, 41, 1, 2]
#    True positive rate (sensitivity): 0.8333333333333334
#    False positive rate:              0.023809523809523808
#    True negative rate (specificity): 0.9761904761904762

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

#    test2()
#    [135023, 517946, 126790, 137224]
#    True positive rate (sensitivity): 0.495957714869218
#    False positive rate:              0.19665413440540003
#    True negative rate (specificity): 0.8033458655946

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

def test_no_default_separator():
    line1 = "peli roca mano roca peli mano peli"
    line2 = "pelo roca mano roca pelo mano pelo"
    text = [line1, line2]
    
    separator = ""
    bigram_appearances = find_bigrams(text[0:1], separator)
    bigram_probabilities = calculate_statistics(bigram_appearances)
    test_comparison = [0, 0, 0, 0]
    for line in text:
        segmented_line = segment_line(bigram_probabilities, clean_line(line, separator), separator)
        line_comparison = compare_lines(line, segmented_line)
        
        for i_comparison in range(len(line_comparison)):
            test_comparison[i_comparison] += line_comparison[i_comparison]
        
        print(line)
        print(segmented_line)
        print(line_comparison)
        print_test_rates(line_comparison)
    print(test_comparison)
    print_test_rates(test_comparison)

def test_syllables1():
    line1 = "pe-li ro-ca ma-no ro-ca pe-li ma-no pe-li"
    line2 = "pe-lo ro-ca ma-no ro-ca pe-lo ma-no pe-lo"
    separator = "-"
    boundary = " "
    text = [line1, line2]
    
    bigram_appearances = find_bigrams(text[0:2], separator)
    syllable_appearances = find_syllables(text[0:2], separator)
    bigram_probabilities = calculate_statistics(bigram_appearances, syllable_appearances, separator)
    test_comparison = [0, 0, 0, 0]
    for line in text:
        segmented_line = segment_line(bigram_probabilities, clean_line(line, separator), separator)
        gram_line = line_2_grams_w_boundaries(line, separator, boundary)
        gram_segmented_line = line_2_grams_w_boundaries(segmented_line, separator, boundary)
                
        line_comparison = compare_lines(gram_line, gram_segmented_line)
        for i_comparison in range(len(line_comparison)):
            test_comparison[i_comparison] += line_comparison[i_comparison]
        
        print(line)
        print(segmented_line)
        print(line_comparison)
        print_test_rates(line_comparison)
    print(test_comparison)
    print_test_rates(test_comparison)

# Overfitting test
def test_syllables2():
    route = "../corpus/CGN-NL-50k-utt-syllables.txt"
    text = load_file(route)
    bg_separator = "-"
    boundary = ' '
    
    bigram_probabilities = bigram_probabilities_from_data(text, bg_separator)
    test_comparison = [0, 0, 0, 0]
    for line in text:
        line = line.strip()
        if len(line) < 2:
            continue
        segmented_line = segment_line(bigram_probabilities, clean_line(line, bg_separator), bg_separator)
        gram_line = line_2_grams_w_boundaries(line, bg_separator, boundary)
        gram_segmented_line = line_2_grams_w_boundaries(segmented_line, bg_separator, boundary)
                
        line_comparison = compare_lines(gram_line, gram_segmented_line)
        for i_comparison in range(len(line_comparison)):
            test_comparison[i_comparison] += line_comparison[i_comparison]
        
#        result_line = ""
#        is_first_word = True
#        for word in segmented_line:
#            if not is_first_word:
#                result_line += " "
#            else:
#                is_first_word = False
#            result_line += word
        #print(line)
        #print(segmented_line)
        #print(line_comparison)
    print(test_comparison)
    print_test_rates(test_comparison)

####################################
# Main Method

if __name__ == "__main__":
    #test1()
    #test_no_default_separator()
    #test_syllables1()
    test_syllables2()
    #test2()
    #test3()
    print ("Current state: Segments with syllables (maybe more testing is needed). Hit/miss rate takes syllables as units")