__author__ = 'ja'


import sys
sys.path.append("options/python")
from TbUTClusterizator import TbUTClusterizator

app = TbUTClusterizator()
# set parameters
#app.inputData = "data/Run_Bias_Scan-B1-A-229-8713.dat"
#app.inputData = "/afs/cern.ch/user/c/cbetanco/eos/lhcb/testbeam/ut/OfficialData/July2015/BoardA6/RawData/Run_Bias_Scan-B6-A-210-8356.dat"
#app.inputData = "/afs/cern.ch/user/c/cbetanco/eos/lhcb/testbeam/ut/OfficialData/July2015/BoardA6/RawData/Run_Bias_Scan-B6-A-299-8431.dat"
#app.inputData = "/afs/cern.ch/user/c/cbetanco/eos/lhcb/testbeam/ut/OfficialData/July2015/BoardA6/RawData/Run_Bias_Scan-B6-A-293-8425.dat"
app.inputData = "/afs/cern.ch/user/c/cbetanco/public/Custom-M1-FanIn-4-15005.dat"
app.isAType = False
app.sensorType = "NType"

app.eventMax = 100000
#app.pedestalInputData = "$KEPLERROOT/../TbUT/options/UT/ped-BoardA4Redo.dat"
app.pedestalInputData = "/afs/cern.ch/user/c/cbetanco/work/LHCb/KeplerDev_v3r0/Tb/TbUT/options/UT/test.dat"
app.eventNumberDisplay = 10

app.runClusterization()


