"""
[Smart Tomato Farm Problem]

    Tomato farm is divided into 3 areas which is a, b and c due to the limitation on area covered by
    individual sprinkler. To find how long we should run the sprinkler, a heuristic
    calculation for auto-scheduling methodology is developed.

    #############
    #       # a #        area (a):  5 [m^2]
    #   b   #####        area (b): 30 [m^2]
    #       #            area (c): 10 [m^2]
    ######### 
    #   C   # 
    #########

    We assume that each areas have only one sprinkler and the water output are;
    - area (a) have  2 [L/minutes] 
    - area (b) have 12 [L/minutes]
    - area (c) have  4 [L/minutes]

    We assume one tomato tree that take 0.5 [m^2] of space need 3.4 [L] in one day, thus;
    - area (a) need 34.0 [L]
    - area (b) need 81.6 [L]
    - area (c) need 27.2 [L]

    We assume that the the system designer installed weather forecast sensor to calculate
    how much of water needed for irrigation. The precipitation for 1 week is;
    - Sunday: 0 [mm]
    - Monday: 0 [mm]
    - Teusday: 7 [mm]
    - Wednesday: 0 [mm]
    - Thursday: 28 [mm]
    - Friday: 2 [mm]
    - Saturday: 0 [mm]
    In Array formatting: [0, 0, 7, 0, 28, 2, 0]
    Liter = (x [mm] / 1000) [m] * y [m^2] * 1000 [L/m^3]  

    Extra parameter to create the schedule;
    - the schedule span for 1 week
    - sprinkler operate once for 1 day

"""

# function to find the optimized sprinkler output based on the weather forecast
def heuristic_as(sensor_reading, cycle_output, interval_output, activation_time, actuator_spec, out):

    # if rainfall from the weather forecast didn't exceed the target_out
    if (sum(sensor_reading) <= cycle_output):

        # create the forecast scheduling
        for i in range(activation_time):

            # find the output needed at that interval
            out.append(interval_output - sensor_reading[i])

        # normalize the array from negative element
        for i in range(activation_time): 

            # initialize counter
            j = 0
            k = 0

            # if the element is negative
            if (out[i] < 0):

                # loop until the negative element spread out
                while True:

                    try:

                        # increase the counter
                        j += 1

                        # if the next element in the array is not negative and bigger or equal with the current element
                        if ((out[i + j] > 0) and (out[i + j] >= -out[i])):

                            # update the next element
                            out[i + j] = out[i + j] + out[i]
                            # swap the current element with 0
                            out[i] = 0
                            # break from the while loop
                            break

                        # else if the next element in the array is not negative and smaller than the current element
                        elif ((out[i + j] > 0) and (out[i + j] < -out[i])):

                            # update the current element
                            out[i] = out[i + j] + out[i]
                            # swap the next element with 0
                            out[i + j] = 0

                    except:

                        # increase the counter
                        k -= 1

                        # if the next element in the array is not negative and bigger or equal with the current element
                        if ((out[i + k] > 0) and (out[i + k] >= -out[i])):

                            # update the next element
                            out[i + k] = out[i + k] + out[i]
                            # swap the current element with 0
                            out[i] = 0
                            # break from the while loop
                            break

                        # else if the next element in the array is not negative and smaller than the current element
                        elif ((out[i + k] > 0) and (out[i + k] < -out[i])):

                            # update the current element
                            out[i] = out[i + k] + out[i]
                            # swap the next element with 0
                            out[i + k] = 0

        # divide out which is [L] with actuators_s which is [L/h] and multiply by 60 to get minutes
        print ("  Sprinkler runtime: %s [minute]" % [int(i / actuator_spec * 60) for i in out])
        # total volume of water in [L]
        print ("  Total volume: %s [L]" % sum(out))

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
    sensor = [0, 0, 7, 0, 28, 2, 0]
    # calculate how many time sprinkler (interval2) will activate in 1 cycle (interval1)
    activation_time = int(interval1 / interval2)

    # meter square of area
    area_a = 5
    # actuators capability sprinkler is 20 [L/h]
    actuator_a = 20
    # rainfall in [L] based on meter square of area
    sensor_a = [(i * area_a) for i in sensor]
    # total output [L] that actuator (sprinkler) need to meet for every cycle
    totaloutput_a = 3.4 / 0.5 * area_a * interval1
    # spread the target output to each activation time
    dailyoutput_a = totaloutput_a / activation_time
    # initialize an empty array to store the time needed to reach the daily quota
    out_a = []
    # calculate the time needed
    heuristic_as(sensor_a, totaloutput_a, dailyoutput_a, activation_time, actuator_a, out_a)

    # meter square of area
    area_b = 30
    # actuators capability sprinkler is 120 [L/h]
    actuator_b = 120
    # rainfall in [L] based on meter square of area
    sensor_b = [(i * area_b) for i in sensor]
    # total output [L] that actuator (sprinkler) need to meet for every cycle
    totaloutput_b = 3.4 / 0.5 * area_b * interval1
    # spread the target output to each activation time
    dailyoutput_b = totaloutput_b / activation_time
    # initialize an empty array to store the time needed to reach the daily quota
    out_b = []
    # calculate the time needed
    heuristic_as(sensor_b, totaloutput_b, dailyoutput_b, activation_time, actuator_b, out_b)

    # meter square of area
    area_c = 10
    # actuators capability sprinkler is 40 [L/h]
    actuator_c = 40
    # rainfall in [L] based on meter square of area
    sensor_c = [(i * area_c) for i in sensor]
    # total output [L] that actuator (sprinkler) need to meet for every cycle
    totaloutput_c = 3.4 / 0.5 * area_c * interval1
    # spread the target output to each activation time
    dailyoutput_c = totaloutput_c / activation_time
    # initialize an empty array to store the time needed to reach the daily quota
    out_c = []
    # calculate the time needed
    heuristic_as(sensor_c, totaloutput_c, dailyoutput_c, activation_time, actuator_c, out_c)