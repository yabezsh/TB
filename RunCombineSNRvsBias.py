#!/usr/bin/env python

"""
Author: Federica Lionetto
Date: June 15th, 2016

Description:
    This script allows to run the CombineSNRvsBias.py script for all the pitch adapter regions and biasing schemes.

How to run it:
    First of all, type

    SetupProject LHCb
    
    to set the environment.
    Then, type
    
    python -u RunCombineSNRvsBias.py | tee LogRunCombineSNRvsBias.dat
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

    for PA in ['FanIn','FanUp'] :
        for BS in ['Top','Back'] :
            command = 'python -u CombineSNRvsBias.py --PA '+PA+' --BS '+BS+' | tee LogCombineSNRvsBias-'+PA+'-'+BS+'.dat'
            print command
            subprocess.call(command,shell=True)
