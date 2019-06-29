#!/usr/bin/env python3
"""
Created by Takao Murakami Jun 18, 2019.

Description: 
    Run all anonymization & shuffle algorithms, re-identification algorithms, 
    tracking programs, and then evaluate utility & security scores.

Usage:
    EvalAll.py
"""
import subprocess
import csv

################################# Parameters ##################################
# Python algorithm
PyAlg = "python"
#PyAlg = "python3"

# Anonymization algorithm directory
AnoAlgDir = "SmplProg_Anonymize"
# Anonymization algorithm file
AnoAlgFile = ["A1-none.py", "A2-MRLH.py", "A3-kRR.py", "A4-PL.py", "A5-YA.py"]
# Parameters of the anonymization algorithms
AnoAlgParam = [0] * len(AnoAlgFile)
AnoAlgParam[1] = ["0-0-0.5","0-0-0.8","0-0-0.95","1-1-0","1-1-0.5","1-1-0.8","2-2-0","2-2-0.5","2-2-0.8",]
AnoAlgParam[2] = ["0.01","0.1","1","2","3","4","5","6","6.93"]
AnoAlgParam[3] = ["0.01-1","0.1-1","1-1","2-1","3-1","4-1","5-1","6-1","6.93-1"]

# Re-identification algorithm directory
ReidAlgDir = "SmplProg_Reidentify"
# Re-identification algorithm file
ReidAlgFile = ["R1-rand.py", "R2-VisitProb.py"]

# Tracking algorithm directory
TraAlgDir = "SmplProg_Track"
# Tracking algorithm file
TraAlgFile = ["T1-rand.py", "T2-VisitProb.py"]

# Shuffle algorithm file
ShuAlgFile = "ShuffleIDs.py"
# Utility evaluation file
EvalUtilFile = "EvalUtil.py"
# Security evaluation (re-identification) file
EvalSecRFile = "EvalSecR.py"
# Security evaluation (tracking) file
EvalSecTFile = "EvalSecT.py"

# Training trace file
TrainTraceFile = "Data/traintraces_TK.csv"
#TrainTraceFile = "Data/testtraces_TK.csv"
# Testing trace file
TestTraceFile = "Data/testtraces_TK.csv"

# Anonymized trace directory
AnoTraceDir = "Data_Anonymized"
# Anonymized & Shuffled trace directory
AnoShuTraceDir = "Data_Anonymized_Shuffled"
# Re-identified trace directory
ReidTraceDir = "Data_Reidentified"
# Tracking trace directory
TraTraceDir = "Data_Tracked"

# Result file (output)
ResFile = "results.csv"

#################################### Main #####################################
# Initialization
anony_lst = []

############# Anonymization & Shuffle ##############
# For each anonymiation algorithm
for i in range(len(AnoAlgFile)):
    if AnoAlgParam[i] == 0:
        # Anonymized trace file --> ano_trace_file
        ano_trace_file = AnoTraceDir + "/testtraces_TK_" + AnoAlgFile[i][0:2] + ".csv"
        # Run the anonymiation algorithm
        cmd = PyAlg + " " + AnoAlgDir + "/" + AnoAlgFile[i] + " " + TestTraceFile + " " + ano_trace_file
        print(cmd)
        subprocess.check_output(cmd.split())
        # Evaluate the utility
        cmd = PyAlg + " " + EvalUtilFile + " " + TestTraceFile + " " + ano_trace_file
        print(cmd)
        runcmd = subprocess.check_output(cmd.split())
        anony_lst.append([AnoAlgFile[i][0:2], float(runcmd.decode())])
    else:
        # For each parameter
        for j in range(len(AnoAlgParam[i])):
            param = AnoAlgParam[i][j].replace("-", " ")
            # Anonymized trace file --> ano_trace_file
            ano_trace_file = AnoTraceDir + "/testtraces_TK_" + AnoAlgFile[i][0:2] + "-" + AnoAlgParam[i][j] + ".csv"
            # Run the anonymiation algorithm with the parameter
            cmd = PyAlg + " " + AnoAlgDir + "/" + AnoAlgFile[i] + " " + TestTraceFile + " " + ano_trace_file + " " + param
            print(cmd)
            subprocess.check_output(cmd.split())
            # Evaluate the anonymized file
            cmd = PyAlg + " " + EvalUtilFile + " " + TestTraceFile + " " + ano_trace_file
            print(cmd)
            runcmd = subprocess.check_output(cmd.split())
            anony_lst.append([AnoAlgFile[i][0:2] + "-" + AnoAlgParam[i][j], float(runcmd.decode())])

# Run a shuffle algorithm
cmd = PyAlg + " " + ShuAlgFile + " " + AnoTraceDir + " " + AnoShuTraceDir
print(cmd)
subprocess.check_output(cmd.split())

