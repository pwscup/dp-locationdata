#!/usr/bin/env python3
"""
Created by Takao Murakami Jun 17, 2019.

Description: 
    Re-identification attack based on ML (Maximum Likelihood) estimation for 
    transition matrices and the Bayes decision rule [Murakami+, TrustCom15]. 
    It performs the following processes:
    1) Train transition matrices via the ML estimation. 
    2) Re-identify each trace by choosing a user with the highest posterior. 

Reference:
    T.Murakami et al., Group Sparsity Tensor Factorization for De-anonymization of Mobility Traces, TrustCom, 2015.

Usage:
    R3-MLTrans-Bayes.py [Training Trace (in)] [Anonymized Trace (in)] [Estimated Table (out)]
"""
import numpy as np
import math
import csv
import sys

################################# Parameters ##################################
# Number of users
UserNum = 1000
# Number of regions in the x-term
NumRegX = 32
# Number of regions in the y-term
NumRegY = 32
# Smallest probability
Delta = 1e-8

#sys.argv = ["R3-MLTrans-Bayes.py", "../Data/traintraces_TK.csv", "../Data_Anonymized_Shuffled/testtraces_TK_A1.csv", "../Data_Reidentified/etable_TK_A1-R2.csv"]
sys.argv = ["R3-MLTrans-Bayes.py", "../Data/testtraces_TK.csv", "../Data_Anonymized_Shuffled/testtraces_TK_A1.csv", "../Data_Reidentified/etable_TK_A1-R2.csv"]
if len(sys.argv) < 3:
    print("Usage:",sys.argv[0],"[Training Trace (in)] [Anonymized Trace (in)] [Estimated Table (out)]" )
    sys.exit(0)

# Training trace file (input)
TrainTraceFile = sys.argv[1]
# Anonymized trace file (input)
AnoTraceFile = sys.argv[2]
# Estimated table file (output)
EstTableFile = sys.argv[3]

########### Train a visit vector & transition matrix for each user ############
# [output1]: visit_vec ({(user_id, reg_id): visit_prob})
# [output2]: trans_mat ({(user_id, reg_id, reg_id_to): trans_prob})
def TrainVisitTrans():
    # Initialization
    visit_vec = {}
    trans_mat = {}
    visit_sum = np.zeros(UserNum)
    trans_sum = np.zeros((UserNum, NumRegX*NumRegY))

    # Read a training trace file
    f = open(TrainTraceFile, "r")
    reader = csv.reader(f)
    next(reader)
    # Compute visit counts & transition counts --> visit_vec, trans_mat
    user_id_pre = -1
    reg_id_pre = -1
    for lst in reader:
#        user_id = int(lst[0])
        user_id = int(lst[0])-1
        reg_id = int(lst[2])-1
        # Update visit counts
        visit_vec[(user_id, reg_id)] = visit_vec.get((user_id, reg_id), 0) + 1
        # Update transition counts
        if user_id == user_id_pre:
            trans_mat[(user_id, reg_id_pre, reg_id)] = trans_mat.get((user_id, reg_id_pre, reg_id), 0) + 1
        # Save user_id & reg_id --> user_id_pre, reg_id_pre
        user_id_pre = user_id
        reg_id_pre = reg_id
    f.close()
    
    # Compute a sum of visit counts for each user_id --> visit_sum
    for (user_id, reg_id), counts in sorted(visit_vec.items()):
        visit_sum[user_id] += counts
    # Compute a log of the visit probability --> visit_vec
    for (user_id, reg_id), counts in sorted(visit_vec.items()):
        visit_vec[user_id, reg_id] = counts / visit_sum[user_id]

    # Compute a sum of transition counts for each (user_id, reg_id) --> trans_sum
    for (user_id, reg_id, reg_id_to), counts in sorted(trans_mat.items()):
        trans_sum[user_id, reg_id] += counts
    # Compute a log of the transition probability --> trnas_mat
    for (user_id, reg_id, reg_id_to), counts in sorted(trans_mat.items()):
        trans_mat[user_id, reg_id, reg_id_to] = counts / trans_sum[user_id, reg_id]

    return visit_vec, trans_mat

###################### Bayesian re-identification attack ######################
# [input1]: visit_vec ({(user_id, reg_id): visit_prob})
# [input2]: trans_mat ({(user_id, reg_id, reg_id_to): trans_prob})
# [output1]: est_table ({pse_id: re_id})
def BayesReidentify(visit_vec, trans_mat):
    # Initialization
    logpost = np.zeros(UserNum)
    est_table = {}

    logdelta = math.log(Delta)

    # Read a anonymized trace file
    f = open(AnoTraceFile, "r")
    reader = csv.reader(f)
    next(reader)

    # Bayesian re-identification attack
    pse_id_pre = -1
    reg_id_pre = -1
    time = 1
    for lst in reader:
    #        user_id = int(lst[0])
        pse_id = int(lst[0])-1
        reg_id = int(lst[2])-1

        # Update the log-posterior --> logprob
        # For a new user
        if pse_id != pse_id_pre:
            # Initialization
            logpost = np.zeros(UserNum)
            time = 1
            # Update the log-posterior using visit_vec
            for i in range(UserNum):
                if (i, reg_id) in visit_vec:
                    logpost[i] += math.log(visit_vec[i, reg_id])
                else:
                    logpost[i] += logdelta
        # For a non-new user
        else:
            # Update the log-posterior using trans_mat
            for i in range(UserNum):
                if (i, reg_id_pre, reg_id) in trans_mat:
                    logpost[i] += math.log(trans_mat[i, reg_id_pre, reg_id])
                else:
                    logpost[i] += logdelta

        # End of the trace
        if time == T:
            # Choose a user whose log-postetior is the highest --> re_id
            re_id = np.argmax(logpost)
            # Update the estimated table --> est_table
            est_table[pse_id] = re_id

        # Save user_id & reg_id --> pse_id_pre, reg_id_pre
        pse_id_pre = pse_id
        reg_id_pre = reg_id
        # Increase time --> time
        time += 1
    f.close()
    
    return est_table

#################################### Main #####################################
# Fix a seed
np.random.seed(1)

# Compute the length of time --> T
T = int((len(open(AnoTraceFile).readlines()) - 1) / UserNum)


# Train a visit vector & transition matrix for each user
visit_vec, trans_mat = TrainVisitTrans()

# Bayesian re-identification attack
est_table = BayesReidentify(visit_vec, trans_mat)

# Output the estimated pseudo-ID table
g = open(EstTableFile, "w")
print("pse_id,user_id", file=g)
writer = csv.writer(g, lineterminator="\n")
for pse_id in range(UserNum):
#    lst = [pse_id, est_table[pse_id]]
    lst = [pse_id+1, est_table[pse_id]+1]
    writer.writerow(lst)
g.close()
