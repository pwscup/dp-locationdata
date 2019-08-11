#!/usr/bin/env python3
"""
Created by Takao Murakami Jun 12, 2019 (last updated: Aug 11, 2019).

Description: 
    Shuffle user IDs in all anonymized trace files.

Usage:
    ShuffleIDs.py [Anonymized Trace Directory] [Anonymized & Shuffled Trace Directory]
"""
import numpy as np
import csv
import sys
import glob
import os

################################# Parameters ##################################
# Number of users
UserNum = 2000
# length of each trace
T = 40

#sys.argv = ["ShuffleIDs.py", "../Data_Anonymize", "../Data_Anonymize_Shuffle"]
if len(sys.argv) < 3:
    print("Usage:",sys.argv[0],"[Anonymized Trace Directory] [Anonymized & Shuffled Trace Directory]" )
    sys.exit(0)

# Anonymized trace directory (input)
AnoTraceDir = sys.argv[1]
# Anonymized & shuffled trace directory (output)
AnoShuTraceDir = sys.argv[2]

#################################### Main #####################################
# Fix a seed
#np.random.seed(1)

# Anonymized trace file list --> ano_trace_file_lst
ano_trace_dir_ast = AnoTraceDir + "/*"
ano_trace_file_lst = glob.glob(ano_trace_dir_ast)

# For each anonymized trace file
for ano_trace_file in ano_trace_file_lst:
    # Randomly shuffled user ID --> rand_id 
    rand_id = np.arange(UserNum)
    np.random.shuffle(rand_id)
    
    rand_id_inv = np.argsort(rand_id)

    # Aonnymized & shuffled trace file --> ano_shu_trace_file
    basename = os.path.basename(ano_trace_file)
    ano_shu_trace_file = AnoShuTraceDir + "/" + basename.replace("anotraces", "pubtraces")

    # Pseudo-ID table file --> pse_id_table_file
    basename_split = basename.split("_", 1)
    pse_id_table_file = AnoShuTraceDir + "/ptable_" + basename_split[1]

    # Make anonymized & shuffled traces --> ano_shu_trace
    ano_shu_trace = []
    f = open(ano_trace_file, "r")
    reader = csv.reader(f)
    next(reader)
    user_id = 0
    tim = T+1
    for lst in reader:
#        user_id = int(lst[0])
#        user_id = int(lst[0])-1
#        tim = lst[1]
#        reg_id = lst[2]
        reg_id = lst[0]
#        ano_shu_trace.append([rand_id[user_id], tim, reg_id])
#        ano_shu_trace.append([rand_id[user_id]+1, tim, reg_id])
        ano_shu_trace.append([rand_id[user_id]+UserNum+1, tim, reg_id])
        tim += 1
        if tim > 2*T:
            user_id += 1
            tim = T+1
    f.close()

    # Sort ano_shu_trace in ascending order of user_id
    ano_shu_trace.sort(key=lambda tup: tup[0], reverse=False)

    # Output the anonymized & shuffled traces
    g = open(ano_shu_trace_file, "w")
    print("pse_id,time_id,reg_id", file=g)
    writer = csv.writer(g, lineterminator="\n")
    for lst in ano_shu_trace:
        writer.writerow(lst)
    g.close()

    # Output the pseudo-ID table
    g = open(pse_id_table_file, "w")
#    print("user_id,pse_id", file=g)
    print("pse_id,user_id", file=g)
    writer = csv.writer(g, lineterminator="\n")
    for i in range(UserNum):
#        lst = [i, rand_id[i]]
#        lst = [i+1, rand_id[i]+1]
#        lst = [i+1, rand_id_inv[i]+1]
        lst = [UserNum+i+1, rand_id_inv[i]+1]
        writer.writerow(lst)
    g.close()
