

import argparse

# parser = argparse.ArgumentParser("adapter analysis")

# parser.add_argument("-b","--board",type=str)
# parser.add_argument("-p","--pitch",type=str)
# parser.add_argument("-r","--run",type=str)
# parser.add_argument("-k","--kepler",type=str)

# args = parser.parse_args()

#list of environment vars to set
import os
# os.environ['OUTPUTPATH'] = "/eos/lhcb/testbeam/ut/TemporaryData/June2017/DQMTemporary"
# os.environ['BOARD'] = args.board
# os.environ['RUNPLACE'] = args.pitch #FanIn etc
# os.environ['RUNNUMBER'] = args.run #MAMBA run number
# os.environ['DEFRUN'] = args.kepler #KEPLER run number
# os.environ['SCANTYPE'] = "Bias" # Run_${SCANTYPE}_Scan...

##I added th3is one to control my actual output location
myoutpath = os.environ['OUTPUTPATH']

if not os.path.exists(myoutpath):
    os.makedirs(myoutpath)
os.environ['MYOUTPUTPATH'] = myoutpath

#my input file is at
#m_fileIndir = OUTPUTPATH/BOARD/RUNPLACE/output_adapter_RUNNUMBER/Run_SCANTYPE_Scan-BOARD-RUNPLACE-RUNNUMBER-DEFRUN_Tracks.root
## this is because my input is the output of TbUT
#my output goes to 
# MYOUTPUTPATH/AdapterAnalysis_BOARD_RUNPLACE_BIASV_RUNNUMBER.root




##this doesn't seem to work in ROOT 6 -- error messages talk about previous declarations of CMS functions on the same line
import ROOT
ROOT.gROOT.ProcessLine(".L "+os.environ["KEPLERROOT"]+"/../TbUT/scripts/CMS.C+");
ROOT.gROOT.ProcessLine(".L "+os.environ["KEPLERROOT"]+"/../TbUT/scripts/AnalysisBase.C+");
ROOT.gROOT.ProcessLine(".L "+os.environ["KEPLERROOT"]+"/../TbUT/scripts/SummaryAnalysis.C+");

a = ROOT.SummaryAnalysis()
a.Loop()
