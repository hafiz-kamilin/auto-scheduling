#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
[Smart Tomato Farm Problem]

    Tomato farm is divided into 3 areas which is a, b and c due to the limitation on area covered by
    individual sprinkler. To find how long we should run the sprinkler, a heuristic
    calculation for auto-scheduling methodology is developed.

    #############
    #       # a #
    #   b   #####        area (a):  5 [m^2]
    #       #            area (b): 30 [m^2]
    #########            area (c): 10 [m^2] 
    #   C   # 
    #########

    We assume that each areas have only one sprinkler and the water output are;
    - area (a) have  5 [L/m] 
    - area (b) have 20 [L/m]
    - area (c) have 13 [L/m]

    We assume one tomato tree that take 0.5 [m^2] of space need 3.4 [L] in one day, thus;
    - area (a) need 34.0 [L]
    - area (b) need 81.6 [L]
    - area (c) need 27.2 [L]

    We assume that the the system designer installed weather forecast sensor to calculate
    how much of water needed for irrigation. The precipitation is randomized
    with max precipitation of 40 [mm] in one week.

    In Array formatting: [x1, x2, x3, x4, x5, x6, x7]
    To convert precipitation to Liter = (x [mm] / 1000) [m] * y [m^2] * 1000 [L/m^3]  

    Extra parameter to create the schedule;
    - the schedule span for 1 week
    - sprinkler operate once for 1 day

