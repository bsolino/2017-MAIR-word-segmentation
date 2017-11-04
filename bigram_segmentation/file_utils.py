# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 12:38:02 2017

@author: Breixo
"""

import random
from collections import deque

def load_file(route):
    with open(route) as f:
        text = []
        for line in f:
            text.append(line)
    return text

# Divides the data evenly in parts.
# data: List of data points
# randomize: If true the data is randomized before dividing
# n_parts: Number of parts in which divide. If the number of parts is bigger
#    than the number of data items the result will be divided in less parts
# Used for 10-fold cross-validation, it shuffles the data into a random order of equal size.
def divide_data(data, randomize = True, n_parts = 10):
    data = data.copy()
    if randomize:
        random.shuffle(data)
    length = len(data)
    stops = []
    for i in range(1, n_parts):
        stops.append(length * i / n_parts)
    stops = deque(stops)
        
    division = []
    current = []
    for i in range(length):
        if len(stops) > 0 and i >= stops[0]:
            division.append(current)
            current = []
            stops.popleft()
        current.append(data[i])
    division.append(current)
    return division

def prepare_training_test_data(divided_data, i_test):
    test_data = divided_data[i_test]
    training_data = []
    for i in range(len(divided_data)):
        if i != i_test:
            training_data += divided_data[i]
    return training_data, test_data