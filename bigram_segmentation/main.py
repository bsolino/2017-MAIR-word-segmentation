# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 15:06:16 2017

@author: Breixo
"""
from bigram_utils import clean_line, bigram_transitional_probabilities_from_data
from segmentation_utils import segment_line_contiguous_probability, line_2_bigrams, segment_random
from file_utils import load_file, divide_data, prepare_training_test_data
from test_utils import compare_lines, test_rates

def print_test_rates(comparison):
    
    rates = test_rates(comparison)
    print("True positive rate (sensitivity): " + str(rates[0]))
    print("False positive rate:              " + str(rates[1]))
#    print("True negative rate (specificity): " + str(rates[2]))

# =============================================================================
# Separates a line in unigrams, considering the word boundary as a unigram too
# If the character to separate unigrams is "", returns the line as is, as it
# can be considered already as a list of unigrams including the word boundary
# @in line: Line to be converted to unigrams
# @in bg_separator: Character used to separate the unigrams in the line
# @in w_boundary: Character used to represent a word boundary
# @return List of unigrams, including word boundaries
# =============================================================================
def line_2_grams_w_boundaries(line, bg_separator, w_boundary):
    if bg_separator != "":
        line = line.split(bg_separator)
        aux = []
        for item in line:
            if w_boundary in item:
                split_item = item.split(w_boundary)
                aux.append(split_item[0])
                for si in split_item[1:]:
                    aux.append(w_boundary)
                    aux.append(si)
            else:
                aux.append(item)
        line = [item for item in aux if item != ""]
    return line


# =============================================================================
# Execute a test on a given corpus, with a threshold value, bigram separator
# and word boundary. The test executes 10-fold cross validation on the corpus,
# stores the true and false positives and true and false negatives and prints
# the results for the whole test.
# Some code lines can be uncommented to print the lines of text as they are
# being segmented, and the partial results for each cross validation test
# @in route: Route to the corpus to be used
#     Usual values:
#         "../corpus/CGN-NL-50k-utt.txt" Corpus without syllable boundaries
#         "../corpus/syllabification_30-10.txt" Corpus with syllable boundaries
# @in threshold: Threshold used to insert a word boundary in a bigram. A word
#     boundary is introduced if the transitional probability of the bigram is
#     smaller or equal to the threshold. To avoid the use of thresholds use a
#     negative threshold
# @in bg_separator: Character used to represent a separation between unigrams
#     in the corpus
#     Usual values:
#         "": No separator specified
#         "-": Used in "/corpus/syllabification_30-10.txt" to separate
#             syllables
# @in w_boundary: Character used to represent a word boundary in the corpus
# @in random_segmentation: Segment at random, used to create a baseline
#     Default value: False
# =============================================================================
def test(route, threshold, bg_separator, w_boundary, random_segmentation = False):
    print("\n Route = {0}, Threshold = {1}, bg_separator = '{2}', w_boundary = '{3}'".format(route, threshold, bg_separator, w_boundary))
    if random_segmentation:
        print(" NOTE: RANDOM SEGMENTATION")
    text = load_file(route)
    randomize_data = True # Randomize 10-fold cross validation data

    full_comparison = [0, 0, 0, 0]

    divided_data = divide_data(text, randomize_data)
    for i in range(len(divided_data)):
        training_data, test_data = prepare_training_test_data(divided_data, i)
        bigram_probabilities = bigram_transitional_probabilities_from_data(training_data, bg_separator)
        test_comparison = [0, 0, 0, 0]
        for line in test_data:
            line = line.strip()
            bigram_line = line_2_bigrams(clean_line(line, bg_separator), bg_separator)
            # Ignore lines without bigrams in results
            if len(bigram_line) < 1:
                continue
            if not random_segmentation:
                segmented_line = segment_line_contiguous_probability(bigram_probabilities, bigram_line, bg_separator, threshold)
            else:
                segmented_line = segment_random(bigram_line, bg_separator, 0.5)
            gram_line = line_2_grams_w_boundaries(line, bg_separator, w_boundary)
            gram_segmented_line = line_2_grams_w_boundaries(segmented_line, bg_separator, w_boundary)
                    
            line_comparison = compare_lines(gram_line, gram_segmented_line)
            for i_comparison in range(len(line_comparison)):
                test_comparison[i_comparison] += line_comparison[i_comparison]
            # Uncomment these lines to print the lines as they are segmented
#            print(line) # Print the original line
#            print(segmented_line) # Print the line after segmentation
#            print(line_comparison) # Print the comparison between lines

        # Uncomment these lines to print intermediate 10-fold cross validation results
        #print("\nTEST " + str(i+1))
        #print(test_comparison)
        #print_test_rates(test_comparison)

        for i_comparison in range(len(test_comparison)):
            full_comparison[i_comparison] += test_comparison[i_comparison]

    print ("\nFULL TEST")
    print (full_comparison)
    print_test_rates(full_comparison)



# =============================================================================
# Main Method
# =============================================================================

if __name__ == "__main__":
    test("../corpus/CGN-NL-50k-utt.txt", -1, '', ' ', True) # Baseline for phonemes
    test("../corpus/CGN-NL-50k-utt.txt", -1, '', ' ') # Test for phonemes & neighbours
    test("../corpus/CGN-NL-50k-utt.txt", 0.005, '', ' ')  # Test for phonemes & neighbours + threshold
    test("../corpus/CGN-NL-50k-utt.txt", 0.01, '', ' ')  # Test for phonemes & neighbours + threshold
    test("../corpus/CGN-NL-50k-utt.txt", 0.012, '', ' ')  # Test for phonemes & neighbours + threshold
    test("../corpus/CGN-NL-50k-utt.txt", 0.015, '', ' ')  # Test for phonemes & neighbours + threshold
    test("../corpus/syllabification_30-10.txt", -1, '-', ' ', True) # Baseline for syllables
    test("../corpus/syllabification_30-10.txt", -1, '-', ' ') # Test for syllables & neighbours
    test("../corpus/syllabification_30-10.txt", 0.005, '-', ' ')  # Test for syllables & neighbours + threshold
    test("../corpus/syllabification_30-10.txt", 0.01, '-', ' ')  # Test for syllables & neighbours + threshold
    test("../corpus/syllabification_30-10.txt", 0.012, '-', ' ')  # Test for syllables & neighbours + threshold
    test("../corpus/syllabification_30-10.txt", 0.015, '-', ' ')  # Test for syllables & neighbours + threshold
