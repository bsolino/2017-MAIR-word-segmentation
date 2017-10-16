# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 11:24:06 2017

@author: Breixo
"""


# text:Array of lines of the text
def build_bigram_database(text):
    db = {} # Dictionary bigram -> number of occurrences
    for line in text:
        line_bigrams = count_bigrams(line)
        update_db(db, line_bigrams) # TODO: Python passes dictionaries by value or by reference?
        #TODO # Update the db with the bigrams
    return db
    #TODO # Save the db to a file for further use

# Count bigrams in the line, return dictionary bigram -> number of occurrences
def count_bigrams(line, sep = ""):
    # TODO Adapt this to other kinds of bigrams
    bigram_dict = {}
    if len(line) >= 2:
        old_c = None
        for c in line:
            if old_c != None:
                bigram = old_c + c
                bigram_dict[bigram] = bigram_dict.get(bigram, 0) +1
            old_c = c
    #elif len(line) == 1:
    #    pass # TODO?
    return bigram_dict
    
# Updates the bigram database with the information from a line of text
def update_db(db, line_bigrams):
    for key in line_bigrams.keys():
        update = line_bigrams[key]
        current = db.get(key, 0)
        db[key] = current + update
    return db