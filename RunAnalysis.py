#!/usr/bin/env python

"""
Author: Federica Lionetto
Date: May 18th, 2016

Description:
    This script allows to get the information of the test beam data from the logbook and to loop over all physics run.
    It sanitise the logbook and then associate to each physics run (run with beam) the corresponding or the most appropriate pedetal run (in general, run with beam too).
    After that, it calls the script that takes care of the analysis itself.
    The following arguments can/have to be provided:
    - board (str): the board one wants to analyse (M1, M3, or M4);
    - PA (str): the pitch adapter region one wants to analyse (FanIn or FanUp);
    - DUTRun (str): optional, the physics run one wants to process (mostly for debugging);
    - mode (str): how to run the script (local or batch).

How to run it:
    First of all, type
    
    SetupProject LHCb
    
    to set the environment.
    Then, type

    python -u RunAnalysis.py | tee LogRunAnalysis.dat
    
    to loop over all the data of the test beam.
    For example:

    python -u RunAnalysis.py --board M1 --PA FanIn --DUTRun 7 --mode local(batch) | tee LogRunAnalysis.dat
    
    to analyse one physics run, or

    python -u RunAnalysis.py --board M1 --PA FanIn --mode local(batch) | tee LogRunAnalysis.dat
    
    to analyse all of them.
"""

import argparse
import subprocess
import sys
import os
import fnmatch

import numpy as np
import pandas as pd

sys.path.insert(0,'./Tools')
from DefineGlobalVariables import *
from ToolsForPython import *



# cput = '23:59:59'
# cput = '1439:59:59'
# cput = '143:59:59'

    

def RunAnalysis(board,PA,DUTRun,mode) :
    # Check that the specified PA exists for the specified board (it can be that M1 has FanIn only, and so on).
    # print PADict[board]
    if PA not in PADict[board] :
        print 'ERROR! The specified PA does not exist for the specified board.'
        exit()

    print '===================='
    print 'Running analysis for'
    print 'Board:', board
    print 'PA:', PA
    print 'DUTRun:', DUTRun
    print 'Mode:', mode
    print '===================='
    
    # Path to input data.
    pathToInput = MAMBA+board+'/'+PA+'/'
    print 'Path to input: ', pathToInput

    # CSV file to be used as input.
    logbook = 'Logbook/RunLogMay2016Board'+board+PA+'.csv'
    print 'Logbook: ', logbook

    logbook_df_san = GetInfoFromLogbook(logbook)

    # Environment variables.
    path = os.environ['PATH']
    ld_library_path = os.environ['LD_LIBRARY_PATH']
    kepler = os.environ['KEPLERROOT']
    # print path
    # print ld_library_path
    # print kepler
    line_empty = '\n'
    line_export_path = 'export PATH='+path+':$PATH\n'
    line_export_ld_library_path = 'export LD_LIBRARY_PATH='+ld_library_path+':$LD_LIBRARY_PATH\n'
    
    if DUTRun is not None :
        # !!! Run the analysis for this run only.
        # Check this is not a pedestal or calibration run.
        rowDUTRun, rowDUTRun_i = GetDUTRun(logbook_df_san,DUTRun)
        if rowDUTRun.get_value(rowDUTRun_i,'Purpose') == 'Pedestal' or rowDUTRun.get_value(rowDUTRun_i,'Purpose') == 'Calibration' :
            print 'ERROR! This is a pedestal or calibration run.'
            exit()
        logbook_df_subset = rowDUTRun.copy(deep=True)

    else :
        # Select runs for the loop.
        print 'Running the analysis for all runs.'
        logbook_df_subset = logbook_df_san.loc[(logbook_df_san['Purpose'] == 'Bias scan') | (logbook_df_san['Purpose'] == 'Angle scan') | (logbook_df_san['Purpose'] == 'Eff/Res')].copy(deep=True)
    
    print logbook_df_subset.head()
    print logbook_df_subset.shape

    # Loop over the selected runs.
    print '==========================='
    print 'Loop over the selected runs'
    for index,row in logbook_df_subset.iterrows() :
        # print index
        # print row

        DUTRun = int(row['DUT run'])
        # print DUTRun

        print 'Running analysis for', DUTRun, 'run.'
        rowPed, rowPed_i = AssociatePed(logbook_df_san,DUTRun)
        # print rowPed, rowPed_i
        ped = int(rowPed.get_value(rowPed_i[0],'DUT run'))
        # print ped
           
        # Assign filenames for physics and pedestal runs.
        for filename in os.listdir(pathToInput) :
            if (fnmatch.fnmatch(filename,'*-'+board+'-'+PA+'-'+str(DUTRun)+'-*.dat')) :
                print 'Filename for physics run:', filename
                filenameNoPathPhys = filename
            elif (fnmatch.fnmatch(filename,'*-'+board+'-'+PA+'-'+str(ped)+'.dat')) :
                print 'Filename for pedestal run:', filename
                filenameNoPathPed = filename

        if (mode == 'batch') :
            # Use qsub
            #command = "qsub -l cput=" + cput + " -v board="+board+",PA="+PA+",DUTRun="+str(DUTRun)+",ped="+str(ped)+",filenameNoPathPhys="+filenameNoPathPhys+    ",filenameNoPathPed="+filenameNoPathPed+" SubmitAnalysis.pbs" # No spaces after ','.
            line_run = "python "+kepler+"/../Analysis.py -b "+board+" -r "+PA+" -s "+filenameNoPathPhys+" -p "+filenameNoPathPed
        
            with open('clusterRun_'+filenameNoPathPhys.split('-')[3]+'.sh','w') as text_file :
                text_file.write(line_export_path)
                text_file.write(line_empty)
                text_file.write(line_export_ld_library_path)
                text_file.write(line_empty)
                text_file.write(line_run)
                text_file.closed
            
            command = 'chmod +x clusterRun_'+filenameNoPathPhys.split('-')[3]+'.sh'
            print '>', command
            subprocess.call(command,shell=True,cwd='.')
            
            command = "bsub -q 8nh clusterRun_"+filenameNoPathPhys.split('-')[3]+".sh"
            print command
            subprocess.call(command,shell=True)
            
        elif (mode == 'local') :
            # Use python directly 
            command = "python Analysis.py -b "+board+" -r "+PA+" -s "+filenameNoPathPhys+" -p "+filenameNoPathPed
            print command
            subprocess.call(command,shell=True)

    return



###############
# 
# Main function
#

if __name__ == "__main__" :

    parser = argparse.ArgumentParser(description='Run the analysis of the May 2016 test beam data.')

    parser.add_argument('--board',required=True,choices=boardList,help='board')
    parser.add_argument('--PA',required=True,choices=PAList,help='PA')
    parser.add_argument('--DUTRun',type=int,required=False,help='DUT run (for debugging, to process one DUT run only)')
    parser.add_argument('--mode',required=True,choices=modeList,help='mode')

    args = parser.parse_args()

    # Parameters and configuration.
    board = args.board
    PA = args.PA
    DUTRun = args.DUTRun
    mode = args.mode

    RunAnalysis(board,PA,DUTRun,mode)
