#!/usr/bin/env python3
"""
Created by Takao Murakami Jun 18, 2019 (last updated: Aug 22, 2019).

Description: 
    Evaluate utility.

Usage:
    EvalSecT.py [Original Trace (in)] [Anonymized Trace (in)]
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
# Minimum distance (km) for a score value of one
MinDisOneScore = 2

#sys.argv = ["EvalUtil.py", "../Data/PWSCup2019_Osaka/orgtraces_team001_data01_IDP.csv", "../Data_Anonymize/anotraces_team001_data01_IDP_A5.csv"]
if len(sys.argv) < 3:
    print("Usage:",sys.argv[0],"[Original Trace (in)] [Anonymized Trace (in)]" )
    sys.exit(0)

# Original trace file (input)
OrgTraceFile = sys.argv[1]
# Anonymized trace file (input)
AnoTraceFile = sys.argv[2]

################ Calculate a utility loss between two regions #################
# [input1]: reg_id1
# [input2]: reg_id2
# [input3]: xc
# [input4]: yc
# [output1]: uloss
def CalUtil(reg_id1, reg_id2, xc, yc):
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
    
    if dist_km > MinDisOneScore:
        uloss = 1
    else:
        uloss = dist_km / MinDisOneScore

    return uloss

#################################### Main #####################################
# Initialization
test_trace = {}
ano_trace = {}

# Read the original trace file & anonymized trace file --> test_trace, ano_trace
f = open(OrgTraceFile, "r")
g = open(AnoTraceFile, "r")
reader = csv.reader(f)
next(reader)
g.readline()
for lst in reader:
    # Read the original trace file --> test_trace
    user_id = int(lst[0])
    time_id = int(lst[1])
    reg_id = int(lst[2])
    test_trace[(user_id, time_id)] = reg_id
    # Read an anonymized trace file --> ano_trace
    ano_reg_id = g.readline().rstrip("\n")
    ano_trace[(user_id, time_id)] = ano_reg_id
f.close()
g.close()

## Read an anonymized trace file --> ano_trace
#f = open(AnoTraceFile, "r")
#reader = csv.reader(f)
#next(reader)
#for lst in reader:
#    user_id = int(lst[0])
#    time_id = int(lst[1])
#    ano_reg_id = lst[2]
#    ano_trace[(user_id, time_id)] = ano_reg_id
#f.close()

# Calculate the center of each region (NumRegX x NumRegY) --> xc, yc
xc = np.zeros(NumRegX)
yc = np.zeros(NumRegY)
x_width = (MAX_X - MIN_X) / NumRegX
y_width = (MAX_Y - MIN_Y) / NumRegY

for i in range(NumRegX):
    xc[i] = MIN_X + x_width * i + x_width / 2
for i in range(NumRegY):
    yc[i] = MIN_Y + y_width * i + y_width / 2

# Calculate the average utility loss --> avg_uloss
avg_uloss = 0
for (user_id, time_id) in test_trace:
    reg_id1 = test_trace[(user_id, time_id)]

    reg_id2_lst = ano_trace[(user_id, time_id)].split(" ")
    # Number of region IDs --> reg_id2_num
    reg_id2_num = len(reg_id2_lst)

    # Noise
    if reg_id2_num == 1 and reg_id2_lst[0] != "*":
        reg_id2 = int(reg_id2_lst[0])
        avg_uloss += CalUtil(reg_id1, reg_id2, xc, yc)
    # Generalization
    elif reg_id2_num >= 2:
        for r in range(reg_id2_num):
            # Region ID --> reg_id
            reg_id2 = int(reg_id2_lst[r])
            avg_uloss += CalUtil(reg_id1, reg_id2, xc, yc) / reg_id2_num
    # Location hiding (deletion)
    else:
        avg_uloss += 1
avg_uloss /= len(test_trace)

# Reverse avg_uloss so that 1 (resp. 0) is the best (resp. worst) score --> avg_uscore
avg_uscore = 1 - avg_uloss

print(avg_uscore)
