import os,sys,getopt, subprocess

#telescopePath = "$KEPLERROOT/eos/lhcb/testbeam/ut/TelescopeData/July2015/RootFiles"
telescopePath = "$KEPLERROOT/eos/lhcb/testbeam/ut/TemporaryData/May2016/TimePix/RootFiles"

#inputPathPedestal = "$KEPLERROOT/eos/lhcb/testbeam/ut/OfficialData/July2015/BoardA6/RawData/"
#inputPathSignal = "$KEPLERROOT/eos/lhcb/testbeam/ut/OfficialData/July2015/BoardA6/RawData/"

#inputPathPedestal = "$KEPLERROOT/eos_sup/user/l/lhcbut/Testbeam/May2016/Board_M3_FanUp/"
#inputPathSignal = "$KEPLERROOT/eos_sup/user/l/lhcbut/Testbeam/May2016/Board_M3_FanUp/"
inputPathPedestal = "/afs/cern.ch/work/i/ibezshyi/public/TESTBEAM/data/"
inputPathSignal = "/afs/cern.ch/work/i/ibezshyi/public/TESTBEAM/data/"


pedFile = "Pedestal-M1-FanIn-51.dat"
#sigFile = "Run_Bias_Scan-B6-A-299-8431.dat"
sigFile = "Run_Bias_Scan-M1-FanIn-50-15027.dat"
if __name__=="__main__":
        try:
                opts,args = getopt.getopt(sys.argv[1:],"p:s:",["pedestal","signal"])
        except getopt.GetoptError as err:
                print str(err)
                usage()
                sys.exit(2)
        for o, a in opts:
                if o in ('-p','--pedestal'):
                        pedFile = str(a)
                if o in ('-s','--signal'):
                        sigFile = str(a)


inputFilePedestal = inputPathPedestal+pedFile
inputFileSignal = inputPathSignal+sigFile
print inputFilePedestal
print inputFileSignal
subprocess.call('source /afs/cern.ch/project/eos/installation/lhcb/etc/setup.sh',shell=True)
subprocess.call('/afs/cern.ch/project/eos/installation/0.3.15/bin/eos.select -b fuse mount $KEPLERROOT/eos',shell=True)
shFile = open(os.environ["KEPLERROOT"]+"/../run_k.sh","w")
shFile.write('#!/bin/bash\n')
shFile.write('cd $KEPLERROOT/../TbUT\n')
shFile.write('python options/TbUTPedestal_conf.py -f '+inputFilePedestal+"\n")
shFile.write('python options/TbUTRun_conf.py -f '+inputFileSignal+"\n")
shFile.write('cd ../../\n')
shFile.write('mkdir -p output\n')
shFile.write('cd output\n')
shFile.write('gaudirun.py $KEPLERROOT/../TbUT/options/TbUTPedestal.py\n')
shFile.write('gaudirun.py $KEPLERROOT/../TbUT/options/TbUTRun.py\n')
shFile.write('gaudirun.py $KEPLERROOT/../TbUT/options/TbUTRun.py\n')
shFile.write('. LbLogin.sh -c x86_64-slc6-gcc48-opt\n')
shFile.write('. SetupProject.sh LHCb v36r2\n')
shFile.write('cd ../Tb/TbUT/scripts/AddTrigTracks\n')
shFile.write('make\n')
shFile.write('cd ../../../../output\n')
shFile.write('pwd\n')
shFile.write('./../Tb/TbUT/scripts/AddTrigTracks/combDUTwithTrack -i '+sigFile[:-4]+'_Tuple.root -t '+telescopePath+'/Run'+sigFile.split('-')[4][:-4]+'/Kepler-tuple.root -n '+sigFile[:-4]+'.root -o '+sigFile[:-4]+'_Tracks.root\n')
os.environ['OUTPUTFILE'] = sigFile.split('-')[4][:-4]
os.environ['BOARD'] = sigFile.split('-')[1]
os.environ['RUNPLACE'] = sigFile.split('-')[2]
os.environ['RUNNUMBER'] = sigFile.split('-')[3]
os.environ['SCANTYPE'] = sigFile.split('-')[0].split('_')[1]
os.environ['DEFRUN'] = sigFile.split('-')[4][:-4]
os.environ['PEDESTALNUMBER'] = pedFile.split('-')[3][:-4]
shFile.write('\nmkdir -p Plots')
shFile.write('\nroot -b -q ../Tb/TbUT/scripts/runClusterWithTrackAna.C')
shFile.close()
subprocess.call("chmod +x "+os.environ["KEPLERROOT"]+"/../run_k.sh",shell=True)
os.system('/$KEPLERROOT/../run_k.sh')
