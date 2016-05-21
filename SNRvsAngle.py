#!/usr/bin/env python

"""
Author: Federica Lionetto
Date: May 20th, 2016

Description:
    This script allows to study
    - the SNR
    - the number of 1-strip clusters
    - the number of 2-strip clusters
    - the fraction of 1-strip clusters
    - the fraction of 2-strip clusters
    as a function of the angle for a given board, a given pitch adapter region, and a given biasing scheme.
    It opens the logbook and gets the subset corresponding to the desired angle scan. After that, for each physics run, it reads the text file with SNR and corresponding uncertainty. Then, it creates a TGraph with the SNR as a function of the angle.
    The following arguments can/have to be provided:
    - board (str): the board one wants to analyse (M1, M3, or M4);
    - PA (str): the pitch adapter region one wants to analyse (FanIn or FanUp);
    - BS (str): the biasing scheme (Top or Back).
    
How to run it:
    First of all, type

    SetupProject LHCb
    
    to set the environment.
    Then, type
    
    python -u SNRvsAngle.py --board M3 --PA FanUp --BS Back | tee LogSNRvsAngle.dat
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

    # Mount EOS
    command = '/afs/cern.ch/project/eos/installation/0.3.15/bin/eos.select -b fuse mount ~/eos'
    print '>', command
    subprocess.call(command,shell=True)
    
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

    l1StripCluster = []
    l2StripCluster = []

    lf1StripCluster = []
    lf2StripCluster = []

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

        filename = pathToInput+'output_'+str(DUTRun)+'/MPV_'+board+'_'+PA+'_'+str(DUTRun)+'_'+str(telescopeRun)+'.txt'
        if os.path.exists(filename) : 
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
                langle.append(angle)
                text_file.closed

            filename = pathToInput+'output_'+str(DUTRun)+'/Plots/AnalysisOutput_'+board+'_'+PA+'_'+str(DUTRun)+'_'+str(telescopeRun)+'.root'
            print filename
            inFileROOTClusterSize = ROOT.TFile(filename,'READ')
            hclusterSize = inFileROOTClusterSize.Get('h12cc') 
            entries = hclusterSize.GetEntries()
            print 'Entries:', entries
            if entries == 0 :
                print 'ERROR! Found histogram with zero entries.'
            print hclusterSize
            oneStripCluster = hclusterSize.GetBinContent(hclusterSize.FindBin(1))
            print oneStripCluster
            l1StripCluster.append(oneStripCluster)
            if entries == 0 :
                lf1StripCluster.append(-1.)
            else :
                lf1StripCluster.append(oneStripCluster/entries)
            twoStripCluster = hclusterSize.GetBinContent(hclusterSize.FindBin(2))
            print twoStripCluster
            l2StripCluster.append(twoStripCluster)
            if entries == 0 :
                lf2StripCluster.append(-1.)
            else :
                lf2StripCluster.append(twoStripCluster/entries)

    print lSNR
    print lSNRU
    print langle
    print l1StripCluster
    print l2StripCluster
    print lf1StripCluster
    print lf2StripCluster

    # Remove runs without entries.
    # !!! This problem should be fixed somewhere else.
    if -1 in lf1StripCluster :
        toDrop = lf1StripCluster.index(-1)
        print 'No entries for:', toDrop
        l1StripCluster.pop(toDrop)
        l2StripCluster.pop(toDrop)
        lf1StripCluster.pop(toDrop)
        lf2StripCluster.pop(toDrop)
        lSNR.pop(toDrop)
        langle.pop(toDrop)

    print lSNR
    print lSNRU
    print langle
    print l1StripCluster
    print l2StripCluster
    print lf1StripCluster
    print lf2StripCluster
    
    # Create a TGraph with the SNR as a function of the angle.
    outFileROOT = ROOT.TFile(pathToOutput+funName+'_'+board+'_'+PA+'_'+BS+'.root','RECREATE')
    
    aSNR = np.asarray(lSNR,dtype=float) 
    aSNRU = np.asarray(lSNRU,dtype=float)

    a1StripCluster = np.asarray(l1StripCluster,dtype=float)
    a2StripCluster = np.asarray(l2StripCluster,dtype=float)

    af1StripCluster = np.asarray(lf1StripCluster,dtype=float)
    af2StripCluster = np.asarray(lf2StripCluster,dtype=float)

    aangle = np.asarray(langle,dtype=float)
    aangleU = np.zeros(len(aSNR),dtype=float)

    cSNRvsAngle = ROOT.TCanvas('cSNRvsAngle'+'_'+board+'_'+PA+'_'+BS,'cSNRvsAngle'+'_'+board+'_'+PA+'_'+BS,800,600)
    gSNRvsAngle = ROOT.TGraphErrors(len(aSNR),aangle,aSNR,aangleU,aSNRU)
    gSNRvsAngle.SetName('SNR vs angle')
    InitGraph(gSNRvsAngle,'SNR vs angle','Angle','SNR')
    SetStyleObj(obj=gSNRvsAngle,lineColor=ROOT.kRed)
    gSNRvsAngle.SetMinimum(20.)
    gSNRvsAngle.SetMaximum(30.)
    gSNRvsAngle.GetXaxis().SetLimits(-12.,22.)

    # Fit.
    # SNR(theta) = SNR(alpha) / cos(theta-alpha)
    minFit = min(langle)
    maxFit = max(langle)
    fSNRvsAngle = ROOT.TF1('fSNRvsAngle','[0]/cos((x-[1])*3.14159/180.)',minFit,maxFit)
    fSNRvsAngle.SetParameter(0,0.)
    fSNRvsAngle.SetParLimits(0,0.,50.)
    gSNRvsAngle.Fit('fSNRvsAngle','R')
    SNRAnglePeak = fSNRvsAngle.GetParameter(1)
    SNRAnglePeakU = fSNRvsAngle.GetParError(1)
    SNRPeak = fSNRvsAngle.Eval(SNRAnglePeak)
    print 'Angle at the peak:', SNRAnglePeak, '+/-', SNRAnglePeakU 
    print 'Signal at the peak:', SNRPeak
    DrawObj(cSNRvsAngle,gSNRvsAngle,None,'AP',pathToFigures)
   
    # Create a TGraph with the number of 1-strip clusters as a function of the angle.
    c1StripClustervsAngle = ROOT.TCanvas('c1StripClustervsAngle'+'_'+board+'_'+PA+'_'+BS,'c1StripClustervsAngle'+'_'+board+'_'+PA+'_'+BS,800,600)
    g1StripClustervsAngle = ROOT.TGraph(len(a1StripCluster),aangle,a1StripCluster)
    g1StripClustervsAngle.SetName('Number of 1-strip clusters vs angle')
    InitGraph(g1StripClustervsAngle,'Number of 1-strip clusters vs angle','Angle','Number of 1-strip clusters')
    SetStyleObj(obj=g1StripClustervsAngle,lineColor=ROOT.kRed)
    DrawObj(c1StripClustervsAngle,g1StripClustervsAngle,None,'AP',pathToFigures)

    # Create a TGraph with the number of 2-strip clusters as a function of the angle.
    c2StripClustervsAngle = ROOT.TCanvas('c2StripClustervsAngle'+'_'+board+'_'+PA+'_'+BS,'c2StripClustervsAngle'+'_'+board+'_'+PA+'_'+BS,800,600)
    g2StripClustervsAngle = ROOT.TGraph(len(a2StripCluster),aangle,a2StripCluster)
    g2StripClustervsAngle.SetName('Number of 2-strip clusters vs angle')
    InitGraph(g2StripClustervsAngle,'Number of 2-strip clusters vs angle','Angle','Number of 2-strip clusters')
    SetStyleObj(obj=g2StripClustervsAngle,lineColor=ROOT.kRed)
    DrawObj(c2StripClustervsAngle,g2StripClustervsAngle,None,'AP',pathToFigures)
    
    # Create a TGraph with the fraction of 1-strip clusters as a function of the angle.
    cf1StripClustervsAngle = ROOT.TCanvas('cf1StripClustervsAngle'+'_'+board+'_'+PA+'_'+BS,'cf1StripClustervsAngle'+'_'+board+'_'+PA+'_'+BS,800,600)
    gf1StripClustervsAngle = ROOT.TGraph(len(af1StripCluster),aangle,af1StripCluster)
    gf1StripClustervsAngle.SetName('Fraction of 1-strip clusters vs angle')
    InitGraph(gf1StripClustervsAngle,'Fraction of 1-strip clusters vs angle','Angle','Fraction of 1-strip clusters')
    SetStyleObj(obj=gf1StripClustervsAngle,lineColor=ROOT.kRed)
    gf1StripClustervsAngle.GetXaxis().SetLimits(-12.,22.)
    # Fit.
    # Second-order polynomial function.
    # minFit = min(langle)
    # maxFit = max(langle)
    minFit = -5.
    maxFit = 5.
    ff1StripClustervsAngle = ROOT.TF1('ff1StripClustervsAngle','pol2',minFit,maxFit)
    SetStyleObj(obj=ff1StripClustervsAngle,lineColor=ROOT.kRed)
    ff1StripClustervsAngle.SetParLimits(2,-2.,0.)
    gf1StripClustervsAngle.Fit('ff1StripClustervsAngle','R')
    f1StripClusterAnglePeak = -1*(ff1StripClustervsAngle.GetParameter(1))/(2*ff1StripClustervsAngle.GetParameter(2))
    f1StripClusterPeak = ff1StripClustervsAngle.Eval(f1StripClusterAnglePeak)
    f1StripClusterAnglePeakU = math.sqrt((ff1StripClustervsAngle.GetParError(1)/(2*ff1StripClustervsAngle.GetParameter(2)))**2+((ff1StripClustervsAngle.GetParameter(1)*ff1StripClustervsAngle.GetParError(2))/(2*((ff1StripClustervsAngle.GetParameter(2))**2)))**2)
    print 'Angle at the peak:', f1StripClusterAnglePeak, '+/-', f1StripClusterAnglePeakU
    print 'Signal at the peak:', f1StripClusterPeak
    DrawObj(cf1StripClustervsAngle,gf1StripClustervsAngle,None,'AP',pathToFigures)
    
    # Create a TGraph with the fraction of 2-strip clusters as a function of the angle.
    cf2StripClustervsAngle = ROOT.TCanvas('cf2StripClustervsAngle'+'_'+board+'_'+PA+'_'+BS,'cf2StripClustervsAngle'+'_'+board+'_'+PA+'_'+BS,800,600)
    gf2StripClustervsAngle = ROOT.TGraph(len(af2StripCluster),aangle,af2StripCluster)
    gf2StripClustervsAngle.SetName('Fraction of 2-strip clusters vs angle')
    InitGraph(gf2StripClustervsAngle,'Fraction of 2-strip clusters vs angle','Angle','Fraction of 2-strip clusters')
    SetStyleObj(obj=gf2StripClustervsAngle,lineColor=ROOT.kRed)
    gf2StripClustervsAngle.GetXaxis().SetLimits(-12.,22.)
    # Fit.
    # Second-order polynomial function.
    # minFit = min(langle)
    # maxFit = max(langle)
    minFit = -5.
    maxFit = 5.
    ff2StripClustervsAngle = ROOT.TF1('ff2StripClustervsAngle','pol2',minFit,maxFit)
    SetStyleObj(obj=ff2StripClustervsAngle,lineColor=ROOT.kRed)
    ff2StripClustervsAngle.SetParLimits(2,0.,2.)
    gf2StripClustervsAngle.Fit('ff2StripClustervsAngle','R')
    f2StripClusterAnglePeak = -1*(ff2StripClustervsAngle.GetParameter(1))/(2*ff2StripClustervsAngle.GetParameter(2))
    f2StripClusterPeak = ff2StripClustervsAngle.Eval(f2StripClusterAnglePeak)
    f2StripClusterAnglePeakU = math.sqrt((ff2StripClustervsAngle.GetParError(1)/(2*ff2StripClustervsAngle.GetParameter(2)))**2+((ff2StripClustervsAngle.GetParameter(1)*ff2StripClustervsAngle.GetParError(2))/(2*((ff2StripClustervsAngle.GetParameter(2))**2)))**2)
    print 'Angle at the peak:', f2StripClusterAnglePeak, '+/-', f2StripClusterAnglePeakU
    print 'Signal at the peak:', f2StripClusterPeak
    DrawObj(cf2StripClustervsAngle,gf2StripClustervsAngle,None,'AP',pathToFigures)
    '''
    ff2StripClustervsAngle = ROOT.TF1('ff2StripClustervsAngle','[0]/cos((x-[1])*3.14159/180.)',minFit,maxFit)
    ff2StripClustervsAngle.SetParLimits(0,0.16,0.20)
    ff2StripClustervsAngle.SetParLimits(1,-2.,2.)
    gf2StripClustervsAngle.Fit('ff2StripClustervsAngle','R')
    DrawObj(cf2StripClustervsAngle,gf2StripClustervsAngle,None,'AP',pathToFigures)
    '''

    # Create a TGraph with the resolution of 2-strip clusters as a function of the angle (fit with a Gaussian of the DeltaX).
    
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