"""
# load all necessary libraries needed in this program
import numpy as np
import random

# create a random weather forecast that span in one week
def random_wf():

    # initialize an empty array
    precipitation = []
    # max total precipitation in one weeks is 40 [mm]
    max = 40
    # initialize rain
    rain = 0

    # fill the empty array with 7 randomized precipitation (rain) [mm]
    for i in range(7):

        # toss the coin, if it is head
        if (random.randint(0, 1) == 0):

            # not raining
            precipitation.append(0)

        # else generate random number of precipitation
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
            max = max - rain
            # raining
            precipitation.append(rain)

    # return the result
    return precipitation
    

# function to find the optimized sprinkler output based on the weather forecast
def algorithm_as(sensor_reading, cycle_output, interval_output, activation_time, actuator_spec):

    # initialize an empty array
    out1 = []

    # if rainfall from the weather forecast didn't exceed the target_out
    if (sum(sensor_reading) <= cycle_output):

        # create the forecast scheduling
        for i in range(activation_time):

            # find the output needed at that interval
            out1.append(interval_output - sensor_reading[i])

        # normalize the array from negative element
        for i in range(activation_time): 

            # initialize counter
            j = 0
            k = 0

            # if the element is negative
            if (out1[i] < 0):

                # loop until the negative element spreadout
                while True:

                    try:

                        # increase the counter
                        j += 1

                        # if the next element in the array is not negative and bigger or equal with the current element
                        if ((out1[i + j] > 0) and (out1[i + j] >= -out1[i])):

                            # update the next element
                            out1[i + j] = out1[i + j] + out1[i]
                            # swap the current element with 0
                            out1[i] = 0
                            # break from the while loop
                            break

                        # else if the next element in the array is not negative and smaller than the current element
                        elif ((out1[i + j] > 0) and (out1[i + j] < -out1[i])):

                            # update the current element
                            out1[i] = out1[i + j] + out1[i]
                            # swap the next element with 0
                            out1[i + j] = 0

                    except:

                        # increase the counter
                        k -= 1

                        # if the next element in the array is not negative and bigger or equal with the current element
                        if ((out1[i + k] > 0) and (out1[i + k] >= -out1[i])):

                            # update the next element
                            out1[i + k] = out1[i + k] + out1[i]
                            # swap the current element with 0
                            out1[i] = 0
                            # break from the while loop
                            break

                        # else if the next element in the array is not negative and smaller than the current element
                        elif ((out1[i + k] > 0) and (out1[i + k] < -out1[i])):

                            # update the current element
                            out1[i] = out1[i + k] + out1[i]
                            # swap the next element with 0
                            out1[i + k] = 0

        # divide out1 which is [L] with actuators_s which is [L/m] and multiply by 60 to get the schedule in minutes
        out2 = [(j / actuator_spec) for j in out1]
        # round up to 2 decimal places
        out2 = list(np.around(np.array(out2), 2))
        # unoptimized schedule for the sake of comparison
        out3 = [(k / actuator_spec) for k in ([interval_output] * 7)]
        # round up to 2 decimal places
        out3 = list(np.around(np.array(out3), 2))
        # show the optimized schedule
        print ("  Auto-scheduling runtime = %s [minute]\n    Total volume = %s [L]" % (out2, sum(out1)))
        # compare with the unoptimized schedule
        print ("  Timing-based runtime = %s [minute]\n    Total volume = %s [L]" % (out3, interval_output * 7))
        # total volume of water in [L]
        print ("Saved volume = %s [L]" % (interval_output * 7 - sum(out1)))
        # return the table
        return out2

    # if the rainfall exceed the target output for the sprinkler
    else:

        # don't generate the output
        print ("  Rainfall exceed the amount of water needed to be sprinkled.")
        print ("  Output volume for the sprinkler won't be generated until the next interval.")

# initiator
if __name__ == '__main__':

    # time interval for 1 cycle is 7 [day]
    interval1 = 7
    # time interval for every loop is 1 [day]
    interval2 = 1
    # weather forecast precipitation for 7 [day] # in [mm] format
    # to see if limiter sanitycheck is working random_wf() with [0, 0, 0, 0, 0, 0, 48]
    sensor = random_wf()
    # calculate how many time sprinkler (interval2) will activate in 1 cycle (interval1)
    activation_time = int(interval1 / interval2)
    # show the user the randomized weather forecast
    print ("Randomized weather forecast in one week is: %s [mm]" % sensor)

    # result for area a
    print ("\nSchedule for sprinkler in area (a):")
    # meter square of area
    area_a = 5
    # actuators capability sprinkler is 5 [L/m]
    actuator_a = 5
    # rainfall in [L] based on meter square of area
    sensor_a = [(i * area_a) for i in sensor]
    # total output [L] that actuator (sprinkler) need to meet for every cycle
    weeklyoutput_a = 3.4 / 0.5 * area_a * interval1
    # spread the target output to each activation time
    dailyoutput_a = weeklyoutput_a / activation_time
    # initialize an empty array to store the time needed to reach the daily quota
    out_a = []
    # calculate the time needed
    out_a = algorithm_as(sensor_a, weeklyoutput_a, dailyoutput_a, activation_time, actuator_a)

    # result for area b
    print ("\nSchedule for sprinkler in area (b):")
    # meter square of area
    area_b = 30
    # actuators capability sprinkler is 20 [L/m]
    actuator_b = 20
    # rainfall in [L] based on meter square of area
    sensor_b = [(i * area_b) for i in sensor]
    # total output [L] that actuator (sprinkler) need to meet for every cycle
    weeklyoutput_b = 3.4 / 0.5 * area_b * interval1
    # spread the target output to each activation time
    dailyoutput_b = weeklyoutput_b / activation_time
    # initialize an empty array to store the time needed to reach the daily quota
    out_b = []
    # calculate the time needed
    out_b = algorithm_as(sensor_b, weeklyoutput_b, dailyoutput_b, activation_time, actuator_b)

    # result for area c
    print ("\nSchedule for sprinkler in area (c):")
    # meter square of area
    area_c = 10
    # actuators capability sprinkler is 13 [L/m]
    actuator_c = 13
    # rainfall in [L] based on meter square of area
    sensor_c = [(i * area_c) for i in sensor]
    # total output [L] that actuator (sprinkler) need to meet for every cycle
    weeklyoutput_c = 3.4 / 0.5 * area_c * interval1
    # spread the target output to each activation time
    dailyoutput_c = weeklyoutput_c / activation_time
    # initialize an empty array to store the time needed to reach the daily quota
    out_c = []
    # calculate the time needed
    out_c = algorithm_as(sensor_c, weeklyoutput_c, dailyoutput_c, activation_time, actuator_c)
