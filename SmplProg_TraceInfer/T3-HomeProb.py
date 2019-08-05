#!/usr/bin/env python3
"""
Created by Takao Murakami Jun 18, 2019 (last updated: Aug 5, 2019).

Description: 
    Trace inference (tracking) attack based on home-probability vectors. 
    It performs the following processes:
    2) Train a home-probability vector, which is composed of the probability 
       for each region at 8:00-8:59, for each user by using reference traces.
    2) Re-identify each anonymized trace by choosing a user with the highest likelihood.
       (For generalized regions, we average the likelihood over randomly chosen 
        L regions. For location hiding (deletion), we don't update the likelihood.)
    3) Infer each trace by de-obfuscating the re-identified trace.
       (For noise, we output the noisy location as is. For generalization, 
        we randomly choose a region from generalized regions. For location 
        hiding (deletion), we randomly choose a region from all regions.)

Usage:
    T2-VisitProb.py [Reference Trace (in)] [Anonymized Trace (in)] [Estimated Trace (out)]
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
# Number of time instants per day
NumTimeIns = 20
# End of time ID at 8:00-8:59
EndTime = 62
# Start time in original traces
OrgStartTime = 41
# Smallest probability
Delta = 1e-8
# Maximum number of regions for generalization in re-identification (for efficiency)
L = 10

#sys.argv = ["T3-HomeProb.py", "../Data/PWSCup2019_Osaka/reftraces_team001_data01_IDP.csv", "../Data_Anonymize_Shuffle/pubtraces_team001_data01_IDP_A1.csv", "../Data_TraceInfer/etraces_team001_data01_IDP_A1-T3.csv"]
if len(sys.argv) < 3:
    print("Usage:",sys.argv[0],"[Reference Trace (in)] [Anonymized Trace (in)] [Estimated Trace (out)]" )
    sys.exit(0)

# Reference trace file (input)
RefTraceFile = sys.argv[1]
# Anonymized trace file (input)
AnoTraceFile = sys.argv[2]
# Estimated trace file (output)
EstTraceFile = sys.argv[3]

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
        time_id = int(lst[1])-1
        reg_id = int(lst[2])-1

        # Continue if time is between 9:00 and 16:59
        hour = int((time_id % NumTimeIns) / 2) + 8
        if hour >= 9:
#        if hour >= 9 and hour < 17:
            continue
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
    reidentified = np.zeros(UserNum)
    est_table = {}

    logdelta = math.log(Delta)

    # Read an anonymized trace file
    f = open(AnoTraceFile, "r")
    reader = csv.reader(f)
    next(reader)

    # Re-identification attack
    pse_id_pre = -1
    time_id = 1
    for lst in reader:
#        pse_id = int(lst[0])
        pse_id = int(lst[0])-1
        time_id = int(lst[1])-1
        reg_id_lst = lst[2].split(" ")

        # Continue if time is between 9:00 and 16:59
        hour = int((time_id % NumTimeIns) / 2) + 8
        if hour >= 9:
#        if hour >= 9 and hour < 17:
            continue
        # For a new user
        if pse_id != pse_id_pre:
            # Initialization
            for i in range(UserNum):
                # Do not reidentify multiple traces as the same user
                if reidentified[i] == 1:
                    logpost[i] = -sys.float_info.max
                else:
                    logpost[i] = 0
            time_id = 1

        # Number of region IDs --> reg_id_num
        reg_id_num = len(reg_id_lst)

        # Update the log-posterior --> logpost
        # Noise
        if reg_id_num == 1 and reg_id_lst[0] != "*":
#            reg_id = int(reg_id_lst[0])
            reg_id = int(reg_id_lst[0])-1
            # Update the log-posterior for each user --> logpost
            for i in range(UserNum):
                # Continue if the user i has been already reidentified
                if reidentified[i] == 1:
                    continue
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
                # Continue if the user i has been already reidentified
                if reidentified[i] == 1:
                    continue
                # Calculate the average likelihood over the chosen regions --> avg_likeli
                avg_likeli = 0
                for r in range(cho_reg_id_num):
                    # Randomly chosen region ID --> reg_id
                    reg_id = int(reg_id_lst[cho_index[r]])-1
                    # Update the average likelihood
                    if (i, reg_id) in visit_vec:
                        avg_likeli += visit_vec[i, reg_id] / cho_reg_id_num
                    else:
                        avg_likeli += Delta / cho_reg_id_num
                # Add the log of the average likelihood to logpost
                logpost[i] += math.log(avg_likeli)

        # End of the trace at 8:00-8:59
        if time_id == EndTime - 1:
            # Choose a user whose log-postetior is the highest --> re_id
            re_id = np.argmax(logpost)
            # Update the estimated table --> est_table
            est_table[pse_id] = re_id
            # Set re_id as a reidentified user --> reidentified
            reidentified[re_id] = 1

        # Save user_id & reg_id --> pse_id_pre, reg_id_pre
        pse_id_pre = pse_id
        # Increase time_id --> time_id
        time_id += 1
    f.close()
    
    return est_table

############################ De-obfuscation attack ############################
# [input1]: est_table ({pse_id: re_id})
# [input2]: visit_vec ({(user_id, reg_id): visit_prob})
# [output1]: est_trace ({(user_id, time_id): re_id})
def Deobfuscate(est_table, visit_vec):
    # Initialization
    est_trace = {}
    
    # Number of regions --> r_num
    r_num = NumRegX * NumRegY

    # Read an anonymized trace file
    f = open(AnoTraceFile, "r")
    reader = csv.reader(f)
    next(reader)

    # De-obfuscation attack
    pse_id_pre = -1
    time_id = OrgStartTime
    for lst in reader:
#        pse_id = int(lst[0])
        pse_id = int(lst[0])-1
        reg_id_lst = lst[2].split(" ")

        # User ID corresponding to pse_id --> user_id
        user_id = est_table[pse_id]

        # For a new user
        if pse_id != pse_id_pre:
            # Initialization
            time_id = OrgStartTime

        # Number of region IDs --> reg_id_num
        reg_id_num = len(reg_id_lst)

        # De-obfuscate a trace --> est_trace[(user_id,time_id)]
        # Noise
        if reg_id_num == 1 and reg_id_lst[0] != "*":
            # Choose the noisy location as is --> est_trace[(user_id,time_id)]
#            est_trace[(user_id,time_id)] = int(reg_id_lst[0])
            est_trace[(user_id,time_id)] = int(reg_id_lst[0])-1
        # Generalization
        elif reg_id_num >= 2:
            # Randomly choose a region from generalized regions
            cho_index = np.arange(reg_id_num)
            np.random.shuffle(cho_index)
            est_trace[(user_id,time_id)] = int(reg_id_lst[cho_index[0]])-1
        # location hiding (deletion)
        else:
            # Randomly choose a region from all regions
            all_reg_id_from_zero = np.arange(r_num)
            np.random.shuffle(all_reg_id_from_zero)
            est_trace[(user_id,time_id)] = all_reg_id_from_zero[0]

        # Save pse_id --> pse_id_pre
        pse_id_pre = pse_id
        # Increase time_id --> time_id
        time_id += 1
    f.close()
    
    return est_trace

#################################### Main #####################################
# Fix a seed
#np.random.seed(1)

# Train a visit vector & transition matrix for each user
visit_vec = TrainVisitTrans()

# Re-identification attack
est_table = Reidentify(visit_vec)

# De-obfuscation attack
est_trace = Deobfuscate(est_table, visit_vec)

# Output the estimated trace
f = open(AnoTraceFile, "r")
g = open(EstTraceFile, "w")
reader = csv.reader(f)
next(reader)
print("user_id,time_id,reg_id", file=g)
writer = csv.writer(g, lineterminator="\n")
for lst in reader:
#    user_id = int(lst[0])
    user_id = int(lst[0])-1
    time_id = int(lst[1])
    
    est_reg_id = est_trace[(user_id,time_id)]
#    lst = [user_id,time_id,est_reg_id]
    lst = [user_id+1,time_id,est_reg_id+1]
    writer.writerow(lst)

f.close()
g.close()
