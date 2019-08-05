#!/usr/bin/env python3
"""
Created by Takao Murakami Jun 17, 2019 (last updated: Aug 5, 2019).

Description: 
    PL(l, r) (Planar Laplace mechanism) [Andres+, CCS13]. 
    It perturbs (adds noise to) a region according to the planar Laplacian with 
    l-privacy within r km assigned for each region. It provides epsilon-Geo-IND 
    (epsilon = l/r) for each region.

Reference:
    M.E.Andres et al., Geo-Indistinguishability: Differential Privacy for Location-Based Systems, CCS, 2013.

Usage:
    A4-PL.py [Original Trace (in)] [Anonymized Trace (out)] ([l (default:0.1)] [r (default:1)])
"""
import numpy as np
import scipy.special as spys
import math
import csv
import sys

################################# Parameters ##################################
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

#sys.argv = ["A4-PL.py", "../Data/PWSCup2019_Osaka/orgtraces_team001_data01_IDP.csv", "../Data_Anonymize/anotraces_team001_data01_IDP_A4.csv", 4, 1]
if len(sys.argv) < 3:
    print("Usage:",sys.argv[0],"[Original Trace (in)] [Anonymized Trace (out)] ([l (default:0.1)] [r (default:1)])" )
    sys.exit(0)

# Original trace file (input)
OrgTraceFile = sys.argv[1]
# Anonymized trace file (output)
AnoTraceFile = sys.argv[2]

# Parameter l
L = 0.1
if len(sys.argv) >= 4:
    L = float(sys.argv[3])

# Parameter r
R = 1
if len(sys.argv) >= 5:
    R = float(sys.argv[4])

#################################### Main #####################################
# Fix a seed
np.random.seed(1)

# privacy budget --> epsilon
epsilon = L/R

# Calculate the center of each region (NumRegX x NumRegY) --> xc, yc
xc = np.zeros(NumRegX)
yc = np.zeros(NumRegY)
x_width = (MAX_X - MIN_X) / NumRegX
y_width = (MAX_Y - MIN_Y) / NumRegY

for i in range(NumRegX):
    xc[i] = MIN_X + x_width * i + x_width / 2
for i in range(NumRegY):
    yc[i] = MIN_Y + y_width * i + y_width / 2

# Read the original trace file and output anonymized traces
f = open(OrgTraceFile, "r")
g = open(AnoTraceFile, "w")
reader = csv.reader(f)
next(reader)
print("user_id,time_id,reg_id", file=g)
writer = csv.writer(g, lineterminator="\n")
home_reg_id = -1
for lst in reader:
    user_id = int(lst[0])
    time_id = int(lst[1])
#    reg_id = int(lst[2])
    reg_id = int(lst[2])-1

    # y_id & x_id (start with 0) --> y_id, x_id
    y_id = int(reg_id / NumRegX)
    x_id = reg_id % NumRegX

    # Draw angle --> theta
    theta = np.random.rand() * 2 * math.pi
    # Draw radius --> r
    p = np.random.rand()
    w_minus_one = spys.lambertw((p-1)/math.e, -1).real
    r = -1 / epsilon * (w_minus_one + 1)
    # y-coordinate of the noise (km) --> ns_y
    ns_y_km = r * math.sin(theta)
    # x-coordinate of the noise (km) --> ns_x
    ns_x_km = r * math.cos(theta)

    # y-coordinate & x-coordinate after anonymization --> ano_y, ano_x
    # 1 degree of latitude (resp. longitude in TK) = 111 km (resp. 91 km)
    ano_y = yc[y_id] + ns_y_km / 111
    ano_x = xc[x_id] + ns_x_km / 91
    
    # y_id (start with 0) after anonymization --> ano_y_id
    ano_y_id = int((ano_y - MIN_Y) / y_width)
    if ano_y_id < 0:
        ano_y_id = 0
    elif ano_y_id >= NumRegY:
        ano_y_id = NumRegY - 1
        
    # x_id (start with 0) after anonymization --> ano_x_id
    ano_x_id = int((ano_x - MIN_X) / x_width)
    if ano_x_id < 0:
        ano_x_id = 0
    elif ano_x_id >= NumRegX:
        ano_x_id = NumRegX - 1

    # reg_id (start with 0) after anonymization --> ano_reg_id
    ano_reg_id = ano_y_id * NumRegX + ano_x_id
    ano_reg_id += 1

    out_lst = [user_id, time_id, ano_reg_id]
    writer.writerow(out_lst)
f.close()
g.close()
