#!/usr/bin/env python3
"""
Created by Takao Murakami Jun 18, 2019 (last updated: Jun 29, 2019).

Description: 
    Evaluate a security score (tracking).

Usage:
    EvalSecT.py [Testing Trace (in)] [Estimated Trace (in)]
"""
import numpy as np
import math
import csv
import sys

################################# Parameters ##################################
# Minimum of y (latitude)
MIN_Y = 35.65
# Maximum of y (latitude)
MAX_Y = 35.75
# Minimum of x (longitude)
MIN_X = 139.68
# Maximum of x (longitude)
MAX_X = 139.8
# Number of regions in the x-term
NumRegX = 32
# Number of regions in the y-term
NumRegY = 32
# Minimum distance (km) for a score value of zero
MinDisZeroScore = 1

#sys.argv = ["EvalSecT.py", "Data/testtraces_TK.csv", "Data_Tracked/etraces_TK_A2-T2.csv"]
if len(sys.argv) < 3:
    print("Usage:",sys.argv[0],"[Testing Trace (in)] [Estimated Trace (in)]" )
    sys.exit(0)

# Testing trace file (input)
TestTraceFile = sys.argv[1]
# Estimated trace file (input)
EstTraceFile = sys.argv[2]

########## Calculate a security loss (tracking) between two regions ###########
# [input1]: reg_id1
# [input2]: reg_id2
# [input3]: xc
# [input4]: yc
# [output1]: tloss
def CalTLoss(reg_id1, reg_id2, xc, yc):
    # Region IDs (with zero start) --> reg_id1, reg_id2
    reg_id1 -= 1
    reg_id2 -= 1

    # Calculate y_id1, x_id1, y_id2, x_id2
    y_id1 = int(reg_id1 / NumRegX)
    x_id1 = reg_id1 % NumRegX
    y_id2 = int(reg_id2 / NumRegX)
    x_id2 = reg_id2 % NumRegX

    # Euclidean distance (km) between reg_id1 & reg_id2 --> dist_km
    # 1 degree of latitude (resp. longitude in TK) = 111 km (resp. 91 km)
    dist_y_km = (yc[y_id1] - yc[y_id2]) * 111
    dist_x_km = (xc[x_id1] - xc[x_id2]) * 91
    dist_km = math.sqrt(dist_y_km**2 + dist_x_km**2)
    
    if dist_km > MinDisZeroScore:
        tloss = 0
    else:
        tloss = 1 - dist_km / MinDisZeroScore

    return tloss

#################################### Main #####################################
# Initialization
test_trace = {}
est_trace = {}

# Read a testing trace file --> test_trace
f = open(TestTraceFile, "r")
reader = csv.reader(f)
next(reader)
for lst in reader:
    user_id = int(lst[0])
    time_id = int(lst[1])
    reg_id = int(lst[2])
    test_trace[(user_id, time_id)] = reg_id
f.close()

# Read an estimated trace file --> est_trace
f = open(EstTraceFile, "r")
reader = csv.reader(f)
next(reader)
for lst in reader:
    user_id = int(lst[0])
    time_id = int(lst[1])
    reg_id = int(lst[2])
    est_trace[(user_id, time_id)] = reg_id
f.close()

# Calculate the center of each region (NumRegX x NumRegY) --> xc, yc
xc = np.zeros(NumRegX)
yc = np.zeros(NumRegY)
x_width = (MAX_X - MIN_X) / NumRegX
y_width = (MAX_Y - MIN_Y) / NumRegY

for i in range(NumRegX):
    xc[i] = MIN_X + x_width * i + x_width / 2
for i in range(NumRegY):
    yc[i] = MIN_Y + y_width * i + y_width / 2

# Calculate the average security score (tracking) --> avg_tloss
avg_tloss = 0
for (user_id, time_id) in test_trace:
    reg_id1 = test_trace[(user_id, time_id)]
    reg_id2 = est_trace[(user_id, time_id)]
    avg_tloss += CalTLoss(reg_id1, reg_id2, xc, yc)
avg_tloss /= len(test_trace)

# Revserse avg_tloss so that 1 (resp. 0) is the best (resp. worst) score --> avg_tscore
avg_tscore = 1 - avg_tloss

print(avg_tscore)
