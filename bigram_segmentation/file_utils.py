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

def prepare_training_test_data(text):
    # TODO If length < 10, this can't apply
    text = text.copy()
    random.shuffle(text)
    length = len(text)
    stops = []
    for i in range(1, 10):
        stops.append(length * i / 10)
    stops = deque(stops)
        
    division = []
    current = []
    for i in range(length):
        if len(stops) > 0 and i >= stops[0]:
            division.append(current)
            current = []
            stops.popleft()
        current.append(text[i])
    division.append(current)
    return division