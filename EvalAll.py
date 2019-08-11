#!/usr/bin/env python3
"""
Created by Takao Murakami Jun 18, 2019 (last updated: Aug 5, 2019).

Description: 
    Run all anonymization & shuffle algorithms, all ID disclosure algorithms, 
    and all trace inference algorithms, and then evaluate utility & security.

Usage:
    EvalAll.py
"""
import subprocess
import csv
import sys

################################# Parameters ##################################
sys.argv = ["EvalAll.py", "001", "01"]
if len(sys.argv) < 3:
    print("Usage:",sys.argv[0],"[Team No (001-002)] [Dataset No (01-02)]" )
    sys.exit(0)

# Python algorithm
PyAlg = "python"
#PyAlg = "python3"

# Anonymization algorithm directory
AnoAlgDir = "SmplProg_Anonymize"
# Anonymization algorithm file
AnoAlgFile = ["A1-none.py", "A2-MRLH.py", "A3-kRR.py", "A4-PL.py", "A5-YA.py"]
# Parameters of the anonymization algorithms
AnoAlgParam = [0] * len(AnoAlgFile)
AnoAlgParam[1] = ["0-0-0.1","0-0-0.2","0-0-0.5","0-0-0.8","1-1-0","1-1-0.1","1-1-0.2","1-1-0.5","1-1-0.8"]
AnoAlgParam[2] = ["0.1","1","2","4","6","8","10","12","14"]
AnoAlgParam[3] = ["0.1-1","1-1","2-1","3-1","4-1","5-1","6-1","7-1"]
AnoAlgParam[4] = ["0.1","0.2","0.3","0.4","0.5","0.6","0.7","0.8","0.9","1"]

# ID-disclosure (re-identification) algorithm directory
ReidAlgDir = "SmplProg_IDDisclose"
# ID-disclosure (re-identification) algorithm file
ReidAlgFile = ["I1-rand.py", "I2-VisitProb.py", "I3-HomeProb.py"]

# Trace inference (tracking) algorithm directory
TraAlgDir = "SmplProg_TraceInfer"
# Trace inference (tracking) algorithm file
TraAlgFile = ["T1-rand.py", "T2-VisitProb.py", "T3-HomeProb.py"]

# Shuffle algorithm file
ShuAlgFile = "Prog_Shuffle/ShuffleIDs.py"
# Utility evaluation file
EvalUtilFile = "Prog_Eval/EvalUtil.py"
# Security evaluation (ID-disclosure) file
EvalSecIFile = "Prog_Eval/EvalSecI.py"
# Security evaluation (trace inference) file
EvalSecTFile = "Prog_Eval/EvalSecT.py"

# Team No
TeamNo = sys.argv[1]
# Dataset No
DataSetNo = sys.argv[2]

# Reference trace file
RefTraceFile = "Data/PWSCup2019_Osaka/reftraces_team" + TeamNo + "_data" + DataSetNo + "_IDP.csv"
# Original trace file
OrgTraceFile = "Data/PWSCup2019_Osaka/orgtraces_team" + TeamNo + "_data" + DataSetNo + "_IDP.csv"

# Anonymized trace directory
AnoTraceDir = "Data_Anonymize"
# Anonymized & Shuffled trace directory
AnoShuTraceDir = "Data_Anonymize_Shuffle"
# ID-disclosured (re-identified) trace directory
ReidTraceDir = "Data_IDDisclose"
# Trace infered (tracked) trace directory
TraTraceDir = "Data_TraceInfer"

# Anonymized trace name
AnoTraceName = "anotraces_team" + TeamNo + "_data" + DataSetNo + "_IDP"
# Anonymized & shuffled trace name
AnoShuTraceName = "pubtraces_team" + TeamNo + "_data" + DataSetNo + "_IDP"
# Pseudo-ID table name
PseTableName = "ptable_team" + TeamNo + "_data" + DataSetNo + "_IDP"
# Estimated table name
EstTableName = "etable_team020-" + TeamNo + "_data" + DataSetNo + "_IDP"
# Estimated trace name
EstTraceName = "etraces_team020-" + TeamNo + "_data" + DataSetNo + "_IDP"

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
        ano_trace_file = AnoTraceDir + "/" + AnoTraceName + "_" + AnoAlgFile[i][0:2] + ".csv"
        # Run the anonymiation algorithm
        cmd = PyAlg + " " + AnoAlgDir + "/" + AnoAlgFile[i] + " " + OrgTraceFile + " " + ano_trace_file
        print(cmd)
        subprocess.check_output(cmd.split())
        # Evaluate the utility
        cmd = PyAlg + " " + EvalUtilFile + " " + OrgTraceFile + " " + ano_trace_file
        print(cmd)
        runcmd = subprocess.check_output(cmd.split())
        anony_lst.append([AnoAlgFile[i][0:2], float(runcmd.decode())])
    else:
        # For each parameter
        for j in range(len(AnoAlgParam[i])):
            param = AnoAlgParam[i][j].replace("-", " ")
            # Anonymized trace file --> ano_trace_file
            ano_trace_file = AnoTraceDir + "/" + AnoTraceName + "_" + AnoAlgFile[i][0:2] + "-" + AnoAlgParam[i][j] + ".csv"
            # Run the anonymiation algorithm with the parameter
            cmd = PyAlg + " " + AnoAlgDir + "/" + AnoAlgFile[i] + " " + OrgTraceFile + " " + ano_trace_file + " " + param
            print(cmd)
            subprocess.check_output(cmd.split())
            # Evaluate the anonymized file
            cmd = PyAlg + " " + EvalUtilFile + " " + OrgTraceFile + " " + ano_trace_file
            print(cmd)
            runcmd = subprocess.check_output(cmd.split())
            anony_lst.append([AnoAlgFile[i][0:2] + "-" + AnoAlgParam[i][j], float(runcmd.decode())])

