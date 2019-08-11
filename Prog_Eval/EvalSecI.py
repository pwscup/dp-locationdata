#!/usr/bin/env python3
"""
Created by Takao Murakami Jun 18, 2019 (last updated: Aug 11, 2019).

Description: 
    Evaluate security (ID-disclosure).

Usage:
    EvalSecR.py [Pseudo-ID Table (in)] [Estimated Table (in)]
"""
import csv
import sys

################################# Parameters ##################################
#sys.argv = ["EvalSecI.py", "../Data_Anonymize_Shuffle/ptable_team001_data01_IDP.csv", "../Data_IDDisclose/etable_team020-001_data01_IDP.csv"]
if len(sys.argv) < 3:
    print("Usage:",sys.argv[0],"[Pseudo-ID Table (in)] [Estimated Table (in)]" )
    sys.exit(0)

# Number of users
UserNum = 2000

# Pseudo-ID table file (input)
PTableFile = sys.argv[1]
# Estimated table file (input)
ETableFile = sys.argv[2]

#################################### Main #####################################
# Initialization
ptable = {}
etable = {}

# Read a pseudo-ID table & estimated table
f = open(PTableFile, "r")
g = open(ETableFile, "r")
reader = csv.reader(f)
next(reader)
g.readline()
for lst in reader:
    # Read a pseudo-ID table
#    user_id = int(lst[0])
    user_id = int(lst[0])-UserNum
    ptable[user_id] = int(lst[1])
    # Read an estimated table
    etable[user_id] = int(g.readline())
f.close()
g.close()

## Read an estimated table
#f = open(ETableFile, "r")
#reader = csv.reader(f)
#next(reader)
#for lst in reader:
#    user_id = int(lst[0])
#    user_id = int(lst[0])-UserNum
#    etable[user_id] = int(lst[1])
#f.close()

# Calculate the re-identification rate --> reid_rate
reid_rate = 0
for i in ptable:
    if ptable[i] == etable[i]:
        reid_rate += 1
reid_rate /= len(ptable)

# Reverse reid_rate so that 1 (resp. 0) is the best (resp. worst) score --> avg_rscore
avg_rscore = 1 - reid_rate

print(avg_rscore)
