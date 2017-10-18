# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 12:38:02 2017

@author: Breixo
"""

def load_file(route):
    with open(route) as f:
        text = []
        for line in f:
            text.append(line.strip())
    return text