#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import random generator module 
import random

# create a random sensor input for the span of interval1
def sensor(interval1, interval2):

    # initialize an empty array
    precipitation = []
    # max total precipitation in one weeks is 40 [mm]
    max = 40
    # initialize rain
    rain = 0
    # initialize counter
    i = 0

    # fill the empty array with randomized precipitation (rain) [mm]
    while (i < int(interval1 / interval2)):

        # toss the coin, if it is head
        if (random.randint(0, 1) == 0):

            # not raining
            precipitation.append(0)

        # if tail, generate random number of precipitation
        else:

            # as long max is not 0
            if (max != 0):

                # randomize the precipitation
                rain = random.randint(1, max)
            
            # else
            else:
                
                # no rain
                rain = 0

            # update the max ceiling
            max -= rain
            # raining
            precipitation.append(rain)

        # increase the counter
        i += 1

    # return the result
    return precipitation