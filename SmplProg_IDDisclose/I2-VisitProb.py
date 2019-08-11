#!/usr/bin/env python3
"""
Created by Takao Murakami Jun 18, 2019 (last updated: Aug 11, 2019).

Description: 
    ID-disclosure (re-identification) attack based on visit-probability vectors.
    It performs the following processes:
    1) Train a visit-probability vector, which is composed of the probability 
       for each region, for each user by using reference traces.
    2) Re-identify each anonymized trace by choosing a user with the highest likelihood.
       (For efficiency, we choose each region in an anonymized trace with probability P.
        For generalized regions, we average the likelihood over randomly chosen 
        L regions. For location hiding (deletion), we don't update the likelihood.)

Usage:
    I2-VisitProb.py [Reference Trace (in)] [Anonymized Trace (in)] [Estimated Table (out)]
"""
import numpy as np
import math
import csv
import sys

################################# Parameters ##################################
# Number of users
UserNum = 2000
# Number of regions on the x-axis
NumRegX = 32
# Number of regions on the y-axis
NumRegY = 32
# Smallest probability
Delta = 1e-8
# Probability of choosing a region in an anonymized trace in re-identification (for efficiency)
P = 0.1
# Maximum number of regions for generalization in re-identification (for efficiency)
L = 10

#sys.argv = ["I2-VisitProb.py", "../Data/PWSCup2019_Osaka/reftraces_team001_data01_IDP.csv", "../Data_Anonymize_Shuffle/pubtraces_team001_data01_IDP.csv", "../Data_IDDisclose/etable_team020-001_data01_IDP.csv"]
if len(sys.argv) < 3:
    print("Usage:",sys.argv[0],"[Reference Trace (in)] [Anonymized Trace (in)] [Estimated Table (out)]" )
    sys.exit(0)

# Reference trace file (input)
RefTraceFile = sys.argv[1]
# Anonymized trace file (input)
AnoTraceFile = sys.argv[2]
# Estimated table file (output)
EstTableFile = sys.argv[3]

##################### Train a visit vector for each user ######################
# [output1]: visit_vec ({(user_id, reg_id): visit_prob})
def TrainVisitTrans():
    # Initialization
    visit_vec = {}
    visit_sum = np.zeros(UserNum)

    # Read a reference trace file
    f = open(RefTraceFile, "r")
    reader = csv.reader(f)
    next(reader)
    # Compute visit counts --> visit_vec
    for lst in reader:
#        user_id = int(lst[0])
        user_id = int(lst[0])-1
        reg_id = int(lst[2])-1
        # Update visit counts
        visit_vec[(user_id, reg_id)] = visit_vec.get((user_id, reg_id), 0) + 1
    f.close()
    
    # Compute a sum of visit counts for each user_id --> visit_sum
    for (user_id, reg_id), counts in sorted(visit_vec.items()):
        visit_sum[user_id] += counts
    # Compute a log of the visit probability --> visit_vec
    for (user_id, reg_id), counts in sorted(visit_vec.items()):
        visit_vec[user_id, reg_id] = counts / visit_sum[user_id]

    return visit_vec

########################## Re-identification attack ###########################
# [input1]: visit_vec ({(user_id, reg_id): visit_prob})
# [output1]: est_table ({pse_id: re_id})
def Reidentify(visit_vec):
    # Initialization
    logpost = np.zeros(UserNum)
    est_table = {}

    logdelta = math.log(Delta)

    # Read a anonymized trace file
    f = open(AnoTraceFile, "r")
    reader = csv.reader(f)
    next(reader)

    # Re-identification attack
    pse_id_pre = -1
    time_id = 1
    for lst in reader:
#        pse_id = int(lst[0])
#        pse_id = int(lst[0])-1
        pse_id = int(lst[0])-UserNum-1
        reg_id_lst = lst[2].split(" ")
        
        # For a new user
        if pse_id != pse_id_pre:
            # Initialization
            logpost = np.zeros(UserNum)
            time_id = 1

        # Choose a region with probability P
        rnd = np.random.rand()
        if rnd < P:
            # Number of region IDs --> reg_id_num
            reg_id_num = len(reg_id_lst)
    
            # Update the log-posterior --> logpost
            # Noise
            if reg_id_num == 1 and reg_id_lst[0] != "*":
    #            reg_id = int(reg_id_lst[0])
                reg_id = int(reg_id_lst[0])-1
                # Update the log-posterior for each user --> logpost
                for i in range(UserNum):
                    # Add the log-likelihood to logpost
                    if (i, reg_id) in visit_vec:
                        logpost[i] += math.log(visit_vec[i, reg_id])
                    else:
                        logpost[i] += logdelta
            # Generalization
            elif reg_id_num >= 2:
                # Randomly choose indexes of (at most) L regions --> cho_index
                cho_reg_id_num = min(L, reg_id_num)
                cho_index = np.arange(reg_id_num)
                np.random.shuffle(cho_index)
    
                # Update the log-posterior for each user --> logpost
                for i in range(UserNum):
                    # Calculate the average likelihood over the chosen regions --> avg_likeli
                    avg_likeli = 0
                    # For each of the chosen regions
                    for r in range(cho_reg_id_num):
                        # Chosen region ID --> reg_id
                        reg_id = int(reg_id_lst[cho_index[r]])-1
                        # Update the average likelihood
                        if (i, reg_id) in visit_vec:
                            avg_likeli += visit_vec[i, reg_id] / cho_reg_id_num
                        else:
                            avg_likeli += Delta / cho_reg_id_num
                    # Add the log of the average likelihood to logpost
                    logpost[i] += math.log(avg_likeli)

        # End of the trace
        if time_id == T:
            # Choose a user whose log-postetior is the highest --> re_id
            re_id = np.argmax(logpost)
            # Update the estimated table --> est_table
            est_table[pse_id] = re_id

        # Save pse_id --> pse_id_pre
        pse_id_pre = pse_id
        # Increase time_id --> time_id
        time_id += 1
    f.close()
    
    return est_table

#################################### Main #####################################
# Fix a seed
#np.random.seed(1)

# Compute the length of time --> T
T = int((len(open(AnoTraceFile).readlines()) - 1) / UserNum)

# Train a visit vector & transition matrix for each user
visit_vec = TrainVisitTrans()

# Re-identification attack
est_table = Reidentify(visit_vec)

# Output the estimated pseudo-ID table
g = open(EstTableFile, "w")
#print("pse_id,user_id", file=g)
print("user_id", file=g)
writer = csv.writer(g, lineterminator="\n")
for pse_id in range(UserNum):
#    lst = [pse_id, est_table[pse_id]]
#    lst = [pse_id+1, est_table[pse_id]+1]
#    lst = [pse_id+UserNum+1, est_table[pse_id]+1]
    lst = [est_table[pse_id]+1]
    writer.writerow(lst)
g.close()
