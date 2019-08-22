#!/usr/bin/env python3
"""
Created by Takao Murakami Jun 17, 2019 (last updated: Aug 22, 2019).

Description: 
    Random trace inference (tracking).

Usage:
    T1-rand.py [Reference Trace (in)] [Anonymized Trace (in)] [Estimated Trace (out)]
"""
import numpy as np
import csv
import sys

################################# Parameters ##################################
# Number of users
UserNum = 2000
# Number of regions on the x-axis
NumRegX = 32
# Number of regions on the y-axis
NumRegY = 32

#sys.argv = ["T1-rand.py", "../Data/PWSCup2019_Osaka/reftraces_team001_data01_IDP.csv", "../Data_Anonymize_Shuffle/pubtraces_team001_data01_IDP.csv", "../Data_TraceInfer/etraces_team020-001_data01_IDP.csv"]
if len(sys.argv) < 3:
    print("Usage:",sys.argv[0],"[Reference Trace (in)] [Anonymized Trace (in)] [Estimated Trace (out)]" )
    sys.exit(0)

# Reference trace file (input)
RefTraceFile = sys.argv[1]
# Anonymized trace file (input)
AnoTraceFile = sys.argv[2]
# Estimated trace file (output)
EstTraceFile = sys.argv[3]

#################################### Main #####################################
# Fix a seed
#np.random.seed(1)

# Number of regions --> k
k = NumRegX * NumRegY

# Output the estimated trace
f = open(AnoTraceFile, "r")
g = open(EstTraceFile, "w")
reader = csv.reader(f)
next(reader)
#print("user_id,time_id,reg_id", file=g)
print("reg_id", file=g)
writer = csv.writer(g, lineterminator="\n")
for lst in reader:
#    user_id = int(lst[0])
#    user_id = int(lst[0])-1
    user_id = int(lst[0])-UserNum-1
    time_id = int(lst[1])

#    est_reg_id = int(np.random.rand() * k)
    est_reg_id = int(np.random.rand() * k)
#    lst = [user_id,time_id,est_reg_id]
#    lst = [user_id+1,time_id,est_reg_id+1]
    lst = [est_reg_id+1]
    writer.writerow(lst)

f.close()
g.close()
