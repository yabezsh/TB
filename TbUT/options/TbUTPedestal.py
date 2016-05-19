import sys
sys.path.append( '/afs/cern.ch/work/f/flionett/LHCb/UTTestBeam/Repository/KeplerDev_v3r0/Tb/Kepler/../TbUT/options/python' )
from TbUTPedestalRunner import TbUTPedestalRunner
app=TbUTPedestalRunner()
app.inputData="/afs/cern.ch/work/f/flionett/LHCb/UTTestBeam/Repository/KeplerDev_v3r0/Tb/Kepler/eos/lhcb/testbeam/ut/TemporaryData/May2016/MAMBA/M1/FanIn/Pedestal-M1-FanIn-8.dat"
app.isAType=False
app.eventMax=20000
app.pedestalOutputData ='/afs/cern.ch/work/f/flionett/LHCb/UTTestBeam/Repository/KeplerDev_v3r0/Tb/Kepler/eos/lhcb/testbeam/ut/TemporaryData/May2016/DQM/M1/FanIn/output_7/Pedestal-M1-FanIn-8.dat'
app.runPedestals()
