#!/usr/bin/env python

"""
Author: Federica Lionetto
Date: May 26th, 2016

Description:

How to run it:
    First of all, type
    
    SetupProject LHCb
    
    to set the environment.
    Then, type

    python -u RunCheckZRot.py | tee LogRunCheckZRot.dat
    
    to loop over all the data of the test beam.
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
            command = 'python -u CheckZRot.py --board '+board+' --PA '+PA+' | tee LogCheckZRot-'+board+'-'+PA+'.dat'
            print command
            # subprocess.call(command,shell=True)