########### Re-identification & Tracking ###########
# For each anonymiation algorithm
x = 0
for i in range(len(AnoAlgFile)):
    if AnoAlgParam[i] == 0:
        # Anonymized & shuffled trace file --> ano_trace_file
        ano_shu_trace_file = AnoShuTraceDir + "/testtraces_TK_" + AnoAlgFile[i][0:2] + ".csv"
        # For each re-identification algorithm
        for k in range(len(ReidAlgFile)):
            # Estimated table file --> est_table_file
            est_table_file = ReidTraceDir + "/etable_TK_" + AnoAlgFile[i][0:2] + "-" + ReidAlgFile[k][0:2] + ".csv"
            # Run the re-identification algorithm
            cmd = PyAlg + " " + ReidAlgDir + "/" + ReidAlgFile[k] + " " + TrainTraceFile + " " + ano_shu_trace_file + " " + est_table_file
            print(cmd)
            subprocess.check_output(cmd.split())
            # Evaluate the security (re-identification)
            ptable_file = AnoShuTraceDir + "/ptable_TK_" + AnoAlgFile[i][0:2] + ".csv" 
            cmd = PyAlg + " " + EvalSecRFile + " " + ptable_file + " " + est_table_file
            print(cmd)
            runcmd = subprocess.check_output(cmd.split())
            anony_lst[x].append(float(runcmd.decode()))
        # For each tracking algorithm
        for k in range(len(TraAlgFile)):
            # Estimated trace file --> est_trace_file
            est_trace_file = TraTraceDir + "/etraces_TK_" + AnoAlgFile[i][0:2] + "-" + TraAlgFile[k][0:2] + ".csv"
            # Run the tracking algorithm
            cmd = PyAlg + " " + TraAlgDir + "/" + TraAlgFile[k] + " " + TrainTraceFile + " " + ano_shu_trace_file + " " + est_trace_file
            print(cmd)
            subprocess.check_output(cmd.split())
            # Evaluate the security (tracking)
            cmd = PyAlg + " " + EvalSecTFile + " " + TestTraceFile + " " + est_trace_file
            print(cmd)
            runcmd = subprocess.check_output(cmd.split())
            anony_lst[x].append(float(runcmd.decode()))
        x += 1
    else:
        # For each parameter
        for j in range(len(AnoAlgParam[i])):
            param = AnoAlgParam[i][j].replace("-", " ")
            # Anonymized & shuffled trace file --> ano_trace_file
            ano_shu_trace_file = AnoShuTraceDir + "/testtraces_TK_" + AnoAlgFile[i][0:2] + "-" + AnoAlgParam[i][j] + ".csv"
            # Run each re-identification algorithm
            for k in range(len(ReidAlgFile)):
                # Estimated table file --> est_table_file
                est_table_file = ReidTraceDir + "/etable_TK_" + AnoAlgFile[i][0:2] + "-" + AnoAlgParam[i][j] + "-" + ReidAlgFile[k][0:2] + ".csv"
                cmd = PyAlg + " " + ReidAlgDir + "/" + ReidAlgFile[k] + " " + TrainTraceFile + " " + ano_shu_trace_file + " " + est_table_file
                print(cmd)
                subprocess.check_output(cmd.split())
                # Evaluate the security (re-identification)
                ptable_file = AnoShuTraceDir + "/ptable_TK_" + AnoAlgFile[i][0:2] + "-" + AnoAlgParam[i][j] + ".csv" 
                cmd = PyAlg + " " + EvalSecRFile + " " + ptable_file + " " + est_table_file
                print(cmd)
                runcmd = subprocess.check_output(cmd.split())
                anony_lst[x].append(float(runcmd.decode()))
            # For each tracking algorithm
            for k in range(len(TraAlgFile)):
                # Estimated trace file --> est_trace_file
                est_trace_file = TraTraceDir + "/etraces_TK_" + AnoAlgFile[i][0:2] + "-" + AnoAlgParam[i][j] + "-" + TraAlgFile[k][0:2] + ".csv"
                # Run the tracking algorithm
                cmd = PyAlg + " " + TraAlgDir + "/" + TraAlgFile[k] + " " + TrainTraceFile + " " + ano_shu_trace_file + " " + est_trace_file
                print(cmd)
                subprocess.check_output(cmd.split())
                # Evaluate the security (tracking)
                cmd = PyAlg + " " + EvalSecTFile + " " + TestTraceFile + " " + est_trace_file
                print(cmd)
                runcmd = subprocess.check_output(cmd.split())
                anony_lst[x].append(float(runcmd.decode()))
            x += 1

################ Output the Results ################
f = open(ResFile, "w")
writer = csv.writer(f, lineterminator="\n")
# header
header_lst = ["Ano", "Util"]
for k in range(len(ReidAlgFile)):
    header_lst.append(ReidAlgFile[k][0:2])
for k in range(len(TraAlgFile)):
    header_lst.append(TraAlgFile[k][0:2])
writer.writerow(header_lst)
# body
for i in range(len(anony_lst)):
    writer.writerow(anony_lst[i])
f.close()
