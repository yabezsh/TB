#!/usr/bin/env python

"""
Author: Federica Lionetto
Date: May 22nd, 2016

Description:

How to run it:
    
    python -u CombineSNRvsBias.py --PA FanIn --BS Top | tee LogCombineSNRvsBias-FanIn-Top.dat
"""

import argparse
import subprocess
import sys

import ROOT

sys.path.insert(0,'./Tools')
from DefineGlobalVariables import *
from ToolsForPython import *
from Style import *

def CombineSNRvsBias(PA,BS) :
    # Check that the specified PA exists for the specified board (it can be that M1 has FanIn only, and so on).
    # print PADict[board]
    # if PA not in PADict[board] :
        # print 'ERROR! The specified PA does not exist for the specified board.'
        # exit()
    
    print '======================================================'
    print 'Studying the SNR as a function of the bias voltage for'
    print 'PA:', PA
    print 'BS:', BS
    print '===================='
    
    funName = 'CombineSNRvsBias'

    # Mount EOS
    command = '/afs/cern.ch/project/eos/installation/0.3.15/bin/eos.select -b fuse mount ~/eos'
    print '>', command
    subprocess.call(command,shell=True)
    
    pathToOutput = DQM+funName+'/'
    print 'Path to output: ', pathToOutput
    pathToFigures = pathToOutput+'Figures/'
    print 'Path to figures: ', pathToFigures

    if not os.path.exists(pathToOutput) :
        os.makedirs(pathToOutput)
    if not os.path.exists(pathToFigures) :
        os.makedirs(pathToFigures)

    gM1 = ROOT.TGraphErrors()
    gM3 = ROOT.TGraphErrors()
    gM4 = ROOT.TGraphErrors()

    gwidthM1 = ROOT.TGraphErrors()
    gwidthM3 = ROOT.TGraphErrors()
    gwidthM4 = ROOT.TGraphErrors()
    
    for board in boardList :
        # Path to input data.
        pathToInput = DQM+board+'/'+PA+'/SNRvsBias/'
        print 'Path to input: ', pathToInput
        filename = pathToInput+'SNRvsBias_'+board+'_'+PA+'_'+BS+'.root'
        if os.path.exists(filename) : 
            print 'Filename:', filename
            inFileROOT = ROOT.TFile(filename,'READ')
            if board is 'M1' :
                gM1 = inFileROOT.Get('gSNRvsBias_'+board+'_'+PA+'_'+BS) 
                gwidthM1 = inFileROOT.Get('gwidthvsBias_'+board+'_'+PA+'_'+BS) 
            elif board is 'M3' :
                gM3 = inFileROOT.Get('gSNRvsBias_'+board+'_'+PA+'_'+BS) 
                gwidthM3 = inFileROOT.Get('gwidthvsBias_'+board+'_'+PA+'_'+BS) 
            elif board is 'M4' :
                gM4 = inFileROOT.Get('gSNRvsBias_'+board+'_'+PA+'_'+BS) 
                gwidthM4 = inFileROOT.Get('gwidthvsBias_'+board+'_'+PA+'_'+BS) 
        elif os.path.exists(filename.replace('Back','Both')) :
            print 'Filename (replacing back with both):', filename.replace('Back','Both')
            inFileROOT = ROOT.TFile(filename.replace('Back','Both'),'READ')
            if board is 'M1' :
                gM1 = inFileROOT.Get('gSNRvsBias_'+board+'_'+PA+'_'+BS.replace('Back','Both')) 
                gwidthM1 = inFileROOT.Get('gwidthvsBias_'+board+'_'+PA+'_'+BS.replace('Back','Both')) 
            elif board is 'M3' :
                gM3 = inFileROOT.Get('gSNRvsBias_'+board+'_'+PA+'_'+BS.replace('Back','Both')) 
                gwidthM3 = inFileROOT.Get('gwidthvsBias_'+board+'_'+PA+'_'+BS.replace('Back','Both')) 
            elif board is 'M4' :
                gM4 = inFileROOT.Get('gSNRvsBias_'+board+'_'+PA+'_'+BS.replace('Back','Both')) 
                gwidthM4 = inFileROOT.Get('gwidthvsBias_'+board+'_'+PA+'_'+BS.replace('Back','Both')) 

    if gM1 is not None and gM3 is not None and gM4 is not None and gwidthM1 is not None and gwidthM3 is not None and gwidthM4 is not None :
        
        outFileROOT = ROOT.TFile(pathToOutput+funName+'_'+PA+'_'+BS+'.root','RECREATE')



        gM1.SetLineColor(ROOT.kAzure-3)
        gM3.SetLineColor(ROOT.kViolet-1)
        gM4.SetLineColor(ROOT.kRed)

        gM1.SetMarkerColor(ROOT.kAzure-3)
        gM3.SetMarkerColor(ROOT.kViolet-1)
        gM4.SetMarkerColor(ROOT.kRed)
    
        gM1.SetLineStyle(1)
        gM3.SetLineStyle(3)
        gM4.SetLineStyle(7)

        gM1.SetLineWidth(2)
        gM3.SetLineWidth(2)
        gM4.SetLineWidth(2)
    
        objList = []
        objList.append(gM1)
        objList.append(gM3)
        objList.append(gM4)

        labelDict = {}
        labelDict[gM1.GetName()] = 'unirradiated'
        labelDict[gM3.GetName()] = 'nominal dose'
        labelDict[gM4.GetName()] = '2 x nominal dose'

        optionDict = {}
        optionDict[gM1.GetName()] = 'lp'
        optionDict[gM3.GetName()] = 'lp'
        optionDict[gM4.GetName()] = 'lp'

        drawOptionDict = {}
        drawOptionDict[gM1.GetName()] = 'APL'
        drawOptionDict[gM3.GetName()] = 'APL'
        drawOptionDict[gM4.GetName()] = 'APL'

        legSNRvsBias = CreateLegend(objList,labelDict,optionDict,0.60,0.23,0.90,0.53)

        # Create a TGraph with the SNR as a function of the bias voltage.
        cSNRvsBias = ROOT.TCanvas('cSNRvsBias'+'_'+PA+'_'+BS,'cSNRvsBias'+'_'+PA+'_'+BS,800,600)
        mgSNRvsBias = ROOT.TMultiGraph('mgSNRvsBias','SNR vs bias voltage')
        mgSNRvsBias.Add(gM1,'PL')
        mgSNRvsBias.Add(gM3,'PL')
        mgSNRvsBias.Add(gM4,'PL')
        mgSNRvsBias.SetMinimum(0.)
        mgSNRvsBias.SetMaximum(30.)
        gM1.GetXaxis().SetLimits(0.,500.)
        gM3.GetXaxis().SetLimits(0.,500.)
        gM4.GetXaxis().SetLimits(0.,500.)
        mgSNRvsBias.Draw('APL')
        cSNRvsBias.Update()
        InitGraph(mgSNRvsBias,'SNR vs bias voltage','Bias voltage (V)','SNR')
        DrawObj(cSNRvsBias,mgSNRvsBias,legSNRvsBias,'APL',pathToFigures)
        mgSNRvsBias.Write()


    
        gwidthM1.SetLineColor(ROOT.kAzure-3)
        gwidthM3.SetLineColor(ROOT.kViolet-1)
        gwidthM4.SetLineColor(ROOT.kRed)

        gwidthM1.SetMarkerColor(ROOT.kAzure-3)
        gwidthM3.SetMarkerColor(ROOT.kViolet-1)
        gwidthM4.SetMarkerColor(ROOT.kRed)
    
        gwidthM1.SetLineStyle(1)
        gwidthM3.SetLineStyle(3)
        gwidthM4.SetLineStyle(7)

        gwidthM1.SetLineWidth(2)
        gwidthM3.SetLineWidth(2)
        gwidthM4.SetLineWidth(2)

        objListWidth = []
        objListWidth.append(gwidthM1)
        objListWidth.append(gwidthM3)
        objListWidth.append(gwidthM4)

        labelDictWidth = {}
        labelDictWidth[gwidthM1.GetName()] = 'unirradiated'
        labelDictWidth[gwidthM3.GetName()] = 'nominal dose'
        labelDictWidth[gwidthM4.GetName()] = '2 x nominal dose'

        optionDictWidth = {}
        optionDictWidth[gwidthM1.GetName()] = 'lp'
        optionDictWidth[gwidthM3.GetName()] = 'lp'
        optionDictWidth[gwidthM4.GetName()] = 'lp'

        drawOptionDictWidth = {}
        drawOptionDictWidth[gwidthM1.GetName()] = 'APL'
        drawOptionDictWidth[gwidthM3.GetName()] = 'APL'
        drawOptionDictWidth[gwidthM4.GetName()] = 'APL'

        legwidthvsBias = CreateLegend(objListWidth,labelDictWidth,optionDictWidth,0.60,0.23,0.90,0.53)

        # Create a TGraph with the width as a function of the bias voltage.
        cwidthvsBias = ROOT.TCanvas('cwidthvsBias'+'_'+PA+'_'+BS,'cwidthvsBias'+'_'+PA+'_'+BS,800,600)
        mgwidthvsBias = ROOT.TMultiGraph('mgwidthvsBias','Width of Landau distribution vs bias voltage')
        mgwidthvsBias.Add(gwidthM1,'PL')
        mgwidthvsBias.Add(gwidthM3,'PL')
        mgwidthvsBias.Add(gwidthM4,'PL')
        mgwidthvsBias.SetMinimum(0.)
        mgwidthvsBias.SetMaximum(2.5)
        gwidthM1.GetXaxis().SetLimits(0.,500.)
        gwidthM3.GetXaxis().SetLimits(0.,500.)
        gwidthM4.GetXaxis().SetLimits(0.,500.)
        mgwidthvsBias.Draw('APL')
        cwidthvsBias.Update()
        InitGraph(mgwidthvsBias,'Width of Landau distribution vs bias voltage','Bias voltage (V)','Width of Landau distribution')
        DrawObj(cwidthvsBias,mgwidthvsBias,legwidthvsBias,'APL',pathToFigures)
        mgwidthvsBias.Write()



        outFileROOT.cd()
        outFileROOT.Close()

    else :
        print 'ERROR! Input not found.'

    return

###############
# 
# Main function
#

if __name__ == "__main__" :

    parser = argparse.ArgumentParser(description='Study the SNR as a function of the bias voltage for the May 2016 or late May 2016 test beam data.')

    parser.add_argument('--PA',required=True,choices=PAList,help='PA')
    parser.add_argument('--BS',required=True,choices=BSList,help='BS')

    args = parser.parse_args()

    # Parameters and configuration.
    PA = args.PA
    BS = args.BS

    CombineSNRvsBias(PA,BS)