# Run a shuffle algorithm
cmd = PyAlg + " " + ShuAlgFile + " " + AnoTraceDir + " " + AnoShuTraceDir
print(cmd)
subprocess.check_output(cmd.split())

########### ID-disclosure & Trace inference ###########
# For each anonymiation algorithm
x = 0
for i in range(len(AnoAlgFile)):
    if AnoAlgParam[i] == 0:
        # Anonymized & shuffled trace file --> ano_shu_trace_file
        ano_shu_trace_file = AnoShuTraceDir + "/" + AnoShuTraceName + "_" + AnoAlgFile[i][0:2] + ".csv"
        # For each ID-disclosure (re-identification) algorithm
        for k in range(len(ReidAlgFile)):
            # Estimated table file --> est_table_file
            est_table_file = ReidTraceDir + "/" + EstTableName + "_" + AnoAlgFile[i][0:2] + "-" + ReidAlgFile[k][0:2] + ".csv"
            # Run the ID-disclosure (re-identification) algorithm
            cmd = PyAlg + " " + ReidAlgDir + "/" + ReidAlgFile[k] + " " + RefTraceFile + " " + ano_shu_trace_file + " " + est_table_file
            print(cmd)
            subprocess.check_output(cmd.split())
            # Evaluate the security (ID-disclosure)
            ptable_file = AnoShuTraceDir + "/" + PseTableName + "_" + AnoAlgFile[i][0:2] + ".csv" 
            cmd = PyAlg + " " + EvalSecIFile + " " + ptable_file + " " + est_table_file
            print(cmd)
            runcmd = subprocess.check_output(cmd.split())
            anony_lst[x].append(float(runcmd.decode()))
        # For each trace inference (tracking) algorithm
        for k in range(len(TraAlgFile)):
            # Estimated trace file --> est_trace_file
            est_trace_file = TraTraceDir + "/" + EstTraceName + "_" + AnoAlgFile[i][0:2] + "-" + TraAlgFile[k][0:2] + ".csv"
            # Run the trace inference (tracking) algorithm
            cmd = PyAlg + " " + TraAlgDir + "/" + TraAlgFile[k] + " " + RefTraceFile + " " + ano_shu_trace_file + " " + est_trace_file
            print(cmd)
            subprocess.check_output(cmd.split())
            # Evaluate the security (trace inference)
            cmd = PyAlg + " " + EvalSecTFile + " " + OrgTraceFile + " " + est_trace_file
            print(cmd)
            runcmd = subprocess.check_output(cmd.split())
            anony_lst[x].append(float(runcmd.decode()))
        x += 1
    else:
        # For each parameter
        for j in range(len(AnoAlgParam[i])):
            param = AnoAlgParam[i][j].replace("-", " ")
            # Anonymized & shuffled trace file --> ano_shu_trace_file
            ano_shu_trace_file = AnoShuTraceDir + "/" + AnoShuTraceName + "_" + AnoAlgFile[i][0:2] + "-" + AnoAlgParam[i][j] + ".csv"
            # Run each ID-disclosure (re-identification) algorithm
            for k in range(len(ReidAlgFile)):
                # Estimated table file --> est_table_file
                est_table_file = ReidTraceDir + "/" + EstTableName + "_" + AnoAlgFile[i][0:2] + "-" + AnoAlgParam[i][j] + "-" + ReidAlgFile[k][0:2] + ".csv"
                cmd = PyAlg + " " + ReidAlgDir + "/" + ReidAlgFile[k] + " " + RefTraceFile + " " + ano_shu_trace_file + " " + est_table_file
                print(cmd)
                subprocess.check_output(cmd.split())
                # Evaluate the security (ID-disclosure)
                ptable_file = AnoShuTraceDir + "/" + PseTableName + "_" + AnoAlgFile[i][0:2] + "-" + AnoAlgParam[i][j] + ".csv" 
                cmd = PyAlg + " " + EvalSecIFile + " " + ptable_file + " " + est_table_file
                print(cmd)
                runcmd = subprocess.check_output(cmd.split())
                anony_lst[x].append(float(runcmd.decode()))
            # For each trace inference (tracking) algorithm
            for k in range(len(TraAlgFile)):
                # Estimated trace file --> est_trace_file
                est_trace_file = TraTraceDir + "/" + EstTraceName + "_" + AnoAlgFile[i][0:2] + "-" + AnoAlgParam[i][j] + "-" + TraAlgFile[k][0:2] + ".csv"
                # Run the trace inference (tracking) algorithm
                cmd = PyAlg + " " + TraAlgDir + "/" + TraAlgFile[k] + " " + RefTraceFile + " " + ano_shu_trace_file + " " + est_trace_file
                print(cmd)
                subprocess.check_output(cmd.split())
                # Evaluate the security (trace inference)
                cmd = PyAlg + " " + EvalSecTFile + " " + OrgTraceFile + " " + est_trace_file
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
