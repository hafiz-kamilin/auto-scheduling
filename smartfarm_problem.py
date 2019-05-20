#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# load all necessary libraries needed in this program
import random
import pulp

"""
[Smart Tomato Farm Problem]

    Tomato farm is divided into 3 areas which is a, b and c due to the limitation on area covered
    by individual sprinkler. To find how long we should run the sprinkler, a linear
    programming calculation is used to optimize the sprinkler runtime.

    #############
    #       # a #
    #   b   #####        area (a):  5 [m^2]
    #       #            area (b): 30 [m^2]
    #########            area (c): 10 [m^2] 
    #   C   # 
    #########

    We assume that each areas have only one sprinkler and the sprinkler'S output are;
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

# function to generate runtime distribution
def compute(interval1, interval2, sensor, actuator, weeklyoutput, dailyoutput):
    # compute(interval1, interval2, sensor_a, actuator_a, weeklyoutput_a, dailyoutput_a)

    # calculate how many time interval2 will be activated in 1 interval1
    activation_time = int(interval1 / interval2)

    # do sanity check to see if the requirement for runtime distribution was met
    if ((activation_time == len(sensor)) and (sum(sensor) <= weeklyoutput)):

        # initialize the problem as a model with maximization target
        model = pulp.LpProblem("Runtime distribution", pulp.LpMaximize)
        # initialize the array to store the runtime distribution
        runtime1 = [0] * activation_time
        runtime2 = [0] * activation_time
        # initialize the array to store the balanced distribution calculation
        runtime3 = [dailyoutput] * activation_time

        # for every element in the runtime1 array
        for i in range(len(runtime1)):

            # initialize it with a lower limit of zero
            runtime1[i] = pulp.LpVariable(str(i), lowBound = 0, cat = 'Continuous')

        # for every element in the runtime2 array
        for j in range(len(runtime2)):

            # multiply the element with the actuator
            runtime2[j] = runtime1[j] * actuator

        # for every element in the runtime3 array
        for k in range(len(runtime3)):

            # calculate the difference
            runtime3[k] -= sensor[k]

        # set the objective function
        model += sum(runtime2), "Runtime"
        # set the output constraint
        model += sum(runtime2) <= (weeklyoutput - sum(sensor))
        # for every element in the runtime1
        for l in range(len(runtime1)):

            # set the input constraint in range of sensor[k]
            model += runtime1[l] <= runtime3[l]

        # solve the linear programming
        model.solve()
        pulp.LpStatus[model.status]

        # for every element in the runtime1
        for l in range(len(runtime1)):

            # refactoring the runtime1 into an answers
            runtime1[l] = runtime1[l].varValue

        # return the answer back to main
        return runtime1

    # sanity test failed
    else:

        # when wrong parameters are parsed
        if (activation_time != len(sensor)):

            # return true; user need to rework on their input
            return True

        # when total of sensor reading is over the limit
        if (sum(sensor) <= weeklyoutput):

            # return false; schedule cannot be created
            return False

# initiator
if __name__ == '__main__':

    # time interval for 1 cycle is 7 [day]
    interval1 = 7
    # time interval for every loop is 1 [day]
    interval2 = 1
    # weather forecast precipitation for 7 [day] # in [mm] format
    forecast = sensor(interval1, interval2)
    # show the user the randomized weather forecast
    print ("\nRandomized weather forecast in one week is: %s [mm]" % forecast)

    # result for area a
    print ("\nSchedule for sprinkler in area (a):")
    # meter square of area
    area_a = 5
    # actuators capability sprinkler is 5 [L/m]
    actuator_a = 5
    # rainfall in [L] based on meter square of area
    sensor_a = [(i * area_a) for i in forecast]
    # convert the sensor_a input from [L] to [minute]
    sensor_a = [(i / actuator_a) for i in sensor_a]
    # total output [L] that actuator (sprinkler) need to meet for every cycle
    weeklyoutput_a = 3.4 / 0.5 * area_a * interval1
    # spread the target output [minute] to each activation time
    dailyoutput_a = (3.4 / 0.5 * area_a) / actuator_a
    # compute the runtime schedule
    out_a = compute(interval1, interval2, sensor_a, actuator_a, weeklyoutput_a, dailyoutput_a)

    # if out_a return true instead of an array
    if (out_a == True):

        # inform the user
        print ("Condition for activation_time == len(sensor) was not met.")

    # if out_a return false instead of an array
    elif (out_a == False):

        # inform the user
        print ("The precipitation is over the weekly limit; scheduler disabled.")

    # else array is normally returned
    else:

        # show the computation result
        print ("  Auto-scheduling runtime = %s [minute]" % out_a) 
        print ("  Total volume = %s [L]" % int(sum(out_a) * actuator_a))
        print ("  Saved water = %s [L]" % int(weeklyoutput_a - sum(out_a) * actuator_a))

    # result for area b
    print ("\nSchedule for sprinkler in area (b):")
    # meter square of area
    area_b = 30
    # actuators capability sprinkler is 20 [L/m]
    actuator_b = 20
    # rainfall in [L] based on meter square of area
    sensor_b = [(i * area_b) for i in forecast]
    # convert the sensor_a input from [L] to [minute]
    sensor_b = [(i / actuator_b) for i in sensor_b]
    # total output [L] that actuator (sprinkler) need to meet for every cycle
    weeklyoutput_b = 3.4 / 0.5 * area_b * interval1
    # spread the target output [minute] to each activation time
    dailyoutput_b = (3.4 / 0.5 * area_b) / actuator_b
    # compute the runtime schedule
    out_b = compute(interval1, interval2, sensor_b, actuator_b, weeklyoutput_b, dailyoutput_b)

    # if out_b return true instead of an array
    if (out_b == True):

        # inform the user
        print ("Condition for activation_time == len(sensor) was not met.")

    # if out_b return false instead of an array
    elif (out_b == False):

        # inform the user
        print ("The precipitation is over the weekly limit; scheduler disabled.")

    # else array is normally returned
    else:

        # show the computation result
        print ("  Auto-scheduling runtime = %s [minute]" % out_b) 
        print ("  Total volume = %s [L]" % int(sum(out_b) * actuator_b))
        print ("  Saved water = %s [L]" % int(weeklyoutput_b - sum(out_b) * actuator_b))

    # result for area c
    print ("\nSchedule for sprinkler in area (c):")
    # meter square of area
    area_c = 10
    # actuators capability sprinkler is 13 [L/m]
    actuator_c = 13
    # rainfall in [L] based on meter square of area
    sensor_c = [(i * area_c) for i in forecast]
    # convert the sensor_a input from [L] to [minute]
    sensor_c = [(i / actuator_c) for i in sensor_c]
    # total output [L] that actuator (sprinkler) need to meet for every cycle
    weeklyoutput_c = 3.4 / 0.5 * area_c * interval1
    # spread the target output [minute] to each activation time
    dailyoutput_c = (3.4 / 0.5 * area_c) / actuator_c
    # compute the runtime schedule
    out_c = compute(interval1, interval2, sensor_c, actuator_c, weeklyoutput_c, dailyoutput_c)

    # if out_c return true instead of an array
    if (out_c == True):

        # inform the user
        print ("Condition for activation_time == len(sensor) was not met.")

    # if out_c return false instead of an array
    elif (out_c == False):

        # inform the user
        print ("The precipitation is over the weekly limit; scheduler disabled.")

    # else array is normally returned
    else:

        # show the computation result
        print ("  Auto-scheduling runtime = %s [minute]" % out_c) 
        print ("  Total volume = %s [L]" % int(sum(out_c) * actuator_c))
        print ("  Saved water = %s [L]" % int(weeklyoutput_c - sum(out_c) * actuator_c))