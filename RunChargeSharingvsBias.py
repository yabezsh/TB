#!/usr/bin/env python

"""
Author: Federica Lionetto
Date: June 28th, 2016

Description:
    This script allows to run the ChargeSharingvsBias.py script for all the boards, pitch adapter regions, and biasing schemes.

How to run it:
    First of all, type

    SetupProject LHCb
    
    to set the environment.
    Then, type
    
    python -u RunChargeSharingvsBias.py | tee LogRunChargeSharingvsBias.dat
"""

import sys
import subprocess

sys.path.insert(0,'./Tools')
from DefineGlobalVariables import *

###############
# 
# Main function
#

if __name__ == "__main__" :

    for board in boardList :
        for PA in PADict[board] :
            for BS in BSList :
                command = 'python -u ChargeSharingvsBias.py --board '+board+' --PA '+PA+' --BS '+BS+' | tee LogChargeSharingvsBias-'+board+'-'+PA+'-'+BS+'.dat'
                print command
                subprocess.call(command,shell=True)
