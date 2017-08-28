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
    - mode (str): how to run the script (local or batch);
    - evts (int): the number of events to run over (if not provided, run over all events);
    - mask (int): status of the masking channel procedure, 0 for off and 1 for off (if not provided, do not mask anything).
    
How to run it:
    First of all, type
    
    SetupProject LHCb
    
    to set the environment.
    Then, type

    python -u RunAnalysis.py | tee LogRunAnalysis.dat
    
    to loop over all the data of the test beam.
    For example:

    python -u RunAnalysis.py --board M1 --PA FanIn --DUTRun 7 --mode local(batch) | tee LogRunAnalysis.dat
    python -u RunAnalysis.py --board M1 --PA FanIn --DUTRun 7 --mode local(batch) --evts 1000 | tee LogRunAnalysis.dat
    python -u RunAnalysis.py --board M1 --PA FanIn --DUTRun 7 --mode local(batch) --mask 1 | tee LogRunAnalysis.dat
    
    to analyse one physics run, or

    python -u RunAnalysis.py --board M1 --PA FanIn --mode local(batch) | tee LogRunAnalysis.dat
    python -u RunAnalysis.py --board M1 --PA FanIn --mode local(batch) --evts 1000 | tee LogRunAnalysis.dat
    python -u RunAnalysis.py --board M1 --PA FanIn --mode local(batch) --mask 1 | tee LogRunAnalysis.dat
    
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



def RunAnalysis(board,PA,DUTRun,mode,evts,mask,onlyPlots) :
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
    if (testbeam=='October2016' or testbeam=='June2017' or testbeam=='August2017'):
	pathToInput = MAMBA+board+'/'
    else:
	pathToInput = MAMBA+board+'/'+PA+'/'
    print 'Path to input: ', pathToInput

    # CSV file to be used as input.
    if (testbeam=='October2016' or testbeam=='June2017' or testbeam=='August2017'):
	if kazu==1:
    		logbook = 'Logbook/RunLog'+testbeam+'Board'+board+'KAZU.csv'
	else:
		logbook = 'Logbook/RunLog'+testbeam+'Board'+board+'.csv'
    else:
	logbook = 'Logbook/RunLog'+testbeam+'Board'+board+PA+'.csv'
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
        # Run the analysis for this run only.
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
        sector = int(row['Sector'])
        rotation = int(row['Rotation (deg)'])
        bias = int(row['Bias voltage (V)'])

        # print DUTRun

        print 'Running analysis for', DUTRun, 'run.'
        rowPed, rowPed_i = AssociatePed(logbook_df_san,DUTRun)
        # print rowPed, rowPed_i
        ped = int(rowPed.get_value(rowPed_i[0],'DUT run'))
        # print ped
           
        # Assign filenames for physics and pedestal runs.
        for filename in os.listdir(pathToInput) :
	  if (testbeam=='October2016' or testbeam=='June2017' or testbeam=='August2017'):
		if (fnmatch.fnmatch(filename,'*-'+PA+'-'+board+'-'+str(DUTRun)+'-*.dat')) :
        	        print 'Filename for physics run:', filename
                	filenameNoPathPhys = filename
          	elif (fnmatch.fnmatch(filename,'*-'+PA+'-'+board+'-'+str(ped)+'.dat')) :
               		print 'Filename for pedestal run:', filename
                	filenameNoPathPed = filename
	  else:
            if (fnmatch.fnmatch(filename,'*-'+board+'-'+PA+'-'+str(DUTRun)+'-*.dat')) :
                print 'Filename for physics run:', filename
                filenameNoPathPhys = filename
            elif (fnmatch.fnmatch(filename,'*-'+board+'-'+PA+'-'+str(ped)+'.dat')) :
                print 'Filename for pedestal run:', filename
                filenameNoPathPed = filename
        
        if (mode == 'batch') :
            # Use qsub
            #command = "qsub -l cput=" + cput + " -v board="+board+",PA="+PA+",DUTRun="+str(DUTRun)+",ped="+str(ped)+",filenameNoPathPhys="+filenameNoPathPhys+    ",filenameNoPathPed="+filenameNoPathPed+" SubmitAnalysis.pbs" # No spaces after ','.
	    if (testbeam=='October2016' or testbeam=='June2017' or testbeam=='August2017'):
            	if onlyPlots:
			line_run = "python "+kepler+"/../Analysis_onlyPlots.py -b "+board+" -t "+typeDict[board]+" -e "+str(evts)+" -m "+str(mask)+" -s "+filenameNoPathPhys+" -p "+filenameNoPathPed + " -l "+str(sector) + " -y "+str(rotation) + " -v "+str(bias)
	    	else:
			line_run = "python "+kepler+"/../Analysis.py -b "+board+" -t "+typeDict[board]+" -e "+str(evts)+" -m "+str(mask)+" -s "+filenameNoPathPhys+" -p "+filenameNoPathPed  + " -l "+str(sector) + " -y "+str(rotation) + " -v "+str(bias)
	    else:
           	 if onlyPlots:
               		line_run = "python "+kepler+"/../Analysis_onlyPlots.py -b "+board+" -r "+PA+" -t "+typeDict[board]+" -e "+str(evts)+" -m "+str(mask)+" -s "+filenameNoPathPhys+" -p "+filenameNoPathPed + " -l "+str(sector) + " -y "+str(rotation) + " -v "+str(bias)
            	 else:
                	line_run = "python "+kepler+"/../Analysis.py -b "+board+" -r "+PA+" -t "+typeDict[board]+" -e "+str(evts)+" -m "+str(mask)+" -s "+filenameNoPathPhys+" -p "+filenameNoPathPed + " -l "+str(sector) + " -y "+str(rotation) + " -v "+str(bias)        

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
            
            command = "bsub -q 1nd clusterRun_"+filenameNoPathPhys.split('-')[3]+".sh"
            print command
            subprocess.call(command,shell=True)
            
        elif (mode == 'local') :
	 if (testbeam=='October2016' or testbeam=='June2017' or testbeam=='August2017'):	  
            # Use python directly 
	    if onlyPlots:            
		command = "python Analysis_onlyPlots.py -b "+board+" -t "+typeDict[board]+" -e "+str(evts)+" -m "+str(mask)+" -s "+filenameNoPathPhys+" -p "+filenameNoPathPed + " -l "+str(sector) + " -y "+str(rotation) + " -v "+str(bias)
	    else:
		command = "python Analysis.py -b "+board+" -t "+typeDict[board]+" -e "+str(evts)+" -m "+str(mask)+" -s "+filenameNoPathPhys+" -p "+filenameNoPathPed + " -l "+str(sector) + " -y "+str(rotation) + " -v "+str(bias)
	    print command
            subprocess.call(command,shell=True)
	 else:
            # Use python directly 
            if onlyPlots:
                command = "python Analysis_onlyPlots.py -b "+board+" -r "+PA+" -t "+typeDict[board]+" -e "+str(evts)+" -m "+str(mask)+" -s "+filenameNoPathPhys+" -p "+filenameNoPathPed + " -l "+str(sector) + " -y "+str(rotation) + " -v "+str(bias)
            else:
                command = "python Analysis.py -b "+board+" -r "+PA+" -t "+typeDict[board]+" -e "+str(evts)+" -m "+str(mask)+" -s "+filenameNoPathPhys+" -p "+filenameNoPathPed + " -l "+str(sector) + " -y "+str(rotation) + " -v "+str(bias)
            print command
            subprocess.call(command,shell=True)
  

    return



