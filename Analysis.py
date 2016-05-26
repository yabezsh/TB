"""
python Analysis.py -b M1 -r FanIn -t pn -s Run_Bias_Scan-M1-FanIn-7-15008.dat -p Pedestal-M1-FanIn-8.dat
"""

import os,sys,getopt, subprocess

telescopePath = "$KEPLERROOT/eos/lhcb/testbeam/ut/TemporaryData/May2016/TimePix/RootFiles"
inputPathPedestal = "$KEPLERROOT/eos/lhcb/testbeam/ut/TemporaryData/May2016/MAMBA"
inputPathSignal = "$KEPLERROOT/eos/lhcb/testbeam/ut/TemporaryData/May2016/MAMBA"
outputPath = "$KEPLERROOT/eos/lhcb/testbeam/ut/TemporaryData/May2016/DQMTest"

boardName = "M1"
PA = "FanIn"

pedFile = "Pedestal-M1-FanIn-51.dat"
sigFile = "Run_Bias_Scan-M1-FanIn-50-15027.dat"

if __name__=="__main__":
        try:
                opts,args = getopt.getopt(sys.argv[1:],"p:s:b:r:t:",["pedestal","signal","board","PA","sensorType"])
        except getopt.GetoptError as err:
                print str(err)
                usage()
                sys.exit(2)
        for o, a in opts:
                if o in ('-p','--pedestal'):
                        pedFile = str(a)
                if o in ('-s','--signal'):
                        sigFile = str(a)
		if o in ('-b','--board'):
                        boardName = str(a)
		if o in ('-r','--PA'):
                        PA = str(a)
		if o in ('-t','--sensorType'):
			if str(a)=="np": os.environ['sensorType'] = 'PType'
                        if str(a)=="pn": os.environ['sensorType'] = 'NType'  	
			print 'Iaro  ',os.environ['sensorType']
if PA!="FanIn" and PA!="FanUp":
	sys.exit("Wrong PA option! Choose FanIn or FanUp!") 
if boardName!="M1" and boardName!="M2" and boardName!="M3" and boardName!="M4":
        sys.exit("Choose the right board: M1, M2, M3, M4")

print 'sigFile:', sigFile[:-4]

inputFilePedestal = inputPathPedestal+"/"+boardName+"/"+PA+"/"+pedFile
inputFileSignal = inputPathSignal+"/"+boardName+"/"+PA+"/"+sigFile
print "Input pedestal file:	"+inputFilePedestal
print "Input signal file:     "+inputFileSignal
subprocess.call('source /afs/cern.ch/project/eos/installation/lhcb/etc/setup.sh',shell=True)
subprocess.call('/afs/cern.ch/project/eos/installation/0.3.15/bin/eos.select -b fuse mount $KEPLERROOT/eos',shell=True)

os.environ['OUTPUTFILE'] = sigFile.split('-')[4][:-4]
os.environ['BOARD'] = sigFile.split('-')[1]
os.environ['RUNPLACE'] = sigFile.split('-')[2]
os.environ['RUNNUMBER'] = sigFile.split('-')[3]
os.environ['SCANTYPE'] = sigFile.split('-')[0].split('_')[1]
os.environ['DEFRUN'] = sigFile.split('-')[4][:-4]
os.environ['PEDESTALNUMBER'] = pedFile.split('-')[3][:-4]
os.environ['OUTPUTPATH'] = outputPath

