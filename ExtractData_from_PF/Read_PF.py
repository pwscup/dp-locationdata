#!/usr/bin/env python3
"""
Created by Takao Murakami Jun 12, 2019.

Description: 
    Read the People flow dataset (SNS-based People Flow Data) within the area 
    of interest.

Usage:
    Read_PF.py
"""
from datetime import datetime
import csv
import numpy as np

################################# Parameters ##################################
# People flow dir (input)
PFDir = "../../20140808_snsbasedPeopleFlowData_nightley/20140808_snsbasedPeopleFlowData_nightley/"
# People flow files (input)
PFFiles = ["2013-07-01.csv", "2013-07-07.csv", "2013-10-07.csv", "2013-10-13.csv", "2013-12-16.csv", "2013-12-22.csv"]
# Region file (output)
RegFile = "../Data/regions_TK.csv"
# Trace file (output)
TraceFile = "../Data/traces_TK.csv"
# Minimum of y (latitude)
MIN_Y = 35.65
# Maximum of y (latitude)
MAX_Y = 35.75
# Minimum of x (longitude)
MIN_X = 139.68
# Maximum of x (longitude)
MAX_X = 139.8
# Number of regions in the x-term
NumRegX = 32
# Number of regions in the y-term
NumRegY = 32

########################### Read People flow files ############################
# [output1]: checkin_list ([user_id, unixtime, year, month, day, hour, min, sec, y, x, y_id, x_id, reg_id])
def ReadPF():
    # Initialization
    checkin_list = []

    # Calculate the boundaries of the regions (NumRegX x NumRegY) --> xb, yb
    xb = np.zeros(NumRegX)
    yb = np.zeros(NumRegY)
    for i in range(NumRegX):
        xb[i] = MIN_X + (MAX_X - MIN_X) * i / NumRegX
    for i in range(NumRegY):
        yb[i] = MIN_Y + (MAX_Y - MIN_Y) * i / NumRegY

    # Read a checkin file --> checkin_list
    for file in PFFiles:
        pffile = PFDir + file
        f = open(pffile, "r")
        reader = csv.reader(f)
        next(reader)
        for lst in reader:
            user_id = int(lst[0])
            y = float(lst[3])
            x = float(lst[4])
            
            if MIN_Y <= y <= MAX_Y and MIN_X <= x <= MAX_X:
                # datetime --> dt
                daytim = lst[2]
                daytim_list = daytim.split(" ")
                day_list = daytim_list[0].split("-")
                tim_list = daytim_list[1].split(":")
                # year --> ye
                ye = int(day_list[0])
                # month --> mo
                mo = int(day_list[1])
                # day --> da
                da = int(day_list[2])
                # hour --> ho
                ho = int(tim_list[0])
                # min --> mi
                mi = int(tim_list[1])
                # sec --> se
                se = int(tim_list[2])
                # datetime --> dt
                dt = datetime(ye, mo, da, ho, mi, se)
                # unixtime --> ut
                ut = dt.timestamp()

                # Calculate x_id
                x_id = NumRegX-1
                for i in range(NumRegX-1):
                    if xb[i] <= x < xb[i+1]:
                        x_id = i
                        break
                # Calculate y_id
                y_id = NumRegY-1
                for i in range(NumRegY-1):
                    if yb[i] <= y < yb[i+1]:
                        y_id = i
                        break
                # Calculate reg_id
                reg_id = y_id * NumRegX + x_id

                # Update checkin_list
#                checkin_list.append([user_id, ut, ye, mo, da, ho, mi, se, y, x, y_id, x_id, reg_id])
                checkin_list.append([user_id+1, ut, ye, mo, da, ho, mi, se, y, x, y_id+1, x_id+1, reg_id+1])
        f.close()

    print("#Checkins within the area of interest =", len(checkin_list))

    return checkin_list

#################################### Main #####################################
# Read People flow files
checkin_list = ReadPF()

# Output region information
f = open(RegFile, "w")
print("reg_id,y_id,x_id,y(center),x(center)", file=f)
writer = csv.writer(f, lineterminator="\n")

# Calculate the center of each region (NumRegX x NumRegY) --> xc, yc
xc = np.zeros(NumRegX)
yc = np.zeros(NumRegY)
x_width = (MAX_X - MIN_X) / NumRegX
y_width = (MAX_Y - MIN_Y) / NumRegY

for i in range(NumRegX):
    xc[i] = MIN_X + x_width * i + x_width / 2
for i in range(NumRegY):
    yc[i] = MIN_Y + y_width * i + y_width / 2
for y_id in range(NumRegY):
    for x_id in range(NumRegX):
        reg_id = y_id * NumRegX + x_id
#        lst = [reg_id, y_id, x_id, yc[y_id], xc[x_id]]
        lst = [reg_id+1, y_id+1, x_id+1, yc[y_id], xc[x_id]]
        writer.writerow(lst)
f.close()

# Sort checkin_list in ascending order of (user_id, unixtime)
checkin_list.sort(key=lambda tup: (tup[0], tup[1]), reverse=False)

# Output checkin_list
f = open(TraceFile, "w")
print("user_id,unixtime,year,month,day,hour,min,sec,y,x,y_id,x_id,reg_id", file=f)
writer = csv.writer(f, lineterminator="\n")
for lst in checkin_list:
    writer.writerow(lst)
f.close()
