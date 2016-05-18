__author__ = 'ja'
import sys
sys.path.append( "options/python" )

from TbUTPedestalRunner import TbUTPedestalRunner
app=TbUTPedestalRunner()
# set parameter
#app.inputData= "/afs/cern.ch/user/a/adendek/eos/lhcb/testbeam/ut/OfficialData/July2015/BoardA6/RawData/Pedestal-B6-A-209-0.dat" 
#app.inputData= "/afs/cern.ch/user/c/cbetanco/eos/lhcb/testbeam/ut/OfficialData/July2015/BoardA6/RawData/Pedestal-B6-A-407-8522.dat"  
app.inputData = "/afs/cern.ch/user/c/cbetanco/public/Pedestal-M1-FanIn-5.dat"
app.isAType=False
# have to be more than 4k (~10k)
app.eventMax=100000
#  keep the pedestals files in $KEPLERROOT/../TbUT/options/UT/ directory !!!!!
app.pedestalOutputData ="$KEPLERROOT/../TbUT/options/UT/test.dat"

app.runPedestals()

