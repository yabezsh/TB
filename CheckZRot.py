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
    
    python -u CheckZRot.py --board M3 --PA FanUp | tee LogCheckZRot-M3-FanUp.dat
"""

import argparse
import subprocess
import sys

import ROOT

sys.path.insert(0,'./Tools')
from DefineGlobalVariables import *
from ToolsForPython import *
from Style import *

def CheckZRot(board,PA) :
    # Check that the specified PA exists for the specified board (it can be that M1 has FanIn only, and so on).
    # print PADict[board]
    if PA not in PADict[board] :
        print 'ERROR! The specified PA does not exist for the specified board.'
        exit()
    
    print '==============================================='
    print 'Studying the rotation around z for'
    print 'Board:', board
    print 'PA:', PA
    print '===================='
    
    funName = 'CheckZRot'

    # Mount EOS
    command = '/afs/cern.ch/project/eos/installation/0.3.15/bin/eos.select -b fuse mount ~/eos'
    print '>', command
    subprocess.call(command,shell=True)
    
    # Open the logbook.
    # CSV file to be used as input.
    logbook = 'Logbook/RunLog'+testbeam+'Board'+board+PA+'.csv'
    print 'Logbook: ', logbook

    logbook_df_san = GetInfoFromLogbook(logbook)
   
    # Ignore custom, calibration, and pedestal runs.
    logbook_df_subset = logbook_df_san.loc[(logbook_df_san['Purpose'] == 'Angle scan') | (logbook_df_san['Purpose'] == 'Bias scan') | (logbook_df_san['Purpose'] == 'Eff/Res')].copy(deep=True)
    if logbook_df_subset.empty :
        print 'ERROR! No logbook subset found.'

    print '=============='
    print 'Logbook subset'
    print '=============='
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
    # - get the TProfile from the proper ROOT file;
    # - fit it with a straight line y = a0+a1*x;
    # - save the fit results and plot their distribution.
    la0 = []
    la0_u = []
    la1 = []
    la1_u = []

    # Create a histogram with the distribution of a0 and a1.
    outFileROOT = ROOT.TFile(pathToOutput+funName+'_'+board+'_'+PA+'.root','RECREATE')
    # outFileROOT.cd()
    
    ca0 = ROOT.TCanvas('ca0'+'_'+board+'_'+PA,'ca0'+'_'+board+'_'+PA,800,600)
    ca1 = ROOT.TCanvas('ca1'+'_'+board+'_'+PA,'ca1'+'_'+board+'_'+PA,800,600)

    InitCanvas(ca0)
    InitCanvas(ca1)

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

        print 'Running analysis for', DUTRun, 'run.'
        filename = pathToInput+'output_'+str(DUTRun)+'/Plots/AnalysisOutput_'+board+'_'+PA+'_'+str(DUTRun)+'_'+str(telescopeRun)+'.root'
        if os.path.exists(filename) : 
            inFileROOT = ROOT.TFile(filename,'READ')
            if inFileROOT.GetListOfKeys().Contains('h9') :
                h9 = inFileROOT.Get('h9') 
                entries = h9.GetEntries()
                print 'Entries:', entries
                if entries == 0 :
                    print 'ERROR! Found histogram with zero entries.'
                else : 
                    f = ROOT.TF1('f','pol1')
                    # f.SetParameter(0,0.)
                    # f.SetParLimits(0,0.,50.)
                    # f.SetParameter(1,0.)
                    # f.SetParLimits(1,0.,50.)
                    h9.Fit(f)
                    a0 = f.GetParameter(0)
                    a0_u = f.GetParError(0)
                    a1 = f.GetParameter(1)
                    a1_u = f.GetParError(1)

                    print 'a0:', a0, '+/-', a0_u
                    print 'a1:', a1, '+/-', a1_u
   
                    # If the fit results are not compatible with a horizontal straight line (possible rotation around z), print a warning.
                    if (a1/a1_u > 3.) :
                        print 'WARNING! Possible rotation around z.'

                    la0.append(a0)
                    la0_u.append(a0_u)
                    la1.append(a1)
                    la1_u.append(a1_u)
            
            inFileROOT.Close()

    outFileROOT.cd()

    print 'List of a0:', la0
    print 'List of a0 uncertainty:', la0_u
    print 'List of a1:', la1
    print 'List of a1 uncertainty:', la1_u

    # Fit.
    mina0 = min(la0)
    maxa0 = max(la0)
    mina1 = min(la1)
    maxa1 = max(la1)

    # print mina0
    # print maxa0
    # print mina1
    # print maxa1

    # ha0 = ROOT.TH1F('ha0','ha0',100,mina0,maxa0)
    # ha1 = ROOT.TH1F('ha1','ha1',100,mina1,maxa1)
    ha0 = ROOT.TH1F('ha0','ha0',30,-0.01,0.01)
    ha1 = ROOT.TH1F('ha1','ha1',30,-0.001,0.001)

    InitHist(ha0,'a_{0}','a_{0}','')
    InitHist(ha1,'a_{1}','a_{1}','')

    SetStyleObj(obj=ha0,lineColor=ROOT.kRed)
    SetStyleObj(obj=ha1,lineColor=ROOT.kRed)

    for a0 in la0 : 
        ha0.Fill(a0)
    for a1 in la1 :
        ha1.Fill(a1)

    print 'Length of la0:', len(la0)
    print 'Length of la1:', len(la1)
    print 'Entries in ha0:', ha0.GetEntries()
    print 'Entries in ha1:', ha1.GetEntries()

    DrawObj(ca0,ha0,None,'E',pathToFigures)
    DrawObj(ca1,ha1,None,'E',pathToFigures)
    
    outFileROOT.Close()

    print 'Done.'

    return

###############
# 
# Main function
#

if __name__ == "__main__" :

    parser = argparse.ArgumentParser(description='Study the rotation around z for the May 2016 or late May 2016 test beam data.')

    parser.add_argument('--board',required=True,choices=boardList,help='board')
    parser.add_argument('--PA',required=True,choices=PAList,help='PA')

    args = parser.parse_args()

    # Parameters and configuration.
    board = args.board
    PA = args.PA

    CheckZRot(board,PA)
