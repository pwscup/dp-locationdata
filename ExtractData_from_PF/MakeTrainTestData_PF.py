#!/usr/bin/env python3
"""
Created by Takao Murakami Jun 12, 2019 (last updated: Jun 17, 2019).

Description: 
    Make training traces and testing traces (People flow).

Usage:
    MakeTrainTestData_PF.py
"""
import numpy as np
import csv
import random

################################# Parameters ##################################
# Trace file (input)
TraceFile = "../Data/traces_TK.csv"
# Training trace file (output)
TrainTraceFile = "../Data/traintraces_TK.csv"
# Testing trace file (output)
TestTraceFile = "../Data/testtraces_TK.csv"

# Ratio of training locations over all locations
TrainRatio = 0.5
# How to divide the trace (0: former part & latter part, 1: random)
#HowToDiv = 0
HowToDiv = 1
# Minimum time interval (sec)
MinTimInt = 1800
# Number of users
UserNum = 1000
# Number of locations per user
LocNum = 70

############################## Read a trace file ##############################
# [output1]: user_dic ({user_id: user_index})
# [output2]: ucount_dic ({user_id: counts})
# [output3]: trace_list ([user_id, unixtime, year, month, day, hour, min, sec, reg_id])
def ReadTrace():
    # Initialization
    ucount_dic= {}
    trace_list = []

    # Read a trace file --> ucount_dic, trace_list
    f = open(TraceFile, "r")
    reader = csv.reader(f)
    next(reader)
    user_id_pre = -1
    ut_pre = -1
    for i, lst in enumerate(reader):
        if i % 100000 == 0:
            print(i)
#        user_id = int(lst[0])
        user_id = int(lst[0]) - 1
        ut = float(lst[1])
        ye = lst[2].zfill(4)
        mo = lst[3].zfill(2)
        da = lst[4].zfill(2)
        ho = lst[5].zfill(2)
        mi = lst[6].zfill(2)
        se = lst[7].zfill(2)
#        reg_id = int(lst[12])
        reg_id = int(lst[12]) - 1

        # Continue if the time interval is less than MinTimInt
        if user_id == user_id_pre and ut - ut_pre < MinTimInt:
            continue
        # Update ucount_dic & trace_list until the number of locations reaches Locnum
        if ucount_dic.get(user_id, 0) < LocNum:
            ucount_dic[user_id] = ucount_dic.get(user_id, 0) + 1
            trace_list.append([user_id, ut, ye, mo, da, ho, mi, se, reg_id])
        # Save the previous user_id & unixtime --> user_id_pre, ut_pre
        user_id_pre = user_id
        ut_pre = ut
    f.close()

    # Sort trace_list in ascending order of (user_id, unixtime)
    trace_list.sort(key=lambda tup: (tup[0], tup[1]), reverse=False)

    # A dictionary of users --> user_dic ({user_id: user_index})
    user_dic = {}
    for user_id, counts in sorted(ucount_dic.items()):
        # Continue if the number of locations for the user is below LocNum
        if counts < LocNum:
            continue
        # User index --> user_dic[user_id]
        if len(user_dic) < UserNum:
            user_dic[user_id] = len(user_dic)

    print("#Users =", len(user_dic))

    return user_dic, ucount_dic, trace_list

############# Split traces into training traces & testing traces ##############
# [input1]: ucount_dic ({user_id: counts})
# [input2]: trace_list ([user_id, unixtime, year, month, day, hour, min, sec, y_id, x_id, reg_id])
# [output1]: train_trace_list ([user_id, unixtime, year, month, day, hour, min, sec, y_id, x_id, reg_id])
# [output2]: test_trace_list ([user_id, unixtime, year, month, day, hour, min, sec, y_id, x_id, reg_id])
def SplitTraces(ucount_dic, trace_list):
    # Initialization
    ucnt_dic = {}
    train_trace_list = []
    test_trace_list = []
    
    # Shuffle trace_list (if the trace is randomly divided)
    if HowToDiv == 1:
        random.seed(1)
        random.shuffle(trace_list)

    # Split trace_list into train_trace_list and test_trace_list
    for event in trace_list:
        if ucnt_dic.get(event[0], 0) < ucount_dic[event[0]] * TrainRatio:
            train_trace_list.append(event)
        else:
            test_trace_list.append(event)   
        ucnt_dic[event[0]] = ucnt_dic.get(event[0], 0) + 1
        
    # Sort train_trace_list & test_trace_list in ascending order of (user_id, unixtime)
    train_trace_list.sort(key=lambda tup: (tup[0], tup[1]), reverse=False)
    test_trace_list.sort(key=lambda tup: (tup[0], tup[1]), reverse=False)

    return train_trace_list, test_trace_list

#################################### Main #####################################
# Fix a seed
np.random.seed(1)

# Read a trace file
user_dic, ucount_dic, trace_list = ReadTrace()

# Split traces into training traces & testing traces
train_trace_list, test_trace_list = SplitTraces(ucount_dic, trace_list)

# Output training traces
f = open(TrainTraceFile, "w")
#print("user_id,time,reg_id", file=f)
print("user_id,time_id,reg_id", file=f)
writer = csv.writer(f, lineterminator="\n")
user_id_pre = -1
time_id = 1
for event in train_trace_list:
    if event[0] in user_dic:
#        user_id = user_dic[event[0]]
        user_id = user_dic[event[0]]+1
#        reg_id = event[8]
        reg_id = event[8]+1

        # For a new user
        if user_id != user_id_pre:
            # Initialization
            time_id = 1

#        lst = [user_id,event[2]+"/"+event[3]+"/"+event[4]+" "+event[5]+":"+event[6]+":"+event[7],reg_id]
        lst = [user_id,time_id,reg_id]
        writer.writerow(lst)

        # Save user_id  --> user_id_pre
        user_id_pre = user_id
        # Increase time_id --> time_id
        time_id += 1
f.close()

# Output testing traces
f = open(TestTraceFile, "w")
#print("user_id,time,reg_id", file=f)
print("user_id,time_id,reg_id", file=f)
writer = csv.writer(f, lineterminator="\n")
user_id_pre = -1
time_id = 1
for event in test_trace_list:
    if event[0] in user_dic:
#        user_id = user_dic[event[0]]
        user_id = user_dic[event[0]]+1
#        reg_id = event[8]
        reg_id = event[8]+1

        # For a new user
        if user_id != user_id_pre:
            # Initialization
            time_id = 1
        
#        lst = [user_id,event[2]+"/"+event[3]+"/"+event[4]+" "+event[5]+":"+event[6]+":"+event[7],reg_id]
        lst = [user_id,time_id,reg_id]
        writer.writerow(lst)

        # Save user_id  --> user_id_pre
        user_id_pre = user_id
        # Increase time_id --> time_id
        time_id += 1
f.close()
