#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import random generator module 
import random

# create a random sensor input for the span of interval1
def sensor(interval1, interval2):

    # initialize an empty array
    array = []
    # max total array in interval1 is 40
    max = 40
    # initialize number
    number = 0
    # initialize counter
    i = 0

    # fill the empty array with randomized array (number)
    while (i < int(interval1 / interval2)):

        # toss the coin, if it is head
        if (random.randint(0, 1) == 0):

            # element is 0
            array.append(0)

        # if tail, generate random number of array
        else:

            # as long max is not 0
            if (max != 0):

                # element is randomized
                number = random.randint(1, max)
            
            # else
            else:
                
                # no number
                number = 0

            # update the max ceiling
            max -= number
            # append the number
            array.append(number)

        # increase the counter
        i += 1

    # return the result
    return array