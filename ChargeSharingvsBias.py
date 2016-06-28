#!/usr/bin/env python

"""
Author: Federica Lionetto
Date: June 28th, 2016

Description:
    This script allows to study
    - the charge sharing
    as a function of the bias voltage for a given board, a given pitch adapter region, and a given biasing scheme.
    It opens the logbook and gets the subset corresponding to the desired bias voltage scan. After that, for each physics run, it reads the ROOT file with charge sharing as a function of the interstrip position and fits it with an error function. Then, it creates a TGraph with the mu and sigma of the error function as a function of the bias voltage.
    The following arguments can/have to be provided:
    - board (str): the board one wants to analyse (M1, M3, or M4);
    - PA (str): the pitch adapter region one wants to analyse (FanIn or FanUp);
    - BS (str): the biasing scheme (Top, Back, or Both). The 'Both' biasing scheme refers to the situation in which the sensor should have been biased from the back, but the jumpers were not set properly, so it has been actually biased both from the top and from the back. This should be treated as a 'Back' biasing scheme. 
    
How to run it:
    First of all, type

    SetupProject LHCb
    
    to set the environment.
    Then, type
    
    python -u ChargeSharingvsBias.py --board M3 --PA FanUp --BS Back | tee LogChargeSharingvsBias-M3-FanUp-Back.dat
"""

import argparse
import subprocess
import sys

import math

import numpy as np

import ROOT

sys.path.insert(0,'./Tools')
from DefineGlobalVariables import *
from ToolsForPython import *
from Style import *

