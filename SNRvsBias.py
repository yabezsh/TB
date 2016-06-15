#!/usr/bin/env python

"""
Author: Federica Lionetto
Date: May 22nd, 2016

Description:
    This script allows to study
    - the SNR
    - the number of 1-strip clusters
    - the number of 2-strip clusters
    - the fraction of 1-strip clusters
    - the fraction of 2-strip clusters
    as a function of the bias voltage for a given board, a given pitch adapter region, and a given biasing scheme.
    It opens the logbook and gets the subset corresponding to the desired bias voltage scan. After that, for each physics run, it reads the text file with SNR and corresponding uncertainty. Then, it creates a TGraph with the SNR as a function of the bias voltage.
    The following arguments can/have to be provided:
    - board (str): the board one wants to analyse (M1, M3, or M4);
    - PA (str): the pitch adapter region one wants to analyse (FanIn or FanUp);
    - BS (str): the biasing scheme (Top, Back, or Both). The 'Both' biasing scheme refers to the situation in which the sensor should have been biased from the back, but the jumpers were not set properly, so it has been actually biased both from the top and from the back. This should be treated as a 'Back' biasing scheme. 
    
How to run it:
    First of all, type

    SetupProject LHCb
    
    to set the environment.
    Then, type
    
    python -u SNRvsBias.py --board M3 --PA FanUp --BS Back | tee LogSNRvsBias-M3-FanUp-Back.dat
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

def SNRvsBias(board,PA,BS) :
    # Check that the specified PA exists for the specified board (it can be that M1 has FanIn only, and so on).
    # print PADict[board]
    if PA not in PADict[board] :
        print 'ERROR! The specified PA does not exist for the specified board.'
        exit()
    
    print '======================================================'
    print 'Studying the SNR as a function of the bias voltage for'
    print 'Board:', board
    print 'PA:', PA
    print 'BS:', BS
    print '===================='
    
    funName = 'SNRvsBias'

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
    # - read the text file with SNR and corresponding uncertainty and width and corresponding uncertainty.
    lSNR = []
    lSNRU = []
    lwidth = []
    lwidthU = []

    l1StripCluster = []
    l2StripCluster = []

    lf1StripCluster = []
    lf2StripCluster = []

    lbias = []
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

        bias = int(row['Bias voltage (V)'])
        print bias

        if bias not in lbias :

            filename = pathToInput+'output_'+str(DUTRun)+'/MPV_'+board+'_'+PA+'_'+str(DUTRun)+'_'+str(telescopeRun)+'.txt'
            if os.path.exists(filename) : 
                with open(filename,'r') as text_file :
                    text_file.readline()
                    values = text_file.readline().replace('\n','')
                    values_list = values.split(',')
                    SNR = values_list[0]
                    SNRU = values_list[1]
                    # !!! Uncomment it when the new jobs are done.
                    # width = values_list[2]
                    # widthU = values_list[3]
                    # !!! Until here.
                    # !!! Comment it when the new jobs are done.
                    width = 0.
                    widthU = 0.
                    # !!! Until here.
                    # print values
                    # print values_list
                    print 'SNR:', SNR
                    print 'SNR uncertainty:', SNRU
                    print 'Width:', width
                    print 'Width uncertainty:', widthU
                    lSNR.append(SNR)
                    lSNRU.append(SNRU)
                    lwidth.append(width)
                    lwidthU.append(widthU)
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
            
            lbias.append(bias)

    print lSNR
    print lSNRU
    print lwidth
    print lwidthU
    print lbias
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
        lSNRU.pop(toDrop)
        lwidth.pop(toDrop)
        lwidthU.pop(toDrop)
        lbias.pop(toDrop)

    print lSNR
    print lSNRU
    print lwidth
    print lwidthU
    print lbias
    print l1StripCluster
    print l2StripCluster
    print lf1StripCluster
    print lf2StripCluster
   
    # Remove duplicates.


    # Create a TGraph with the SNR as a function of the bias voltage.
    outFileROOT = ROOT.TFile(pathToOutput+funName+'_'+board+'_'+PA+'_'+BS+'.root','RECREATE')
    outFileROOT.cd()

    aSNR = np.asarray(lSNR,dtype=float) 
    aSNRU = np.asarray(lSNRU,dtype=float)

    awidth = np.asarray(lwidth,dtype=float) 
    awidthU = np.asarray(lwidthU,dtype=float)

    a1StripCluster = np.asarray(l1StripCluster,dtype=float)
    a2StripCluster = np.asarray(l2StripCluster,dtype=float)

    af1StripCluster = np.asarray(lf1StripCluster,dtype=float)
    af2StripCluster = np.asarray(lf2StripCluster,dtype=float)

    abias = np.asarray(lbias,dtype=float)
    abiasU = np.zeros(len(aSNR),dtype=float)

    cSNRvsBias = ROOT.TCanvas('cSNRvsBias'+'_'+board+'_'+PA+'_'+BS,'cSNRvsBias'+'_'+board+'_'+PA+'_'+BS,800,600)
    gSNRvsBias = ROOT.TGraphErrors(len(aSNR),abias,aSNR,abiasU,aSNRU)
    InitGraph(gSNRvsBias,'SNR vs bias voltage','Bias voltage (V)','SNR')
    SetStyleObj(obj=gSNRvsBias,lineColor=ROOT.kRed)
    gSNRvsBias.SetMinimum(0.)
    gSNRvsBias.SetMaximum(30.)
    gSNRvsBias.GetXaxis().SetLimits(0.,500.)
    DrawObj(cSNRvsBias,gSNRvsBias,None,'AP',pathToFigures)
    gSNRvsBias.SetName('gSNRvsBias'+'_'+board+'_'+PA+'_'+BS)
    gSNRvsBias.Write()

    cwidthvsBias = ROOT.TCanvas('cwidthvsBias'+'_'+board+'_'+PA+'_'+BS,'cwidthvsBias'+'_'+board+'_'+PA+'_'+BS,800,600)
    gwidthvsBias = ROOT.TGraphErrors(len(awidth),abias,awidth,abiasU,awidthU)
    InitGraph(gwidthvsBias,'Width of Landau distribution vs bias voltage','Bias voltage (V)','Width of Landau distribution')
    SetStyleObj(obj=gwidthvsBias,lineColor=ROOT.kRed)
    gwidthvsBias.SetMinimum(0.)
    gwidthvsBias.SetMaximum(30.)
    gwidthvsBias.GetXaxis().SetLimits(0.,500.)
    DrawObj(cwidthvsBias,gwidthvsBias,None,'AP',pathToFigures)
    gwidthvsBias.SetName('gwidthvsBias'+'_'+board+'_'+PA+'_'+BS)
    gwidthvsBias.Write()

    # Create a TGraph with the number of 1-strip clusters as a function of the bias voltage.
    c1StripClustervsBias = ROOT.TCanvas('c1StripClustervsBias'+'_'+board+'_'+PA+'_'+BS,'c1StripClustervsBias'+'_'+board+'_'+PA+'_'+BS,800,600)
    g1StripClustervsBias = ROOT.TGraph(len(a1StripCluster),abias,a1StripCluster)
    InitGraph(g1StripClustervsBias,'Number of 1-strip clusters vs bias voltage','Bias voltage (V)','Number of 1-strip clusters')
    SetStyleObj(obj=g1StripClustervsBias,lineColor=ROOT.kRed)
    DrawObj(c1StripClustervsBias,g1StripClustervsBias,None,'AP',pathToFigures)
    g1StripClustervsBias.SetName('g1StripClustervsBias'+'_'+board+'_'+PA+'_'+BS)
    g1StripClustervsBias.Write()

    # Create a TGraph with the number of 2-strip clusters as a function of the bias voltage.
    c2StripClustervsBias = ROOT.TCanvas('c2StripClustervsBias'+'_'+board+'_'+PA+'_'+BS,'c2StripClustervsBias'+'_'+board+'_'+PA+'_'+BS,800,600)
    g2StripClustervsBias= ROOT.TGraph(len(a2StripCluster),abias,a2StripCluster)
    InitGraph(g2StripClustervsBias,'Number of 2-strip clusters vs bias voltage','Bias voltage (V)','Number of 2-strip clusters')
    SetStyleObj(obj=g2StripClustervsBias,lineColor=ROOT.kRed)
    DrawObj(c2StripClustervsBias,g2StripClustervsBias,None,'AP',pathToFigures)
    g2StripClustervsBias.SetName('g2StripClustervsBias'+'_'+board+'_'+PA+'_'+BS)
    g2StripClustervsBias.Write()

    # Create a TGraph with the fraction of 1-strip clusters as a function of the bias voltage.
    cf1StripClustervsBias = ROOT.TCanvas('cf1StripClustervsBias'+'_'+board+'_'+PA+'_'+BS,'cf1StripClustervsBias'+'_'+board+'_'+PA+'_'+BS,800,600)
    gf1StripClustervsBias = ROOT.TGraph(len(af1StripCluster),abias,af1StripCluster)
    InitGraph(gf1StripClustervsBias,'Fraction of 1-strip clusters vs bias voltage','Bias voltage (V)','Fraction of 1-strip clusters')
    SetStyleObj(obj=gf1StripClustervsBias,lineColor=ROOT.kRed)
    gf1StripClustervsBias.GetXaxis().SetLimits(0.,500.)
    DrawObj(cf1StripClustervsBias,gf1StripClustervsBias,None,'AP',pathToFigures)
    gf1StripClustervsBias.SetName('gf1StripClustervsBias'+'_'+board+'_'+PA+'_'+BS)
    gf1StripClustervsBias.Write()

    # Create a TGraph with the fraction of 2-strip clusters as a function of the bias voltage.
    cf2StripClustervsBias = ROOT.TCanvas('cf2StripClustervsBias'+'_'+board+'_'+PA+'_'+BS,'cf2StripClustervsBias'+'_'+board+'_'+PA+'_'+BS,800,600)
    gf2StripClustervsBias = ROOT.TGraph(len(af2StripCluster),abias,af2StripCluster)
    InitGraph(gf2StripClustervsBias,'Fraction of 2-strip clusters vs bias voltage','Bias voltage (V)','Fraction of 2-strip clusters')
    SetStyleObj(obj=gf2StripClustervsBias,lineColor=ROOT.kRed)
    gf2StripClustervsBias.GetXaxis().SetLimits(0.,500.)
    DrawObj(cf2StripClustervsBias,gf2StripClustervsBias,None,'AP',pathToFigures)
    gf2StripClustervsBias.SetName('gf2StripClustervsBias'+'_'+board+'_'+PA+'_'+BS)
    gf2StripClustervsBias.Write()

    outFileROOT.Close()

    return

###############
# 
# Main function
#

if __name__ == "__main__" :

    parser = argparse.ArgumentParser(description='Study the SNR as a function of the bias voltage for the May 2016 or late May 2016 test beam data.')

    parser.add_argument('--board',required=True,choices=boardList,help='board')
    parser.add_argument('--PA',required=True,choices=PAList,help='PA')
    parser.add_argument('--BS',required=True,choices=BSList,help='BS')

    args = parser.parse_args()

    # Parameters and configuration.
    board = args.board
    PA = args.PA
    BS = args.BS

    SNRvsBias(board,PA,BS)
