# Gear-Selection
Optimized for the Vex competition, gear selection program to find all possable combinations of gears in multi stage gear trains that produce a desired RPM rate.
Prompts user for the desired output RPM, the range of RPMs to consider, the number of stages desired, and any modifications to the available gear list. Returns a list of all gears that form a geartrain matching the input data, and a diagram showing how the gears should be set up. 
Considers each motor type of vex motors, and can consider gear trains containing stages of gears mixed with stages of sprockets. 


How to read output:

[G1, G2, G3, G4, G5, G6]

Motor:       [M]
Stage 1:     [G1] [G2]
Stage 2:          [G3] [G4]
Stage 3:               [G5] [G6]
Output:                      [O]

In diagram, shafts connect vertically, teeth mesh horizontally
