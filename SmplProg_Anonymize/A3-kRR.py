#!/usr/bin/env python3
"""
Created by Takao Murakami Jun 12, 2019 (last updated: Aug 22, 2019).

Description: 
    k-RR(epsilon) (k-ary randomized response) [Kairouz+, ICML16]. 
    It perturbs (adds noise to) a region using the k-ary randomized response 
    with parameter (privacy budget) epsilon assigned for each region.

Reference:
    P.Kairouz et al., Discrete Distribution Estimation under Local Privacy, ICML, 2016.

Usage:
    A3-kRR.py [Original Trace (in)] [Anonymized Trace (out)] ([epsilon (default:0.1)])
"""
import numpy as np
import math
import csv
import sys

################################# Parameters ##################################
# Number of regions on the x-axis
NumRegX = 32
# Number of regions on the y-axis
NumRegY = 32

#sys.argv = ["A3-kRR.py", "../Data/PWSCup2019_Osaka/orgtraces_team001_data01_IDP.csv", "../Data_Anonymize/anotraces_team001_data01_IDP_A3.csv", 8]
if len(sys.argv) < 3:
    print("Usage:",sys.argv[0],"[Original Trace (in)] [Anonymized Trace (out)] ([epsilon (default:0.1)])" )
    sys.exit(0)

# Original trace file (input)
OrgTraceFile = sys.argv[1]
# Anonymized trace file (output)
AnoTraceFile = sys.argv[2]

# Parameter epsilon
Epsilon = 0.1
if len(sys.argv) >= 4:
    Epsilon = float(sys.argv[3])

#################################### Main #####################################
# Fix a seed
np.random.seed(1)

# Number of regions --> k
k = NumRegX * NumRegY
# Probability of sending a true region id --> p
p = math.exp(Epsilon) / (k - 1 + math.exp(Epsilon))
# Probability of sending a false region id --> q
q = 1 / (k - 1 + math.exp(Epsilon))

# Read the original trace file and output anonymized traces
f = open(OrgTraceFile, "r")
g = open(AnoTraceFile, "w")
reader = csv.reader(f)
next(reader)
#print("user_id,time_id,reg_id", file=g)
print("reg_id", file=g)
writer = csv.writer(g, lineterminator="\n")
home_reg_id = -1
for lst in reader:
    user_id = int(lst[0])
    time_id = int(lst[1])
#    reg_id = int(lst[2])
    reg_id = int(lst[2])-1
    # Anonymized region ID --> ano_reg_id
    rand = np.random.rand()
    # Send a true region ID
    if rand < p:
        ano_reg_id = reg_id
        ano_reg_id += 1
    # Send a false region ID
    else:
        rand -= p
        shift_id = int(rand / q)
        ano_reg_id = shift_id
        if ano_reg_id >= reg_id:
            ano_reg_id += 1
        ano_reg_id += 1
#    out_lst = [user_id, time_id, ano_reg_id]
    out_lst = [ano_reg_id]
    writer.writerow(out_lst)
f.close()
g.close()
