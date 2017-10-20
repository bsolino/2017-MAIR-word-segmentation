# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 15:06:16 2017

@author: Breixo
"""
from bigram_utils import find_bigrams, calculate_statistics, clean_line, bigram_probabilities_from_data
from segmentation_utils import segment_line
from file_utils import load_file, divide_data, prepare_training_test_data

def compare_lines(original_line, test_line):
    
    true_positives = 0  # Space in test, space in original
    false_positives = 0 # Space in test, NO space in original
    false_negatives = 0 # NO space in test, space in original
    true_negatives = 0  # NO space in test, NO space in original
    
    j = 0
    for i in range(len(original_line)):
        char_o = original_line[i]
        char_t = test_line[j]
        
        is_sep_o = (char_o == " ")
        is_sep_t = (char_t == " ")
        
        j += 1
        if is_sep_t:
            if is_sep_o:
                true_positives += 1
            else:
                false_positives += 1
                j += 1 # Compensate the extra space
        else:
            if is_sep_o:
                false_negatives += 1
                j -= 1 # Compensate the lack of space
            else:
                true_negatives += 1
#        print(char_o + " == " + char_t + " ? " + str(char_o == char_t)) #TODO REMOVE
    
    return true_positives, true_negatives, false_positives, false_negatives

def test1():
    line = "peli roca mano roca peli mano peli"
    line = "pelo roca mano roca pelo mano pelo"
    text = [line]
    
    bigram_appearances = find_bigrams(text)
    bigram_probabilities = calculate_statistics(bigram_appearances)
    for line2 in text:
        print(line.split(" "))
        print(segment_line(bigram_probabilities, clean_line(line2)))
    
def print_test_rates(comparison):
    tp = comparison[0]
    tn = comparison[1]
    fp = comparison[2]
    fn = comparison[3]
    
    print("True positive rate (sensitivity): " + str(tp / (tp + fn)))
    print("False positive rate:              " + str(fp / (fp + fn)))
    print("True negative rate (specificity): " + str(tn / (fp + tn)))
    
def test2():
    route = "../corpus/CGN-NL-50k-utt.txt"
    text = load_file(route)

    full_comparison = [0, 0, 0, 0]

    divided_data = divide_data(text, False)
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
            result_line = ""
            is_first_word = True
            for word in segmented_line:
                if not is_first_word:
                    result_line += " "
                else:
                    is_first_word = False
                result_line += word
#            print(line)
            #print(result_line)
            line_comparison = compare_lines(line, result_line)
#            print(line_comparison)
            for i_comparison in range(len(line_comparison)):
                test_comparison[i_comparison] += line_comparison[i_comparison]
        print("\nTEST " + str(i+1))
        print(test_comparison)
        print_test_rates(test_comparison)
        for i_comparison in range(len(test_comparison)):
            full_comparison[i_comparison] += test_comparison[i_comparison]
    print ("\nFULL TEST")
    print (full_comparison)
    print_test_rates(full_comparison)
# test1()
test2()