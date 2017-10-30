# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 15:06:16 2017

@author: Breixo
"""
from bigram_utils import find_bigrams, find_syllables, calculate_absolute_probabilities, calculate_syllable_statistics, clean_line, bigram_absolute_probabilities_from_data, bigram_transitional_probabilities_from_data
from segmentation_utils import segment_line_contiguous_probability, segment_line_threshold
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

def test_absolute_phoneme_toy_transitional():
    line1 = "peli rucy mano rucy peli mano peli"
    line2 = "pelo rucy mano rucy pelo mano pelo"
    text = [line1, line2]
    bg_separator = ""
    
    bigram_appearances = find_bigrams(text[0:1], bg_separator)
    unit_appearances = find_syllables(text[0:1], bg_separator)
    bigram_probabilities = calculate_syllable_statistics(bigram_appearances, unit_appearances, bg_separator)
    test_comparison = [0, 0, 0, 0]
    for line in text:
        segmented_line = segment_line_contiguous_probability(bigram_probabilities, clean_line(line, bg_separator), bg_separator)
        line_comparison = compare_lines(line, segmented_line)
        
        for i_comparison in range(len(line_comparison)):
            test_comparison[i_comparison] += line_comparison[i_comparison]
        
        print(line)
        print(segmented_line)
        print(line_comparison)
        print_test_rates(line_comparison)
    print(test_comparison)
    print_test_rates(test_comparison)


# Use this test to check whether it works without assigning a bg_separator
# Default bg_separator are a liability, so I recommend not using this
def test_absolute_default_bg_separator():
    print("Test if it works with default bigram separators")

    line1 = "peli roca mano roca peli mano peli"
    line2 = "pelo roca mano roca pelo mano pelo"
    text = [line1, line2]
    
    bigram_appearances = find_bigrams(text[0:1])
    bigram_probabilities = calculate_absolute_probabilities(bigram_appearances)
    test_comparison = [0, 0, 0, 0]
    for line in text:
        segmented_line = segment_line_contiguous_probability(bigram_probabilities, clean_line(line))
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
def test_absolute_phoneme_overfitting():
    print("Phoneme segmentation, training and testing with whole corpus")
    route = "../corpus/CGN-NL-50k-utt.txt"
    text = load_file(route)
    bg_separator = ""
    bigram_probabilities = bigram_absolute_probabilities_from_data(text, bg_separator)
    test_comparison = [0, 0, 0, 0]
    for line in text:
        line = line.strip()
        if len(line) < 3:
            continue
        segmented_line = segment_line_contiguous_probability(bigram_probabilities, clean_line(line, bg_separator), bg_separator)
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

#    test_absolute_phoneme_overfitting()
#    [135023, 517946, 126790, 137224]
#    True positive rate (sensitivity): 0.495957714869218
#    False positive rate:              0.19665413440540003
#    True negative rate (specificity): 0.8033458655946

    
    
def test_absolute_phoneme_10_fold_cv():
    print("Phoneme segmentation, 10-fold crosss validation whole corpus")
    route = "../corpus/CGN-NL-50k-utt.txt"
    text = load_file(route)
    randomize = True
    bg_separator = ""

    full_comparison = [0, 0, 0, 0]

    divided_data = divide_data(text, randomize)
    for i in range(len(divided_data)):
        training_data, test_data = prepare_training_test_data(divided_data, i)
    #    training_data, test_data = prepare_training_test_data(divided_data, 0)
        bigram_probabilities = bigram_absolute_probabilities_from_data(training_data, bg_separator)
        test_comparison = [0, 0, 0, 0]
        for line in test_data:
            line = line.strip()
            if len(line) < 3:
                continue
            segmented_line = segment_line_contiguous_probability(bigram_probabilities, clean_line(line, bg_separator), bg_separator)
            line_comparison = compare_lines(line, segmented_line)
            for i_comparison in range(len(line_comparison)):
                test_comparison[i_comparison] += line_comparison[i_comparison]
#            print(line)
#            print(segmented_line)
#            print(line_comparison)
# =============================================================================
#         print("\nTEST " + str(i+1))
#         print(test_comparison)
#         print_test_rates(test_comparison)
        for i_comparison in range(len(test_comparison)):
            full_comparison[i_comparison] += test_comparison[i_comparison]
# =============================================================================
    print ("\nFULL TEST")
    print (full_comparison)
    print_test_rates(full_comparison)
    
def test_absolute_phoneme_sentence_10_fold_cv():
    print("Phoneme segmentation (w/ sentence boundaries), 10-fold crosss validation whole corpus")
    route = "../corpus/CGN-NL-50k-utt.txt"
    text = load_file(route)
    randomize = True
    bg_separator = ""

    full_comparison = [0, 0, 0, 0]

    divided_data = divide_data(text, randomize)
    for i in range(len(divided_data)):
        training_data, test_data = prepare_training_test_data(divided_data, i)
    #    training_data, test_data = prepare_training_test_data(divided_data, 0)
        bigram_probabilities = bigram_absolute_probabilities_from_data(training_data, bg_separator)
        test_comparison = [0, 0, 0, 0]
        for line in test_data:
            line = line.strip()
            if len(line) < 3:
                continue
            segmented_line = segment_line_contiguous_probability(bigram_probabilities, clean_line(line, bg_separator), bg_separator)
            line_comparison = compare_lines(line, segmented_line)
            for i_comparison in range(len(line_comparison)):
                test_comparison[i_comparison] += line_comparison[i_comparison]
#            print(line)
#            print(segmented_line)
#            print(line_comparison)
# =============================================================================
#         print("\nTEST " + str(i+1))
#         print(test_comparison)
#         print_test_rates(test_comparison)
        for i_comparison in range(len(test_comparison)):
            full_comparison[i_comparison] += test_comparison[i_comparison]
# =============================================================================
    print ("\nFULL TEST")
    print (full_comparison)
    print_test_rates(full_comparison)
    
    
    
def test_transitional_phoneme_10_fold_cv():
    print("Phoneme segmentation, 10-fold crosss validation whole corpus (transitional)")
    route = "../corpus/CGN-NL-50k-utt.txt"
    text = load_file(route)
    randomize = True
    bg_separator = ""

    full_comparison = [0, 0, 0, 0]

    divided_data = divide_data(text, randomize)
    for i in range(len(divided_data)):
        training_data, test_data = prepare_training_test_data(divided_data, i)
    #    training_data, test_data = prepare_training_test_data(divided_data, 0)
        bigram_probabilities = bigram_transitional_probabilities_from_data(training_data, bg_separator)
        test_comparison = [0, 0, 0, 0]
        for line in test_data:
            line = line.strip()
            if len(line) < 3:
                continue
            segmented_line = segment_line_contiguous_probability(bigram_probabilities, clean_line(line, bg_separator), bg_separator)
            line_comparison = compare_lines(line, segmented_line)
            for i_comparison in range(len(line_comparison)):
                test_comparison[i_comparison] += line_comparison[i_comparison]
#            print(line)
#            print(segmented_line)
#            print(line_comparison)
# =============================================================================
#         print("\nTEST " + str(i+1))
#         print(test_comparison)
#         print_test_rates(test_comparison)
        for i_comparison in range(len(test_comparison)):
            full_comparison[i_comparison] += test_comparison[i_comparison]
# =============================================================================
    print ("\nFULL TEST")
    print (full_comparison)
    print_test_rates(full_comparison)
    
def test_transitional_phoneme_sentence_10_fold_cv(threshold):
    print("\nPhoneme segmentation (w/ sentence boundaries), 10-fold crosss validation whole corpus (transitional). Threshold = " + str(threshold))
    route = "../corpus/CGN-NL-50k-utt.txt"
    text = load_file(route)
    randomize = True
    bg_separator = ""

    full_comparison = [0, 0, 0, 0]

    divided_data = divide_data(text, randomize)
    for i in range(len(divided_data)):
        training_data, test_data = prepare_training_test_data(divided_data, i)
    #    training_data, test_data = prepare_training_test_data(divided_data, 0)
        bigram_probabilities = bigram_transitional_probabilities_from_data(training_data, bg_separator)
        test_comparison = [0, 0, 0, 0]
        for line in test_data:
            line = line.strip()
            if len(line) < 3:
                continue
            segmented_line = segment_line_contiguous_probability(bigram_probabilities, clean_line(line, bg_separator), bg_separator, threshold)
            line_comparison = compare_lines(line, segmented_line)
            for i_comparison in range(len(line_comparison)):
                test_comparison[i_comparison] += line_comparison[i_comparison]
#            print(line)
#            print(segmented_line)
#            print(line_comparison)
# =============================================================================
#         print("\nTEST " + str(i+1))
#         print(test_comparison)
#         print_test_rates(test_comparison)
        for i_comparison in range(len(test_comparison)):
            full_comparison[i_comparison] += test_comparison[i_comparison]
# =============================================================================
    print ("FULL TEST")
    print (full_comparison)
    print_test_rates(full_comparison)
    
    
def test_absolute_syllable_10_fold_cv():
    print("Syllable segmentation, 10-fold crosss validation whole corpus")
    route = "../corpus/CGN-NL-50k-utt-syllables.txt"
    text = load_file(route)
    randomize = True
    bg_separator = "-"
    boundary = " "

    full_comparison = [0, 0, 0, 0]

    divided_data = divide_data(text, randomize)
    for i in range(len(divided_data)):
        training_data, test_data = prepare_training_test_data(divided_data, i)
    #    training_data, test_data = prepare_training_test_data(divided_data, 0)
        bigram_probabilities = bigram_absolute_probabilities_from_data(training_data, bg_separator)
        test_comparison = [0, 0, 0, 0]
        for line in test_data:
            line = line.strip()
            if len(line) < 3:
                continue
            segmented_line = segment_line_contiguous_probability(bigram_probabilities, clean_line(line, bg_separator), bg_separator)
            gram_line = line_2_grams_w_boundaries(line, bg_separator, boundary)
            gram_segmented_line = line_2_grams_w_boundaries(segmented_line, bg_separator, boundary)
                    
            line_comparison = compare_lines(gram_line, gram_segmented_line)
            for i_comparison in range(len(line_comparison)):
                test_comparison[i_comparison] += line_comparison[i_comparison]
#            print(line)
#            print(segmented_line)
#            print(line_comparison)
# =============================================================================
#         print("\nTEST " + str(i+1))
#         print(test_comparison)
#         print_test_rates(test_comparison)
        for i_comparison in range(len(test_comparison)):
            full_comparison[i_comparison] += test_comparison[i_comparison]
# =============================================================================
    print ("\nFULL TEST")
    print (full_comparison)
    print_test_rates(full_comparison)
    
def test_absolute_syllable_sentence_10_fold_cv():
    print("Syllable segmentation (w/ sentence boundaries), 10-fold crosss validation whole corpus")
    route = "../corpus/CGN-NL-50k-utt-syllables.txt"
    text = load_file(route)
    randomize = True
    bg_separator = "-"
    boundary = " "

    full_comparison = [0, 0, 0, 0]

    divided_data = divide_data(text, randomize)
    for i in range(len(divided_data)):
        training_data, test_data = prepare_training_test_data(divided_data, i)
    #    training_data, test_data = prepare_training_test_data(divided_data, 0)
        bigram_probabilities = bigram_absolute_probabilities_from_data(training_data, bg_separator)
        test_comparison = [0, 0, 0, 0]
        for line in test_data:
            line = line.strip()
            if len(line) < 3:
                continue
            segmented_line = segment_line_contiguous_probability(bigram_probabilities, clean_line(line, bg_separator), bg_separator)
            gram_line = line_2_grams_w_boundaries(line, bg_separator, boundary)
            gram_segmented_line = line_2_grams_w_boundaries(segmented_line, bg_separator, boundary)
                    
            line_comparison = compare_lines(gram_line, gram_segmented_line)
            for i_comparison in range(len(line_comparison)):
                test_comparison[i_comparison] += line_comparison[i_comparison]
#            print(line)
#            print(segmented_line)
#            print(line_comparison)

# =============================================================================
#         print("\nTEST " + str(i+1))
#         print(test_comparison)
#         print_test_rates(test_comparison)
# =============================================================================

        for i_comparison in range(len(test_comparison)):
            full_comparison[i_comparison] += test_comparison[i_comparison]
    print ("\nFULL TEST")
    print (full_comparison)
    print_test_rates(full_comparison)
    
    
    
def test_transitional_syllable_10_fold_cv():
    print("Syllable segmentation, 10-fold crosss validation whole corpus (transitional)")
    route = "../corpus/CGN-NL-50k-utt-syllables.txt"
    text = load_file(route)
    randomize = True
    bg_separator = "-"
    boundary = " "

    full_comparison = [0, 0, 0, 0]

    divided_data = divide_data(text, randomize)
    for i in range(len(divided_data)):
        training_data, test_data = prepare_training_test_data(divided_data, i)
    #    training_data, test_data = prepare_training_test_data(divided_data, 0)
        bigram_probabilities = bigram_transitional_probabilities_from_data(training_data, bg_separator)
        test_comparison = [0, 0, 0, 0]
        for line in test_data:
            line = line.strip()
            if len(line) < 3:
                continue
            segmented_line = segment_line_contiguous_probability(bigram_probabilities, clean_line(line, bg_separator), bg_separator)
            gram_line = line_2_grams_w_boundaries(line, bg_separator, boundary)
            gram_segmented_line = line_2_grams_w_boundaries(segmented_line, bg_separator, boundary)
                    
            line_comparison = compare_lines(gram_line, gram_segmented_line)
            for i_comparison in range(len(line_comparison)):
                test_comparison[i_comparison] += line_comparison[i_comparison]
#            print(line)
#            print(segmented_line)
#            print(line_comparison)
# =============================================================================
#         print("\nTEST " + str(i+1))
#         print(test_comparison)
#         print_test_rates(test_comparison)
        for i_comparison in range(len(test_comparison)):
            full_comparison[i_comparison] += test_comparison[i_comparison]
# =============================================================================
    print ("\nFULL TEST")
    print (full_comparison)
    print_test_rates(full_comparison)
    
def test_transitional_syllable_sentence_10_fold_cv(threshold):
    print("\nSyllable segmentation (w/ sentence boundaries), 10-fold crosss validation whole corpus (transitional). Threshold = " + str(threshold))
    route = "../corpus/CGN-NL-50k-utt-syllables.txt"
    text = load_file(route)
    randomize = True
    bg_separator = "-"
    boundary = " "

    full_comparison = [0, 0, 0, 0]

    divided_data = divide_data(text, randomize)
    for i in range(len(divided_data)):
        training_data, test_data = prepare_training_test_data(divided_data, i)
    #    training_data, test_data = prepare_training_test_data(divided_data, 0)
        bigram_probabilities = bigram_transitional_probabilities_from_data(training_data, bg_separator)
        test_comparison = [0, 0, 0, 0]
        for line in test_data:
            line = line.strip()
            if len(line) < 3:
                continue
            segmented_line = segment_line_contiguous_probability(bigram_probabilities, clean_line(line, bg_separator), bg_separator, threshold)
            gram_line = line_2_grams_w_boundaries(line, bg_separator, boundary)
            gram_segmented_line = line_2_grams_w_boundaries(segmented_line, bg_separator, boundary)
                    
            line_comparison = compare_lines(gram_line, gram_segmented_line)
            for i_comparison in range(len(line_comparison)):
                test_comparison[i_comparison] += line_comparison[i_comparison]
#            print(line)
#            print(segmented_line)
#            print(line_comparison)
# =============================================================================
#         print("\nTEST " + str(i+1))
#         print(test_comparison)
#         print_test_rates(test_comparison)
# =============================================================================
        for i_comparison in range(len(test_comparison)):
            full_comparison[i_comparison] += test_comparison[i_comparison]

    print ("FULL TEST")
    print (full_comparison)
    print_test_rates(full_comparison)
    


def test_absolute_phoneme_toy():
    print("Phoneme segmentation (toy problem)")

    training_line = "peli roca mano roca peli mano peli"
    testing_line = "pelo roca mano roca pelo mano pelo"
    text = [training_line, testing_line]
    
    bg_separator = ""
    bigram_appearances = find_bigrams(text[0:1], bg_separator)
    bigram_probabilities = calculate_absolute_probabilities(bigram_appearances)
    test_comparison = [0, 0, 0, 0]
    for line in text:
        segmented_line = segment_line_contiguous_probability(bigram_probabilities, clean_line(line, bg_separator), bg_separator)
        line_comparison = compare_lines(line, segmented_line)
        
        for i_comparison in range(len(line_comparison)):
            test_comparison[i_comparison] += line_comparison[i_comparison]
        
        print(line)
        print(segmented_line)
        print(line_comparison)
        print_test_rates(line_comparison)
    print(test_comparison)
    print_test_rates(test_comparison)

def test_absolute_syllables_toy():
    print("Syllable segmentation (toy problem)")

    training_line = "pe-li ro-ca ma-no ro-ca pe-li ma-no pe-li"
    testing_line = "pe-lo ro-ca ma-no ro-ca pe-lo ma-no pe-lo"
    separator = "-"
    boundary = " "
    text = [training_line, testing_line]
    
    bigram_appearances = find_bigrams(text[0:1], separator)
    bigram_probabilities = calculate_absolute_probabilities(bigram_appearances)
    test_comparison = [0, 0, 0, 0]
    for line in text:
        segmented_line = segment_line_contiguous_probability(bigram_probabilities, clean_line(line, separator), separator)
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
def test_absolute_syllables_overfitting():
    print("Syllable segmentation: Training and testing with whole corpus")

    route = "../corpus/CGN-NL-50k-utt-syllables.txt"
    text = load_file(route)
    bg_separator = "-"
    boundary = ' '
    
    bigram_probabilities = bigram_absolute_probabilities_from_data(text, bg_separator)
    test_comparison = [0, 0, 0, 0]
    for line in text:
        line = line.strip()
        if len(line) < 3:
            continue
        segmented_line = segment_line_contiguous_probability(bigram_probabilities, clean_line(line, bg_separator), bg_separator)
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
#        print(line)
#        print(segmented_line)
#        print(line_comparison)
    print(test_comparison)
    print_test_rates(test_comparison)

# Overfitting test
def test_transitional_phoneme_overfitting():
    print("Phoneme segmentation, training and testing with whole corpus (transitional)")
    route = "../corpus/CGN-NL-50k-utt.txt"
    text = load_file(route)
    bg_separator = ""
    bigram_probabilities = bigram_transitional_probabilities_from_data(text, bg_separator)
    test_comparison = [0, 0, 0, 0]
    for line in text:
        line = line.strip()
        if len(line) < 3:
            continue
        segmented_line = segment_line_contiguous_probability(bigram_probabilities, clean_line(line, bg_separator), bg_separator)
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
    
# Overfitting test
def test_transitional_phoneme_sentence_overfitting():
    print("Phoneme (w/sentence boundary) segmentation, training and testing with whole corpus (transitional)")
    route = "../corpus/CGN-NL-50k-utt.txt"
    text = load_file(route)
    bg_separator = ""
    bigram_probabilities = bigram_transitional_probabilities_from_data(text, bg_separator)
    test_comparison = [0, 0, 0, 0]
    for line in text:
        line = line.strip()
        if len(line) < 3:
            continue
        segmented_line = segment_line_contiguous_probability(bigram_probabilities, clean_line(line, bg_separator), bg_separator)
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

def test_syllables1():
    line1 = "pe-li ro-ca ma-no ro-ca pe-li ma-no pe-li"
    line2 = "pe-lo ro-ca ma-no ro-ca pe-lo ma-no pe-lo"
    separator = "-"
    boundary = " "
    text = [line1, line2]
    
    bigram_appearances = find_bigrams(text[0:2], separator)
    syllable_appearances = find_syllables(text[0:2], separator)
    bigram_probabilities = calculate_syllable_statistics(bigram_appearances, syllable_appearances, separator)
    test_comparison = [0, 0, 0, 0]
    for line in text:
        segmented_line = segment_line_threshold(bigram_probabilities, clean_line(line, separator), separator)
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
    
    bigram_probabilities = bigram_transitional_probabilities_from_data(text, bg_separator)
    test_comparison = [0, 0, 0, 0]
    for line in text:
        line = line.strip()
        if len(line) < 2:
            continue
        segmented_line = segment_line_threshold(bigram_probabilities, clean_line(line, bg_separator), bg_separator)
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
#    test1()
#    test_absolute_default_bg_separator() # This functionality is potentially confusing, so I'll avoid implementing it
#    test_absolute_phoneme_toy()
#    test_absolute_phoneme_overfitting()
#    test_transitional_phoneme_overfitting()
#    test_transitional_phoneme_sentence_overfitting()
    
#    test_absolute_phoneme_10_fold_cv()
#    test_transitional_phoneme_10_fold_cv()
#    test_absolute_phoneme_sentence_10_fold_cv()
    test_transitional_phoneme_sentence_10_fold_cv(0)
#    test_transitional_phoneme_sentence_10_fold_cv(0.005)
#    test_transitional_phoneme_sentence_10_fold_cv(0.01)
#    test_transitional_phoneme_sentence_10_fold_cv(0.02)
#    test_transitional_phoneme_sentence_10_fold_cv(0.05)
    test_transitional_phoneme_sentence_10_fold_cv(1)
    test_transitional_phoneme_sentence_10_fold_cv(1.1)
    
#    test_absolute_syllable_10_fold_cv()
#    test_transitional_syllable_10_fold_cv()
#    test_absolute_syllable_sentence_10_fold_cv()
    test_transitional_syllable_sentence_10_fold_cv(0)
    test_transitional_syllable_sentence_10_fold_cv(0.005)
    test_transitional_syllable_sentence_10_fold_cv(0.01)
    test_transitional_syllable_sentence_10_fold_cv(0.02)
    test_transitional_syllable_sentence_10_fold_cv(0.05)
    test_transitional_syllable_sentence_10_fold_cv(1)
    test_transitional_syllable_sentence_10_fold_cv(1.1)
    
#    test_absolute_syllables_toy()
#    test_absolute_syllables_overfitting()
#    #test_syllables1()
#    test_syllables2()
    print ("\nCurrent state: Segmentation with sentence boundaries hardcoded in segmentation")