shFile = open(os.environ["KEPLERROOT"]+"/../run_"+os.environ["RUNNUMBER"]+".sh","w")
shFile.write('#!/bin/bash\n')
shFile.write('cd $KEPLERROOT/../TbUT\n')
shFile.write('python options/TbUTPedestal_conf.py -f '+inputFilePedestal+" -p "+outputPath+'/'+boardName+'/'+PA+'/output_'+os.environ["RUNNUMBER"]+"\n")
shFile.write('python options/TbUTRun_conf.py -f '+inputFileSignal+" -p "+outputPath+'/'+boardName+'/'+PA+'/output_'+os.environ["RUNNUMBER"]+"\n")
shFile.write('mkdir -p '+outputPath+'/'+boardName+'/'+PA+'/output_'+os.environ["RUNNUMBER"]+'\n')
shFile.write('cd '+outputPath+'/'+boardName+'/'+PA+'/output_'+os.environ["RUNNUMBER"]+'\n')
shFile.write('echo "1 2 3 4" >>' +outputPath+'/'+boardName+'/'+PA+'/output_'+os.environ["RUNNUMBER"]+'/noise_Mamba.dat\n')
shFile.write('gaudirun.py $KEPLERROOT/../TbUT/options/TbUTPedestal_'+os.environ["RUNNUMBER"]+'.py\n')
shFile.write('gaudirun.py $KEPLERROOT/../TbUT/options/TbUTRun_'+os.environ["RUNNUMBER"]+'.py\n')
shFile.write('gaudirun.py $KEPLERROOT/../TbUT/options/TbUTRun_'+os.environ["RUNNUMBER"]+'.py\n')
shFile.write('. LbLogin.sh -c x86_64-slc6-gcc48-opt\n')
shFile.write('. SetupProject.sh LHCb v36r2\n')
shFile.write('cd '+os.environ["KEPLERROOT"]+'/../TbUT/scripts/AddTrigTracks\n')
shFile.write('make\n')
shFile.write('cd '+outputPath+'/'+boardName+'/'+PA+'/output_'+os.environ["RUNNUMBER"]+'\n')
shFile.write(os.environ["KEPLERROOT"]+'/../TbUT/scripts/AddTrigTracks/combDUTwithTrack -i '+sigFile[:-4]+'_Tuple.root -t '+telescopePath+'/Run'+sigFile.split('-')[4][:-4]+'/Kepler-tuple.root -n '+sigFile[:-4]+'.root -o '+sigFile[:-4]+'_Tracks.root\n')
shFile.write('\nmkdir -p '+outputPath+'/'+boardName+'/'+PA+'/output_'+os.environ["RUNNUMBER"]+'/Plots')
shFile.write('\nroot -b -q '+os.environ["KEPLERROOT"]+'/../TbUT/scripts/runClusterWithTrackAna.C')
shFile.close()
subprocess.call("chmod +x "+os.environ["KEPLERROOT"]+"/../run_"+os.environ["RUNNUMBER"]+".sh",shell=True)
os.system('/$KEPLERROOT/../run_'+os.environ["RUNNUMBER"]+'.sh')
if os.path.exists("./LogRunAnalysis_"+os.environ['BOARD']+"_"+os.environ['RUNPLACE']+".dat"):os.system("mv LogRunAnalysis_"+os.environ['BOARD']+"_"+os.environ['RUNPLACE']+".dat  "+outputPath+'/'+boardName+'/'+PA+'/')
if os.path.exists("/afs/cern.ch/work/i/ibezshyi/public/TESTBEAM/ChrisSoft/KeplerDev_v3r0/Tb/run_"+os.environ["RUNNUMBER"]+".sh"):os.system("mv /afs/cern.ch/work/i/ibezshyi/public/TESTBEAM/ChrisSoft/KeplerDev_v3r0/Tb/run_"+os.environ["RUNNUMBER"]+".sh  "+outputPath+'/'+boardName+'/'+PA+'/output_'+os.environ["RUNNUMBER"]+'/\n')
if os.path.exists("/afs/cern.ch/work/i/ibezshyi/public/TESTBEAM/ChrisSoft/KeplerDev_v3r0/Tb/clusterRun_"+os.environ["RUNNUMBER"]+".sh"):os.system("mv /afs/cern.ch/work/i/ibezshyi/public/TESTBEAM/ChrisSoft/KeplerDev_v3r0/Tb/clusterRun_"+os.environ["RUNNUMBER"]+".sh  "+outputPath+'/'+boardName+'/'+PA+'/output_'+os.environ["RUNNUMBER"]+'/\n')
