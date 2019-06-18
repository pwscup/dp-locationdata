#!/usr/bin/env python3
"""
Created by Takao Murakami Jun 12, 2019 (last updated: Jun 17, 2019).

Description: 
    Output a testing trace as an anonymized trace; i.e., do nothing (except for shuffling IDs).

Usage:
    A1-none.py [Testing Trace (in)] [Anonymized Trace (out)]
"""
import numpy as np
import csv
import sys

################################# Parameters ##################################
#sys.argv = ["A1-none.py", "../Data/testtraces_TK.csv", "../Data_Anonymized/testtraces_TK_A1.csv"]
if len(sys.argv) < 3:
    print("Usage:",sys.argv[0],"[Testing Trace (in)] [Anonymized Trace (out)])" )
    sys.exit(0)

# Testing trace file (input)
TestTraceFile = sys.argv[1]
# Anonymized trace file (output)
AnoTraceFile = sys.argv[2]

#################################### Main #####################################
# Fix a seed
np.random.seed(1)

# Read a testing trace file and output anonymized traces
f = open(TestTraceFile, "r")
g = open(AnoTraceFile, "w")
reader = csv.reader(f)
next(reader)
print("user_id,time_id,reg_id", file=g)
writer = csv.writer(g, lineterminator="\n")
for lst in reader:
    user_id = int(lst[0])
    time_id = int(lst[1])
    reg_id = int(lst[2])
    out_lst = [user_id, time_id, reg_id]
    writer.writerow(lst)
f.close()
g.close()
