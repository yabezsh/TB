#!/usr/bin/env python

sensor='P_1'
hybrid='TTV2_01'

import sys
if len(sys.argv) > 2:
    sensor = sys.argv[1]
    hybrid = sys.argv[2]

print sensor, hybrid

rawdir='/eos/lhcb/testbeam/ut/TemporaryData/August2017/MAMBA'
kepdir='/eos/lhcb/testbeam/ut/TelescopeData/August2017/RootFiles'
outdir='/eos/lhcb/testbeam/ut/TemporaryData/August2017/DQMTemporary'

sys.path.insert(0,'./Tools')
from DefineGlobalVariables import *
from ToolsForPython import *
import os

logbook = 'Logbook/RunLogAugust2017Board'+sensor+'.csv'

logbook_df_san = GetInfoFromLogbook(logbook)
logbook_df_subset = logbook_df_san.loc[(logbook_df_san['Purpose'] == 'Bias scan') | (logbook_df_san['Purpose'] == 'Angle scan') | (logbook_df_san['Purpose'] == 'Eff/Res')].copy(deep=True)


print logbook_df_subset.head()
print logbook_df_subset.shape
for index,row in logbook_df_subset.iterrows():
    dutrun = int(row['DUT run'])
    keplerrun = int(row['Telescope run'])
    runtype = row['Purpose']
    print dutrun,keplerrun,runtype
    ##check input file exists
    if runtype == 'Bias scan':
        prefix= 'Run_Bias_Scan'
    elif runtype == 'Angle scan':
        prefix = 'Run_Angle_Scan'
    datfile = os.path.join( rawdir, sensor, '{}-{}-{}-{}-{}.dat'.format(prefix,hybrid,sensor,dutrun,keplerrun) )

    if not os.path.exists(datfile):
        print "ERROR: no input data file",datfile,"for run", dutrun
        continue

    trkfile = os.path.join( kepdir, 'Run{}'.format(keplerrun), 'Kepler-tuple.root')
    if not os.path.exists(trkfile):
        print "ERROR: no input tracks file",trkfile,"for run", dutrun
        continue
    

    clusterfile = os.path.join( outdir, sensor, 'output_{}'.format(dutrun), '{}-{}-{}-{}-{}_Tuple.root'.format(prefix,hybrid,sensor,dutrun,keplerrun))
    combfile = os.path.join( outdir, sensor, 'output_{}'.format(dutrun), '{}-{}-{}-{}-{}_Tracks.root'.format(prefix,hybrid,sensor,dutrun,keplerrun))
    if not os.path.exists( clusterfile ):
        print "ERROR: no output clusters",clusterfile,"for run",dutrun
        continue
    if not os.path.exists( combfile ):
        print "ERROR: no output clusters+tracks combined file for run",dutrun
        continue
        
    plotfile = os.path.join( outdir, sensor, 'output_{}'.format(dutrun), 'Plots', 'AnalysisOutput_{}_{}_{}_{}.root'.format( sensor, hybrid, dutrun, keplerrun ) )
    if not os.path.exists( plotfile ):
        print "ERROR: no plot file for run",dutrun
        continue
