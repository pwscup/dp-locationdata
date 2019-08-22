#!/usr/bin/env python3
"""
Created by Takao Murakami Jun 12, 2019 (last updated: Aug 22, 2019).

Description: 
    MRLH(mu_x, mu_y, lambda) (Merging Regions and Location Hiding; also called 
    Precision Reducing and Location Hiding) [Shokri+, S&P11]. 
    It generalizes (merges) a region by dropping lower mu_x (resp. mu_y) bit(s) 
    for the x-coordinate (resp. y-coordinate) expressed as a binary sequence, 
    and hides (deletes) a region with probability lambda.

Reference:
    R.Shokri et al., Quantifying Location Privacy, IEEE S&P, 2011.

Usage:
    A2-MRLH.py [Original Trace (in)] [Anonymized Trace (out)] ([mu_x (default:2)] [mu_y (default:2)] [lambda (default:0.5)])
"""
import numpy as np
import csv
import sys

################################# Parameters ##################################
# Number of users
UserNum = 2000
# Number of regions on the x-axis
NumRegX = 32
# Number of regions on the y-axis
NumRegY = 32
#sys.argv = ["A2-MRLH.py", "../Data/PWSCup2019_Osaka/orgtraces_team001_data01_IDP.csv", "../Data_Anonymize/anotraces_team001_data01_IDP_A2.csv", 1, 1, 0]
if len(sys.argv) < 3:
    print("Usage:",sys.argv[0],"[Original Trace] [Anonymized Trace] [Original Trace (in)] [Anonymized Trace (out)] ([mu_x (default:2)] [mu_y (default:2)] [lambda (default:0.5)])" )
    sys.exit(0)

# Original trace file (input)
OrgTraceFile = sys.argv[1]
# Anonymized trace file (output)
AnoTraceFile = sys.argv[2]

# Parameter mu_x
MuX = 2
if len(sys.argv) >= 4:
    MuX = int(sys.argv[3])
# Parameter mu_y
MuY = 2
if len(sys.argv) >= 5:
    MuY = int(sys.argv[4])
# Parameter lambda
Lambda = 0.5
if len(sys.argv) >= 6:
    Lambda = float(sys.argv[5])

###################### Make a generalization dictionary #######################
# [output1]: gen_dic ({reg_id: [reg_id, ...]})
def MakeGenDic():
    # Initialization
    pr_dic = {}
    gen_dic = {}

    # Precision reduction for NumRegX --> pre_num_reg_x
    pre_num_reg_x = NumRegX >> MuX

    # Make a precision-reduction dictionary --> pr_dic
    for reg_id in range(NumRegX * NumRegY):
        y_id = int(reg_id / NumRegX)
        x_id = reg_id % NumRegX
        # Precision reduction for y_id --> pre_y_id
        pr_y_id = y_id >> MuY
        # Precision reduction for x_id --> pre_x_id
        pr_x_id = x_id >> MuX
        # Precision reduction for reg_id --> pre_reg_id
        pre_reg_id = pr_y_id * pre_num_reg_x + pr_x_id
        # Update pr_dic
#        pr_dic[reg_id] = pre_reg_id
        pr_dic[reg_id+1] = pre_reg_id+1
        
    # Make a mapping from pre_reg_id to reg_id --> pre_reg2reg
    pre_reg2reg = {}
    for reg_id, pre_reg_id in pr_dic.items():
        if pre_reg_id not in pre_reg2reg:
            pre_reg2reg[pre_reg_id] = str(reg_id)
#            pre_reg2reg[pre_reg_id] = [reg_id]
        else:
            pre_reg2reg[pre_reg_id] = pre_reg2reg[pre_reg_id]+" "+str(reg_id)
#            pre_reg2reg[pre_reg_id].append(reg_id)

    # Make a generalization dictionary --> gen_dic
    for reg_id in range(NumRegX * NumRegY):
        # Precision-reduced ID --> pre_reg_id
#        pre_reg_id = pr_dic[reg_id]
        pre_reg_id = pr_dic[reg_id+1]
        # Update gen_dic
#        gen_dic[reg_id] = pre_reg2reg[pre_reg_id]
        gen_dic[reg_id+1] = pre_reg2reg[pre_reg_id]
        
    return gen_dic

#################################### Main #####################################
# Fix a seed
np.random.seed(1)

# Make a generalization dictionary --> gen_dic
gen_dic = MakeGenDic()

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
    reg_id = int(lst[2])
    # Anonymized region ID --> ano_reg_id
    rand = np.random.rand()
    # Hide a region
    if rand < Lambda:
        ano_reg_id = "*"
    # Generalize a region
    else:
        ano_reg_id = gen_dic[reg_id]
#    out_lst = [user_id, time_id, ano_reg_id]
    out_lst = [ano_reg_id]
    writer.writerow(out_lst)
f.close()
g.close()
