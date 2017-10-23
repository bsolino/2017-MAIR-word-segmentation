# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 12:14:53 2017

@author: Breixo
"""

# This assumes there are separators only in the middle of the string
#   and never more than two spaces next to each other
def compare_lines(original_line, test_line, boundary = " "):
    
    # TODO When comparing with syllables, consider each syllable as a bigram
    
    true_positives = 0  # Space in test, space in original
    false_positives = 0 # Space in test, NO space in original
    false_negatives = 0 # NO space in test, space in original
    true_negatives = 0 # NO space in test, NO space in original
    
    j = 0
    
    # NEW VERSION (bigram by bigram)
    i = 0
    while i < (len(original_line) -1):
        pair_o = original_line[i] + original_line[i+1]
        pair_t = test_line[j] + test_line[j+1]
        
        is_sep_o = boundary in pair_o
        is_sep_t = boundary in pair_t
        
        i += 1
        j += 1
        if is_sep_o:
            i += 1 # Skip the space in the next iteration
            
        if is_sep_t:
            j += 1 # Skip the space in the next iteration
            if is_sep_o:
                true_positives += 1
            else:
                false_positives += 1
        else:
            if is_sep_o:
                false_negatives += 1
            else:
                true_negatives += 1
        #TODO REMOVE DEBUG
#        match_type = " Positive" if is_sep_t else " Negative"
#        print("'" + pair_o + "' == '" + pair_t + "' ? " + str(pair_o == pair_t) + match_type)

    
    return true_positives, true_negatives, false_positives, false_negatives

def test_rates(comparison):
    tp = comparison[0]
    tn = comparison[1]
    fp = comparison[2]
    fn = comparison[3]
    
    true_positive_rate = tp / (tp + fn)
    false_positive_rate = fp / (fp + tn)
    true_negative_rate = tn / (fp + tn)
    return true_positive_rate, false_positive_rate, true_negative_rate
    