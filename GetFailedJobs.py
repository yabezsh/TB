#!/usr/bin/env python

"""
Author: Federica Lionetto
Date: May 21st, 2016

Description:
   This script allows to get all the jobs that failed when execuing the RunAnalysis.py script.
   The list of the failed jobs is saved in a text file, where each line contains:
   - the error
   - the board
   - the pitch adapter region
   - the physics run
   This allows to have a closer look to problematic jobs and fix their issues.

How to run it:
    First of all, type
    
    SetupProject LHCb
    
    to set the environment.
    Then, type
    
    python -u GetFailedJobs.py | tee LogGetFailedJobs.dat
"""

import fnmatch
import os
import subprocess
import sys

sys.path.insert(0,'./Tools')
from DefineGlobalVariables import *

def GetFailedJobs() :
    print '==================='
    print 'Getting failed jobs'
    print '==================='
    
    # Mount EOS
    command = '/afs/cern.ch/project/eos/installation/0.3.15/bin/eos.select -b fuse mount ~/eos'
    print '>', command
    subprocess.call(command,shell=True)
    
    # Even if the log files contain "Job finished", it does not mean that the job did not crash.
    # This is the list of the issues that are searched in the log file.
    # 'mkdir: cannot create directory'
    # 'segmentation violation'
    # This is the list of the issues that should not be a problem.
    # 'TbPixelSvc          ERROR Device W0002_I03 is not in the alignment file'
    issueList = []
    issueList.append('mkdir: cannot create directory')
    issueList.append('segmentation violation')
    # issueList.append('TbPixelSvc          ERROR Device W0002_I03 is not in the alignment file')
    print 'Issue list:', issueList

    # !!! To be changed after we have the final version of the analysis.
    # inPath = DQM+'Logs/'
    inPath = '/afs/cern.ch/work/i/ibezshyi/public/TESTBEAM/ChrisSoft/KeplerDev_v3r0/Tb/'
    outPath = DQM+'Logs/'

    print 'Input folder:', inPath
    print 'Output folder:', outPath

    # If the output folder does not exist, create it.
    if not os.path.exists(outPath) :
        # command = 'eos mkdir '+outPath
        # print command
        # subprocess.call(command,shell=True)
        os.makedirs(outPath)
    
    # If the output file already exists, delete it (since each line is appended to whatever is already there).
    if 'GetFailedJobs.dat' in os.listdir(outPath) :
        command = 'rm '+outPath+'GetFailedJobs.dat'
        print command
        subprocess.call(command,shell=True)

    for item in os.listdir(inPath) :
        if fnmatch.fnmatch(item,'LSFJOB_*') :
            # print item
            
            # Associate board and PA to the DUTRun.
            found = False
            with open(inPath+item+'/STDOUT','r') as inFileOut :

                for line in inFileOut :
                    # print line
                    if 'MAMBA' in line and '.dat' in line and 'Pedestal' not in line and not found :
                        # print line
                        found = True
                        if 'M1' in line :
                            board = 'M1'
                        elif 'M3' in line :
                            board = 'M3'
                        elif 'M4' in line :
                            board = 'M4'
                        else :
                            print 'ERROR! Board not found.'

                        if 'FanIn' in line :
                            PA = 'FanIn'
                        elif 'FanUp' in line :
                            PA = 'FanUp'
                        else :
                            print 'ERROR! PA not found.'

            # Get the DUTRun from the LSFJOB file.
            # Check if the STDOUT file contains the words 'Job finished', which means that the job finished without problems. If it is not the case, write the corresponding DUTRun number in a text file.
            for issue in issueList :
                with open(inPath+item+'/STDOUT','r') as inFileOut :
                    # print 'Looking for issue', issue
                    if issue in inFileOut.read() :
                        print '=================='
                        print 'Found failed job: ', inPath+item+'/STDOUT'
                        # The DUTRun can be found in the LSFJOB file.
                        with open(inPath+item+'/LSFJOB','r') as inFileErr :
                            # print inPath+item+'/LSFJOB'
                            linesErr = inFileErr.readlines() 
                            # print linesErr
                            info = linesErr[7].replace('\n','')
                            # print info
                            infoList = str.split(info,' ')
                            # print infoList[1]
                            temp = infoList[1].replace('clusterRun_','')
                            temp = temp.replace('\'','')
                            DUTRun = temp.replace('.sh','')
                            print 'DUTRun:', DUTRun
                            print 'Board:', board
                            print 'PA:', PA
                        with open(outPath+'GetFailedJobs.dat','a') as outFile :
                            outFile.write(issue+','+board+','+PA+','+DUTRun+'\n')

    return



###############
# 
# Main function
#

if __name__ == "__main__" :

    GetFailedJobs()
