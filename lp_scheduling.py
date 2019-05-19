#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import the linear programming module
import pulp

# function to generate runtime distribution
def compute(interval1, interval2, sensor_reading, actuator_spec, cycle_output, interval_output):

    # calculate how many time interval2 will be activated in 1 interval1
    activation_time = int(interval1 / interval2)

    # do sanity check to see if the requirement for runtime distribution was met
    if ((activation_time == len(sensor_reading)) and (sum(sensor_reading) <= cycle_output)):

        # initialize the problem as a model with maximization target
        model = pulp.LpProblem("Runtime distribution", pulp.LpMaximize)
        # initialize the array to store the runtime distribution
        runtime1 = [0] * activation_time
        runtime2 = [0] * activation_time
        # initialize the array to store the balanced distribution calculation
        runtime3 = [interval_output] * activation_time

        # for every element in the runtime1 array
        for i in range(len(runtime1)):

            # initialize it with a lower limit of zero
            runtime1[i] = pulp.LpVariable(str(i), lowBound = 0, cat = 'Continuous')

        # for every element in the runtime2 array
        for j in range(len(runtime2)):

            # multiply the element with the actuator_spec
            runtime2[j] = runtime1[j] * actuator_spec

        # for every element in the runtime3 array
        for k in range(len(runtime3)):

            # calculate the difference
            runtime3[k] -= sensor_reading[k]

        # set the objective function
        model += sum(runtime2), "Runtime"
        # set the output constraint
        model += sum(runtime2) <= (cycle_output - sum(sensor_reading))
        # for every element in the runtime1
        for l in range(len(runtime1)):

            # set the input constraint in range of sensor_reading[k]
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
        if (activation_time != len(sensor_reading)):

            # return true; user need to rework on their input
            return True

        # when total of sensor reading is over the limit
        if (sum(sensor_reading) <= cycle_output):

            # return false; schedule cannot be created
            return False