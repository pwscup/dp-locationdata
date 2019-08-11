#!/usr/bin/env python3
"""
Created by Takao Murakami Jun 17, 2019 (last updated: Aug 11, 2019).

Description: 
    Random ID-disclosure (re-identification).

Usage:
    I1-rand.py [Reference Trace (in)] [Anonymized Trace (in)] [Estimated Table (out)]
"""
import numpy as np
import csv
import sys

################################# Parameters ##################################
# Number of users
UserNum = 2000

#sys.argv = ["I1-rand.py", "../Data/PWSCup2019_Osaka/reftraces_team001_data01_IDP.csv", "../Data_Anonymize_Shuffle/pubtraces_team001_data01_IDP.csv", "../Data_IDDisclose/etable_team020-001_data01_IDP.csv"]
if len(sys.argv) < 3:
    print("Usage:",sys.argv[0],"[Reference Trace (in)] [Anonymized Trace (in)] [Estimated Table (out)]" )
    sys.exit(0)

# Reference trace file (input)
RefTraceFile = sys.argv[1]
# Anonymized trace file (input)
AnoTraceFile = sys.argv[2]
# Estimated table file (output)
EstTableFile = sys.argv[3]

#################################### Main #####################################
# Fix a seed
#np.random.seed(1)

# Randomly shuffled user ID --> rand_id 
rand_id = np.arange(UserNum)
np.random.shuffle(rand_id)

# Output the estimated pseudo-ID table
g = open(EstTableFile, "w")
#print("pse_id,user_id", file=g)
print("user_id", file=g)
writer = csv.writer(g, lineterminator="\n")
for i in range(UserNum):
#        lst = [i, rand_id[i]]
#    lst = [i+1, rand_id[i]+1]
#    lst = [i+UserNum+1, rand_id[i]+1]
    lst = [rand_id[i]+1]
    writer.writerow(lst)
g.close()