def ChargeSharingvsBias(board,PA,BS) :
    # Check that the specified PA exists for the specified board (it can be that M1 has FanIn only, and so on).
    # print PADict[board]
    if PA not in PADict[board] :
        print 'ERROR! The specified PA does not exist for the specified board.'
        exit()
    
    print '================================================================='
    print 'Studying the charge sharing as a function of the bias voltage for'
    print 'Board:', board
    print 'PA:', PA
    print 'BS:', BS
    print '===================='
    
    funName = 'ChargeSharingvsBias'

    if BS == 'Both' :
        BSInLogbook = 'Back+Top'
    else :
        BSInLogbook = BS
    
    # Mount EOS
    command = '/afs/cern.ch/project/eos/installation/0.3.15/bin/eos.select -b fuse mount ~/eos'
    print '>', command
    subprocess.call(command,shell=True)
    
    # Open the logbook and get the subset corresponding to the desired bias voltage scan.
    # CSV file to be used as input.
    logbook = 'Logbook/RunLog'+testbeam+'Board'+board+PA+'.csv'
    print 'Logbook: ', logbook

    logbook_df_san = GetInfoFromLogbook(logbook)
    
    logbook_df_subset = logbook_df_san.loc[(logbook_df_san['Purpose'] == 'Bias scan') & (logbook_df_san['Biasing scheme'] == BSInLogbook)].copy(deep=True)
    if logbook_df_subset.empty :
        print 'ERROR! No logbook subset found.'
        return
    
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
    # - open the corresponding ROOT file and get the TProfile h17b
    # - fit the TProfile h17b with an error function
    # - save the mu and sigma of the error function
    lmu = []
    lmuU = []

    lsigma = []
    lsigmaU = []

    lbias = []
   
    outFileROOT = ROOT.TFile(pathToOutput+funName+'_'+board+'_'+PA+'_'+BS+'.root','RECREATE')
    outFileROOT.cd()
  
    ROOT.gStyle.SetOptFit(1)
    ROOT.gStyle.SetFitFormat('.3g')

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

        bias = abs(int(row['Bias voltage (V)']))
        print bias

        if bias not in lbias :
            print 'First run at this bias voltage.'
        
            filename = pathToInput+'output_'+str(DUTRun)+'/Plots/AnalysisOutput_'+board+'_'+PA+'_'+str(DUTRun)+'_'+str(telescopeRun)+'.root'
            print filename
        
            if os.path.exists(filename) :
                inFileROOT = ROOT.TFile(filename,'READ')
                hchargeSharing = inFileROOT.Get('h17b') 
                hchargeSharing.SetName('hchargeSharing'+'_'+board+'_'+PA+'_'+BS+'_'+str(bias))
                InitGraph(hchargeSharing,'charge sharing','interstrip position','Q_{R}/(Q_{L}+Q_{R})')
                SetStyleObj(obj=hchargeSharing,lineColor=ROOT.kRed)
                entries = hchargeSharing.GetEntries()
                print 'Entries:', entries
                if entries == 0 :
                    print 'ERROR! Found histogram with zero entries.'
                else :
                    print hchargeSharing

                    # Fit with an error function
                    minFit = -0.5
                    maxFit = 0.5
                    ferr = ROOT.TF1('ferr','[0]*(1.-erf((x-[1])/(sqrt(2.)*[2])))+[3]',minFit,maxFit)
                    ferr.SetParameter(0,0.4)
                    ferr.SetParLimits(0,0.2,0.6)
                    ferr.SetParameter(1,0.)
                    ferr.SetParLimits(1,-0.1,0.1)
                    ferr.SetParameter(2,0.1)
                    ferr.SetParLimits(2,0.,10.)
        
                    # Set parameter names.
                    ferr.SetParName(0,"a")
                    ferr.SetParName(1,"#mu")
                    ferr.SetParName(2,"#sigma")
                    ferr.SetParName(3,"b")

                    hchargeSharing.Fit('ferr','BR')
                    cchargeSharing = ROOT.TCanvas('cchargeSharing'+'_'+board+'_'+PA+'_'+BS+'_'+str(bias),'cchargeSharing'+'_'+board+'_'+PA+'_'+BS+'_'+str(bias),800,600)
                    InitCanvas(cchargeSharing)
                    outFileROOT.cd()
        
                    # Position of the fit results.
                    ROOT.gStyle.SetStatX(0.93)
                    ROOT.gStyle.SetStatY(0.82)
                    ROOT.gStyle.SetStatW(0.2)
                    ROOT.gStyle.SetStatH(0.2)

                    hchargeSharing.SetMinimum(0.)
                    hchargeSharing.SetMaximum(1.)

                    DrawObj(cchargeSharing,hchargeSharing,None,'',pathToFigures)
        
                    # Get parameters and parameter uncertainties.
                    a = ferr.GetParameter(0)
                    mu = ferr.GetParameter(1)
                    sigma = ferr.GetParameter(2)
                    b = ferr.GetParameter(3)
        
                    aU = ferr.GetParError(0)
                    muU = ferr.GetParError(1)
                    sigmaU = ferr.GetParError(2)
                    bU = ferr.GetParError(3)
            
                    print 'Mu: %.5f' % mu
                    print 'Mu uncertainty: %.5f' % muU
        
                    print 'Sigma: %.5f' % sigma
                    print 'Sigma uncertainty: %.5f' % sigmaU
        
                    lmu.append(mu)
                    lmuU.append(muU)

                    lsigma.append(sigma)
                    lsigmaU.append(sigmaU)
            
                    lbias.append(bias)

    print lmu
    print lmuU
    print lsigma
    print lsigmaU
    print lbias
    
    # Create a TGraph with the sigma as a function of the bias voltage.
    
    if len(lbias) > 0 :

        amu = np.asarray(lmu,dtype=float) 
        amuU = np.asarray(lmuU,dtype=float)
    
        asigma = np.asarray(lsigma,dtype=float) 
        asigmaU = np.asarray(lsigmaU,dtype=float)

        abias = np.asarray(lbias,dtype=float)
        abiasU = np.zeros(len(asigma),dtype=float)

        csigmavsBias = ROOT.TCanvas('csigmavsBias'+'_'+board+'_'+PA+'_'+BS,'csigmavsBias'+'_'+board+'_'+PA+'_'+BS,800,600)
        gsigmavsBias = ROOT.TGraphErrors(len(asigma),abias,asigma,abiasU,asigmaU)
        gsigmavsBias.SetName('#sigma vs bias voltage')
        InitGraph(gsigmavsBias,'#sigma vs bias voltage','bias voltage (V)','#sigma')
        SetStyleObj(obj=gsigmavsBias,lineColor=ROOT.kRed)
        gsigmavsBias.SetMinimum(0.)
        gsigmavsBias.SetMaximum(0.4)
        gsigmavsBias.GetXaxis().SetLimits(0.,500.)
        DrawObj(csigmavsBias,gsigmavsBias,None,'AP',pathToFigures)

        cmuvsBias = ROOT.TCanvas('cmuvsBias'+'_'+board+'_'+PA+'_'+BS,'cmuvsBias'+'_'+board+'_'+PA+'_'+BS,800,600)
        gmuvsBias = ROOT.TGraphErrors(len(amu),abias,amu,abiasU,amuU)
        gmuvsBias.SetName('#mu vs bias voltage')
        InitGraph(gmuvsBias,'#mu vs bias voltage','bias voltage (V)','#mu')
        SetStyleObj(obj=gmuvsBias,lineColor=ROOT.kRed)
        gmuvsBias.SetMinimum(-0.1)
        gmuvsBias.SetMaximum(0.1)
        gmuvsBias.GetXaxis().SetLimits(0.,500.)
        DrawObj(cmuvsBias,gmuvsBias,None,'AP',pathToFigures)

    outFileROOT.Close()

    return

###############
# 
# Main function
#

if __name__ == "__main__" :

    parser = argparse.ArgumentParser(description='Study the charge sharing as a function of the bias voltage for the May 2016 or late May 2016 test beam data.')

    parser.add_argument('--board',required=True,choices=boardList,help='board')
    parser.add_argument('--PA',required=True,choices=PAList,help='PA')
    parser.add_argument('--BS',required=True,choices=BSList,help='BS')

    args = parser.parse_args()

    # Parameters and configuration.
    board = args.board
    PA = args.PA
    BS = args.BS

    ChargeSharingvsBias(board,PA,BS)