###############
# 
# Main function
#

if __name__ == "__main__" :

    parser = argparse.ArgumentParser(description='Run the analysis of the May 2016 or late May 2016 test beam data.')

    parser.add_argument('--board',required=True,choices=boardList,help='board')
    parser.add_argument('--PA',required=True,choices=PAList,help='PA or Hybrid name')
    parser.add_argument('--DUTRun',type=int,required=False,help='DUT run (for debugging, to process one DUT run only)')
    parser.add_argument('--mode',required=True,choices=modeList,help='mode')
    parser.add_argument('--evts',required=False,type=int,help='evts')
    parser.add_argument('--mask',required=False,type=int,choices=[0,1],help='mask')
    parser.add_argument('--onlyPlots',required=False,type=int,choices=[0,1],help='onlyPlots')
    parser.add_argument('--KAZU',required=False,type=int,choices=[0,1],help='KAZU')
    
    args = parser.parse_args()

    # Parameters and configuration.
    board = args.board
    PA = args.PA
    DUTRun = args.DUTRun
    mode = args.mode
    kazu = args.KAZU
    if args.evts is None :
        evts = -1
    else :
        evts = args.evts
    if args.mask is None :
        mask = 0
    else :
        mask = args.mask
    if args.onlyPlots is None :
	onlyPlots = 0
    else:
	onlyPlots = 1

    RunAnalysis(board,PA,DUTRun,mode,evts,mask,onlyPlots)
