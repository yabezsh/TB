

import argparse

parser = argparse.ArgumentParser("adapter analysis")

parser.add_argument("-b","--board",type=str)
parser.add_argument("-p","--pitch",type=str)
parser.add_argument("-s","--sector",type=str)
parser.add_argument("-r","--run",type=str)
parser.add_argument("-k","--kepler",type=str)
parser.add_argument("-v","--volts",type=str, default="300V")
parser.add_argument("-t","--type",type=str, default='Bias')

args = parser.parse_args()

#list of environment vars to set
import os
os.environ['OUTPUTPATH'] = "/eos/lhcb/testbeam/ut/TemporaryData/October2016/DQM"
os.environ['BOARD'] = args.board
os.environ['RUNPLACE'] = args.pitch #FanIn etc
os.environ['RUNNUMBER'] = args.run #MAMBA run number
os.environ['DEFRUN'] = args.kepler #KEPLER run number
os.environ['SCANTYPE'] = args.type # Run_${SCANTYPE}_Scan...
os.environ['SECTORPOS'] = args.sector
os.environ['ROTATION'] = "0"

##I added th3is one to control my actual output location
myoutpath = "/afs/cern.ch/work/m/mrudolph/public/AdapterTiming/"
if not os.path.exists(myoutpath):
    os.makedirs(myoutpath)
os.environ['MYOUTPUTPATH'] = myoutpath
os.environ['BIASV'] = args.volts
os.environ['SENSORBIAS'] = args.volts

#my input file is at
#m_fileIndir = OUTPUTPATH/BOARD/RUNPLACE/output_adapter_RUNNUMBER/Run_SCANTYPE_Scan-BOARD-RUNPLACE-RUNNUMBER-DEFRUN_Tracks.root
## this is because my input is the output of TbUT
#my output goes to 
# MYOUTPUTPATH/AdapterAnalysis_BOARD_RUNPLACE_BIASV_RUNNUMBER.root


##this doesn't seem to work in ROOT 6 -- error messages talk about previous declarations of CMS functions on the same line
import ROOT
ROOT.gROOT.ProcessLine(".L CMS.C+");
ROOT.gROOT.ProcessLine(".L AnalysisBase.C+");
ROOT.gROOT.ProcessLine(".L AdapterTiming.C+");

a = ROOT.AdapterTiming()
a.Loop()
