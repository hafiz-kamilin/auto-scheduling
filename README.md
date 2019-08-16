# Auto-Scheduling based on Linear Programming Method

## Introduction

<p align = "center">
  <img src = "https://raw.githubusercontent.com/hafiz-kamilin/auto-scheduling/master/pictures/1.png" width = "900" height = "350"/>
</p>

This is an example concept that show IoT type of sensors and actuators can be scheduled automatically based on parameters and constraints specified by the system designer. The schedule load distribution is optimized by using the Linear Programming method.

## Test run

1. Assuming Python 3 programming environment already configured by the user; execute
   - `pip install pulp` on Windows with administrative right or
   - `sudo pip install pulp` on Linux.
2. Execute `smartfarm_problem.py`, the result will change based on randomized weather forecast.

## Note

For generalized example, check the [./modules/linear_programming.py](https://github.com/hafiz-kamilin/auto-scheduling/blob/master/modules/linear_programming.py) and [./modules/random_generator.py](https://github.com/hafiz-kamilin/auto-scheduling/blob/master/modules/random_generator.py) to see the Python modules implementation.

## Acknowledgement

This work was partially supported by Interface Corporation, Japan.
