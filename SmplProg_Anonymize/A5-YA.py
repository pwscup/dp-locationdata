#!/usr/bin/env python3
"""
Created by Takao Murakami Jun 18, 2019 (last updated: Aug 5, 2019).

Description: 
    YA(p) (Yamaoka anonymization; also called cheating anonymization or 
    shuffling anonymization). 
    It selects the first p (0 <= p <= 1) of all users as a subset of users, and 
    randomly shuffles user IDs and replaces the whole traces within the subset.

Usage:
    A5-YA.py [Original Trace (in)] [Anonymized Trace (out)] ([p (default:1)])
"""
import numpy as np
import csv
import sys

################################# Parameters ##################################
# Number of users
UserNum = 2000

#sys.argv = ["A5-YA.py", "../Data/PWSCup2019_Osaka/orgtraces_team001_data01_IDP.csv", "../Data_Anonymize/anotraces_team001_data01_IDP_A5.csv", "0.3"]
if len(sys.argv) < 3:
    print("Usage:",sys.argv[0],"[Original Trace (in)] [Anonymized Trace (out)] ([p (default:1)])" )
    sys.exit(0)

# Original trace file (input)
OrgTraceFile = sys.argv[1]
# Anonymized trace file (output)
AnoTraceFile = sys.argv[2]

# Parameter P
P = 1
if len(sys.argv) >= 4:
    P = float(sys.argv[3])

#################################### Main #####################################
# Fix a seed
np.random.seed(1)

# Number of users in the subset --> SubUserNum
SubUserNum = int(UserNum * P)

# Randomly shuffled user ID --> rand_id 
rand_id = np.arange(SubUserNum)
np.random.shuffle(rand_id)

# Read the original trace file --> out_lst
out_lst = []
f = open(OrgTraceFile, "r")
reader = csv.reader(f)
next(reader)
for lst in reader:
#    user_id = int(lst[0])
    user_id = int(lst[0])-1
    time_id = int(lst[1])
    reg_id = int(lst[2])
#    out_lst.append([rand_id[user_id], time_id, reg_id])
    if user_id < SubUserNum:
        out_lst.append([rand_id[user_id]+1, time_id, reg_id])
    else:
        out_lst.append([user_id+1, time_id, reg_id])
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
