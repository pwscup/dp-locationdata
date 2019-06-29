#!/usr/bin/env python3
"""
Created by Takao Murakami Jun 18, 2019 (last updated: Jun 29, 2019).

Description: 
    Evaluate a security score (re-identification).

Usage:
    EvalSecR.py [Pseudo-ID Table (in)] [Estimated Table (in)]
"""
import csv
import sys

################################# Parameters ##################################
#sys.argv = ["EvalSecR.py", "Data_Anonymized_Shuffled/ptable_TK_A2-2-2-0.5.csv", "Data_Reidentified/etable_TK_A2-R2.csv"]
if len(sys.argv) < 3:
    print("Usage:",sys.argv[0],"[Pseudo-ID Table (in)] [Estimated Table (in)]" )
    sys.exit(0)

# Pseudo-ID table file (input)
PTableFile = sys.argv[1]
# Estimated table file (input)
ETableFile = sys.argv[2]

#################################### Main #####################################
# Initialization
ptable = {}
etable = {}

# Read a pseudo-ID table
f = open(PTableFile, "r")
reader = csv.reader(f)
next(reader)
for lst in reader:
    user_id = int(lst[0])
    ptable[user_id] = int(lst[1])
f.close()

# Read an estimated table
f = open(ETableFile, "r")
reader = csv.reader(f)
next(reader)
for lst in reader:
    user_id = int(lst[0])
    etable[user_id] = int(lst[1])
f.close()

# Calculate the re-identification rate --> reid_rate
reid_rate = 0
for i in ptable:
    if ptable[i] == etable[i]:
        reid_rate += 1
reid_rate /= len(ptable)

# Revserse reid_rate so that 1 (resp. 0) is the best (resp. worst) score --> avg_rscore
avg_rscore = 1 - reid_rate

print(avg_rscore)
