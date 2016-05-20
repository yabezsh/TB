#!/usr/bin/env python

"""
Author: Federica Lionetto
Date: May 20th, 2016

Description:
    This script allows to study the SNR as a function of the angle for a given board, a given pitch adapter region, and a given biasing scheme.
    It opens the logbook and gets the subset corresponding to the desired angle scan. After that, for each physics run, it reads the text file with SNR and corresponding uncertainty. Then, it creates a TGraph with the SNR as a function of the angle.
    The following arguments can/have to be provided:
    - board (str): the board one wants to analyse (M1, M3, or M4);
    - PA (str): the pitch adapter region one wants to analyse (FanIn or FanUp);
    - BS (str): the biasing scheme (Top or Back).
    
How to run it:
    python -u SNRvsAngle.py --board M3 --PA FanUp --BS Back | tee LogSNRvsAngle.dat
"""

import argparse
import sys

import numpy as np

import ROOT

sys.path.insert(0,'./Tools')
from DefineGlobalVariables import *
from ToolsForPython import *
from Style import *

def SNRvsAngle(board,PA,BS) :
    # Check that the specified PA exists for the specified board (it can be that M1 has FanIn only, and so on).
    # print PADict[board]
    if PA not in PADict[board] :
        print 'ERROR! The specified PA does not exist for the specified board.'
        exit()
    
    print '==============================================='
    print 'Studying the SNR as a function of the angle for'
    print 'Board:', board
    print 'PA:', PA
    print 'BS:', BS
    print '===================='
    
    funName = 'SNRvsAngle'

    # Open the logbook and get the subset corresponding to the desired angle scan.
    # CSV file to be used as input.
    logbook = 'Logbook/RunLogMay2016Board'+board+PA+'.csv'
    print 'Logbook: ', logbook

    logbook_df_san = GetInfoFromLogbook(logbook)
    
    logbook_df_subset = logbook_df_san.loc[(logbook_df_san['Purpose'] == 'Angle scan') & (logbook_df_san['Biasing scheme'] == BS)].copy(deep=True)
    
    print logbook_df_subset.head()
    print logbook_df_subset.shape
    
    # Path to input data.
    pathToInput = DQM+board+'/'+PA+'/'
    print 'Path to input: ', pathToInput
    pathToOutput = DQM+board+'/'+PA+'/'+funName+'/'
    print 'Path to output: ', pathToOutput
    pathToFigures = pathToOutput+'Figures/'
    print 'Path to figures: ', pathToFigures

    if not os.path.exists(pathToOutput) :
        os.makedirs(pathToOutput)
    if not os.path.exists(pathToFigures) :
        os.makedirs(pathToFigures)

    # For each physics run:
    # - read the text file with SNR and corresponding uncertainty.
    lSNR = []
    lSNRU = []
    langle = []
    # Loop over the selected runs.
    print '==========================='
    print 'Loop over the selected runs'
    for index,row in logbook_df_subset.iterrows() :
        # print index
        # print row
        
        DUTRun = int(row['DUT run'])
        print DUTRun

        telescopeRun = int(row['Telescope run'])
        print telescopeRun

        angle = int(row['Rotation (deg)'])
        print angle
        langle.append(angle)

        filename = pathToInput+'output_'+str(DUTRun)+'/MPV_'+board+'_'+PA+'_'+str(DUTRun)+'_'+str(telescopeRun)+'.txt'
        with open(filename,'r') as text_file :
            text_file.readline()
            values = text_file.readline().replace('\n','')
            values_list = values.split(',')
            SNR = values_list[0]
            SNRU = values_list[1]
            # print values
            # print values_list
            print 'SNR:', SNR
            print 'SNR uncertainty:', SNRU
            lSNR.append(SNR)
            lSNRU.append(SNRU)
            text_file.closed

    print lSNR
    print lSNRU
    print langle
    
    # Create a TGraph with the SNR as a function of the angle.
    outFileROOT = ROOT.TFile(pathToOutput+funName+'_'+board+'_'+PA+'_'+BS+'.root','RECREATE')
    aSNR = np.asarray(lSNR,dtype=float) 
    aSNRU = np.asarray(lSNRU,dtype=float)
    aangle = np.asarray(langle,dtype=float)
    aangleU = np.zeros(len(aSNR),dtype=float)

    cSNRvsAngle = ROOT.TCanvas('cSNRvsAngle'+'_'+board+'_'+PA+'_'+BS,'cSNRvsAngle'+'_'+board+'_'+PA+'_'+BS,800,600)
    gSNRvsAngle = ROOT.TGraphErrors(len(aSNR),aangle,aSNR,aangleU,aSNRU)
    gSNRvsAngle.SetName("SNR vs angle")
    InitGraph(gSNRvsAngle,'SNR vs angle','Angle','SNR')
    SetStyleObj(obj=gSNRvsAngle,lineColor=ROOT.kRed)
    # gSNRvsAngle.SetMinimum(0.)
    # gSNRvsAngle.SetMaximum(10.)
    # gSNRvsAngle.GetXaxis().SetLimits(-0.05,1.05)

    # Fit.
    minFit = min(langle);
    maxFit = max(langle);
    fpol2 = ROOT.TF1('fpol2','pol2',minFit,maxFit)
    gSNRvsAngle.Fit('fpol2','R')
    anglePeak = -1*(fpol2.GetParameter(1))/(2*fpol2.GetParameter(2));
    SNRPeak = fpol2.Eval(anglePeak);
    print 'Angle at the peak:', anglePeak
    print 'Signal at the peak:', SNRPeak

    DrawObj(cSNRvsAngle,gSNRvsAngle,None,'AP',pathToFigures)
    
    outFileROOT.cd()
    outFileROOT.Close()

    return

###############
# 
# Main function
#

if __name__ == "__main__" :

    parser = argparse.ArgumentParser(description='Study the SNR as a function of the angle for the May 2016 test beam data.')

    parser.add_argument('--board',required=True,choices=boardList,help='board')
    parser.add_argument('--PA',required=True,choices=PAList,help='PA')
    parser.add_argument('--BS',required=True,choices=BSList,help='BS')

    args = parser.parse_args()

    # Parameters and configuration.
    board = args.board
    PA = args.PA
    BS = args.BS

    SNRvsAngle(board,PA,BS)
