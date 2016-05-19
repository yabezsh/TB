import sys
sys.path.append( '/afs/cern.ch/work/c/cbetanco/LHCb/KeplerDev_v3r0/Tb/Kepler/../TbUT/options/python' )
from TbUTClusterizator import TbUTClusterizator
app=TbUTClusterizator()
app.inputData="/afs/cern.ch/work/c/cbetanco/LHCb/KeplerDev_v3r0/Tb/Kepler/eos/lhcb/testbeam/ut/TemporaryData/May2016/MAMBA/M1/FanIn/Run_Bias_Scan-M1-FanIn-17-15013.dat"
app.isAType=False
app.sensorType = 'NType'
app.eventMax = 100000
app.pedestalInputData = "/afs/cern.ch/work/c/cbetanco/LHCb/KeplerDev_v3r0/Tb/Kepler/eos/lhcb/testbeam/ut/TemporaryData/May2016/DQM/M1/FanIn/output_17/Pedestal-M1-FanIn-5.dat"
app.eventNumberDisplay = 100
app.runClusterization()
