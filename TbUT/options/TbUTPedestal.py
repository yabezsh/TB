import sys
sys.path.append( '/afs/cern.ch/work/c/cbetanco/LHCb/KeplerDev_v3r0/Tb/Kepler/../TbUT/options/python' )
from TbUTPedestalRunner import TbUTPedestalRunner
app=TbUTPedestalRunner()
app.inputData="/afs/cern.ch/work/c/cbetanco/LHCb/KeplerDev_v3r0/Tb/Kepler/eos/lhcb/testbeam/ut/TemporaryData/May2016/MAMBA/M1/FanIn/Pedestal-M1-FanIn-5.dat"
app.isAType=False
app.eventMax=20000
app.pedestalOutputData ='/afs/cern.ch/work/c/cbetanco/LHCb/KeplerDev_v3r0/Tb/Kepler/eos/lhcb/testbeam/ut/TemporaryData/May2016/DQM/M1/FanIn/output_17/Pedestal-M1-FanIn-5.dat'
app.runPedestals()
