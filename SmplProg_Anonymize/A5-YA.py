#!/usr/bin/env python3
"""
Created by Takao Murakami Jun 18, 2019.

Description: 
    Yamaoka anonymization (cheating anonymization). 
    It randomly shuffles user IDs and replaces the whole traces.

Usage:
    A5-YA.py [Testing Trace (in)] [Anonymized Trace (out)]
"""
import numpy as np
import csv
import sys

################################# Parameters ##################################
# Number of users
UserNum = 1000

#sys.argv = ["A5-YA.py", "../Data/testtraces_TK.csv", "../Data_Anonymized/testtraces_TK_A5.csv"]
if len(sys.argv) < 3:
    print("Usage:",sys.argv[0],"[Testing Trace (in)] [Anonymized Trace (out)]" )
    sys.exit(0)

# Testing trace file (input)
TestTraceFile = sys.argv[1]
# Anonymized trace file (output)
AnoTraceFile = sys.argv[2]

#################################### Main #####################################
# Fix a seed
np.random.seed(1)

# Randomly shuffled user ID --> rand_id 
rand_id = np.arange(UserNum)
np.random.shuffle(rand_id)

# Read a testing trace file --> out_lst
out_lst = []
f = open(TestTraceFile, "r")
reader = csv.reader(f)
next(reader)
for lst in reader:
#    user_id = int(lst[0])
    user_id = int(lst[0])-1
    time_id = int(lst[1])
    reg_id = int(lst[2])
#    out_lst.append([rand_id[user_id], time_id, reg_id])
    out_lst.append([rand_id[user_id]+1, time_id, reg_id])
f.close()

# Sort out_lst in ascending order of shuffled user ID
out_lst.sort(key=lambda tup: tup[0], reverse=False)

# Output anonymized traces
g = open(AnoTraceFile, "w")
print("user_id,time_id,reg_id", file=g)
writer = csv.writer(g, lineterminator="\n")
for lst in out_lst:
    writer.writerow(lst)
g.close()
