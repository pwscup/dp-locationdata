#!/usr/bin/env python3
"""
Created by Takao Murakami Jun 17, 2019.

Description: 
    Random re-identification.

Usage:
    R1-rand.py [Training Trace (in)] [Anonymized Trace (in)] [Estimated Table (out)]
"""
import numpy as np
import csv
import sys

################################# Parameters ##################################
# Number of users
UserNum = 1000

#sys.argv = ["R1-rand.py", "../Data/trainingtraces_TK.csv", "../Data_Anonymized_Shuffled/testtraces_TK_A1.csv", "../Data_Reidentified/etable_TK_A1-R1.csv"]
if len(sys.argv) < 3:
    print("Usage:",sys.argv[0],"[Training Trace (in)] [Anonymized Trace (in)] [Estimated Table (out)]" )
    sys.exit(0)

# Training trace file (input)
TrainTraceFile = sys.argv[1]
# Anonymized trace file (input)
AnoTraceFile = sys.argv[2]
# Estimated table file (output)
EstTableFile = sys.argv[3]

#################################### Main #####################################
# Fix a seed
np.random.seed(1)

# Randomly shuffled user ID --> rand_id 
rand_id = np.arange(UserNum)
np.random.shuffle(rand_id)

# Output the estimated pseudo-ID table
g = open(EstTableFile, "w")
print("pse_id,user_id", file=g)
writer = csv.writer(g, lineterminator="\n")
for i in range(UserNum):
#        lst = [i, rand_id[i]]
    lst = [i+1, rand_id[i]+1]
    writer.writerow(lst)
g.close()