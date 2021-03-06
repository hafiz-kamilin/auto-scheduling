#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import the linear programming module
import pulp

# function to generate runtime distribution
def compute(interval, cycle, sensor_output, sensor_constraint, actuator_specification, interval_output, cycle_output):

    # calculate how many time cycle will be activated in 1 interval
    activation_time = int(interval / cycle)

    # do sanity check to see if the requirement for runtime distribution was met
    if ((activation_time == len(sensor_output)) and (sum(sensor_output) <= interval_output)):

        # initialize the problem as a model with maximization target
        model = pulp.LpProblem("Runtime distribution", pulp.LpMaximize)
        # initialize the array to store the runtime distribution
        runtime1 = [0] * activation_time
        runtime2 = [0] * activation_time
        # initialize the array to store the balanced distribution calculation
        runtime3 = [cycle_output] * activation_time

        # for every element in the runtime1 array
        for i in range(len(runtime1)):

            # initialize it with a lower limit of zero
            runtime1[i] = pulp.LpVariable(str(i), lowBound = 0, cat = 'Continuous')

        # for every element in the runtime2 array
        for j in range(len(runtime2)):

            # multiply the element with the actuator_spec
            runtime2[j] = runtime1[j] * actuator_specification

        # for every element in the runtime3 array
        for k in range(len(runtime3)):

            # calculate the difference
            runtime3[k] -= sensor_constraint[k]

        # set the objective function
        model += sum(runtime2), "Runtime"
        # set the output constraint
        model += sum(runtime2) <= (interval_output - sum(sensor_output))
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
        if (activation_time != len(sensor_constraint)):

            # return true; user need to rework on their input
            return True

        # when total of sensor reading is over the limit
        if (sum(sensor_output) <= interval_output):

            # return false; schedule cannot be created
            return False