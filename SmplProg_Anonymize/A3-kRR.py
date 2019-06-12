#!/usr/bin/env python3
"""
Created by Takao Murakami Jun 12, 2019.

Description: 
    k-RR(epsilon) (k-ary randomized response) [Kairouz+, ICML16]. 
    It perturbs (adds noise to) a region using the k-ary randomized response 
    with parameter (privacy budget) epsilon assigned for each region.

Reference:
    P.Kairouz et al., Discrete Distribution Estimation under Local Privacy, ICML, 2016.

Usage:
    A3-kRR.py [Testing Trace] [Anonymized Trace] ([epsilon (default:0.1)]
"""
import numpy as np
import math
import csv
import sys

################################# Parameters ##################################
# Number of regions in the x-term
NumRegX = 32
# Number of regions in the y-term
NumRegY = 32

#sys.argv = ["A3-kRR.py", "../Data/testtraces_TK.csv", "../Data_Anonymized/testtraces_TK_A3-kRR.csv", 6]
if len(sys.argv) < 3:
    print("Usage:",sys.argv[0],"[Testing Trace] [Anonymized Trace] ([epsilon (default:0.1)])" )
    sys.exit(0)

# Testing trace file (input)
TestTraceFile = sys.argv[1]
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

# Read a testing trace file and output anonymized traces
f = open(TestTraceFile, "r")
g = open(AnoTraceFile, "w")
reader = csv.reader(f)
next(reader)
print("user_id,time,reg_id", file=g)
writer = csv.writer(g, lineterminator="\n")
for lst in reader:
    user_id = int(lst[0])
    tim = lst[1]
#    reg_id = int(lst[2])
    reg_id = int(lst[2])-1
    # Anonymized region ID --> ano_reg_id
    rand = np.random.rand()
    # Send a true region ID
    if rand < p:
        ano_reg_id = reg_id
    # Send a false region ID
    else:
        rand -= p
        shift_id = int(rand / q)
        ano_reg_id = shift_id
        if ano_reg_id >= reg_id:
            ano_reg_id += 1
#    out_lst = [user_id, tim, ano_reg_id]
    out_lst = [user_id, tim, ano_reg_id+1]
    writer.writerow(out_lst)
f.close()
g.close()
