"""
python Analysis.py -b M1 -r FanIn -t pn -s Run_Bias_Scan-M1-FanIn-7-15008.dat -p Pedestal-M1-FanIn-8.dat -m 0 -e 100
"""

import os,sys,getopt, subprocess

boardName = "M1"
#PA = "FanIn"
PA =""
NEvents = "-1"
mask = 0

pedFile = "Pedestal-M1-FanIn-51.dat"
sigFile = "Run_Bias_Scan-M1-FanIn-50-15027.dat"

if __name__=="__main__":

        	# Initialize these environment variables, in case they are not set
	os.environ['SECTORPOS'] = "0"
	os.environ['ROTATION'] = "0"
	os.environ['SENSORBIAS'] = "300"

	try:
                opts,args = getopt.getopt(sys.argv[1:],"p:s:b:r:t:e:m:l:y:v:",["pedestal","signal","board","PA","sensorType","events","mask","sector","rot","bias"])
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
		if o in ('-e','--events'):
			NEvents = str(a)
		if o in('-m','--mask'):
			if int(a)==0 or int(a)==1: mask = a
			else: sys.exit("choose right masking option: 0 or 1")
		if o in('-l','--sector'):
			if str(a)=="0" or str(a)=="1" or str(a)=="2": os.environ['SECTORPOS'] = str(a)			
			else: sys.exit("choose a sector: 0, 1 or 2")
		if o in('-y','--rot'):
			os.environ['ROTATION'] = str(a)
		if o in('-v','--bias'):
			os.environ['SENSORBIAS'] = str(a)

#if PA!="FanIn" and PA!="FanUp":
#	sys.exit("Wrong PA option! Choose FanIn or FanUp!") 
#if boardName!="M1" and boardName!="M2" and boardName!="M3" and boardName!="M4" and boardName!="F1" and boardName!="F3":
#        sys.exit("Choose the right board for a testbeam in the May 2016: M1, M3, M4, F1, F3. Otherwise, you need to check all paths.")


#telescopePath = "$KEPLERROOT/eos_"+str(sigFile.split('-')[3])+"/lhcb/testbeam/ut/TemporaryData/May2016/TimePix/RootFiles"
#telescopePath = "$KEPLERROOT/eos_"+str(sigFile.split('-')[3])+"/lhcb/testbeam/ut/TemporaryData/October2016/TelescopeFiles/RootFiles"
telescopePath = "$KEPLERROOT/eos_"+str(sigFile.split('-')[3])+"/lhcb/testbeam/ut/TelescopeData/Oct2016/RootFiles"


if boardName=="M1" or boardName=="M3" or boardName=="M4":
	inputPathPedestal = "$KEPLERROOT/eos_"+str(sigFile.split('-')[3])+"/lhcb/testbeam/ut/TemporaryData/May2016/MAMBA"
	inputPathSignal = "$KEPLERROOT/eos_"+str(sigFile.split('-')[3])+"/lhcb/testbeam/ut/TemporaryData/May2016/MAMBA"
elif boardName=="F1" or boardName=="F3":
	inputPathPedestal = "$KEPLERROOT/eos_"+str(sigFile.split('-')[3])+"/lhcb/testbeam/ut/TemporaryData/LateMay2016/MAMBA"
	inputPathSignal = "$KEPLERROOT/eos_"+str(sigFile.split('-')[3])+"/lhcb/testbeam/ut/TemporaryData/LateMay2016/MAMBA"
else:
	inputPathPedestal = "$KEPLERROOT/eos_"+str(sigFile.split('-')[3])+"/lhcb/testbeam/ut/TemporaryData/October2016/MAMBA"
        inputPathSignal = "$KEPLERROOT/eos_"+str(sigFile.split('-')[3])+"/lhcb/testbeam/ut/TemporaryData/October2016/MAMBA" 

#else:
#	sys.exit("Input files location is definded for a testbeam in the May 2016. Please go to Analysis.py and change inputPathPedestal and inputPathSignal")

#outputPath = "$KEPLERROOT/eos_"+str(sigFile.split('-')[3])+"/lhcb/testbeam/ut/TemporaryData/May2016/DQMTest"
#outputPath = "$KEPLERROOT/eos_"+str(sigFile.split('-')[3])+"/lhcb/testbeam/ut/TemporaryData/October2016/DQMTest"
outputPath = "$KEPLERROOT/eos_"+str(sigFile.split('-')[3])+"/lhcb/testbeam/ut/TemporaryData/October2016/DQMTemporary"

subprocess.call('source /afs/cern.ch/project/eos/installation/lhcb/etc/setup.sh',shell=True)
subprocess.call('/afs/cern.ch/project/eos/installation/0.3.15/bin/eos.select -b fuse mount $KEPLERROOT/eos_'+str(sigFile.split('-')[3]),shell=True)

if boardName=="M1" or boardName=="M2" or boardName=="M3" or boardName=="M4" or boardName=="F1" or boardName=="F3":
	os.environ['OUTPUTFILE'] = sigFile.split('-')[4][:-4]
	os.environ['BOARD'] = sigFile.split('-')[1]
	os.environ['RUNPLACE'] = sigFile.split('-')[2]
	os.environ['RUNNUMBER'] = sigFile.split('-')[3]
	os.environ['SCANTYPE'] = sigFile.split('-')[0].split('_')[1]
	os.environ['DEFRUN'] = sigFile.split('-')[4][:-4]
	os.environ['PEDESTALNUMBER'] = pedFile.split('-')[3][:-4]
	os.environ['OUTPUTPATH'] = outputPath
	os.environ['EVENTSNUMBER'] = NEvents
	inputFilePedestal = inputPathPedestal+"/"+boardName+"/"+PA+"/"+pedFile
	inputFileSignal = inputPathSignal+"/"+boardName+"/"+PA+"/"+sigFile

else:
        os.environ['OUTPUTFILE'] = sigFile.split('-')[4][:-4]
        os.environ['BOARD'] = sigFile.split('-')[2]
        os.environ['RUNPLACE'] = sigFile.split('-')[1]
        #os.environ['BOARD'] = sigFile.split('-')[1]
        #os.environ['RUNPLACE'] = sigFile.split('-')[2]
        os.environ['RUNNUMBER'] = sigFile.split('-')[3]
        os.environ['SCANTYPE'] = sigFile.split('-')[0].split('_')[1]
        os.environ['DEFRUN'] = sigFile.split('-')[4][:-4]
        os.environ['PEDESTALNUMBER'] = pedFile.split('-')[3][:-4]
        os.environ['OUTPUTPATH'] = outputPath
        os.environ['EVENTSNUMBER'] = NEvents
	inputFilePedestal = inputPathPedestal+"/"+boardName+"/"+pedFile
	inputFileSignal = inputPathSignal+"/"+boardName+"/"+sigFile
print "Input pedestal file:     "+inputFilePedestal
print "Input signal file:     "+inputFileSignal

if mask == 0: os.environ['MAMBAMASK'] = 'No'
else: os.environ['MAMBAMASK'] = os.environ['BOARD']
#else: os.environ['MAMBAMASK'] = os.environ['RUNPLACE']

shFile = open(os.environ["KEPLERROOT"]+"/../run_"+os.environ["RUNNUMBER"]+".sh","w")
shFile.write('#!/bin/bash\n')
shFile.write('cd $KEPLERROOT/../TbUT\n')
if PA=="":
	shFile.write('python options/TbUTPedestal_conf.py -f '+inputFilePedestal+" -p "+outputPath+'/'+boardName+'/output_'+os.environ["RUNNUMBER"]+"\n")
else:
        shFile.write('python options/TbUTPedestal_conf.py -f '+inputFilePedestal+" -p "+outputPath+'/'+boardName+'/'+PA+'/output_'+os.environ["RUNNUMBER"]+"\n")
if PA=="":
	shFile.write('python options/TbUTRun_conf.py -f '+inputFileSignal+" -p "+outputPath+'/'+boardName+'/output_'+os.environ["RUNNUMBER"]+"\n")
	shFile.write('mkdir -p '+outputPath+'/'+boardName+'/output_'+os.environ["RUNNUMBER"]+'\n')
	shFile.write('cd '+outputPath+'/'+boardName+'/output_'+os.environ["RUNNUMBER"]+'\n')
	shFile.write('echo "1 2 3 4" >>' +outputPath+'/'+boardName+'/output_'+os.environ["RUNNUMBER"]+'/noise_Mamba.dat\n')
else:
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
if PA=="":
	shFile.write('cd '+outputPath+'/'+boardName+'/output_'+os.environ["RUNNUMBER"]+'\n')
else:
        shFile.write('cd '+outputPath+'/'+boardName+'/'+PA+'/output_'+os.environ["RUNNUMBER"]+'\n')
if PA=="":
	shFile.write(os.environ["KEPLERROOT"]+'/../TbUT/scripts/AddTrigTracks/combDUTwithTrack -i '+sigFile[:-4]+'_Tuple.root -t '+telescopePath+'/Run'+sigFile.split('-')[4][:-4]+'/Kepler-tuple.root -n '+sigFile[:-4]+'.root -o '+sigFile[:-4]+'_Tracks.root\n')
else:
	shFile.write(os.environ["KEPLERROOT"]+'/../TbUT/scripts/AddTrigTracks/combDUTwithTrack -i '+sigFile[:-4]+'_Tuple.root -t '+telescopePath+'/Run'+sigFile.split('-')[4][:-4]+'/Kepler-tuple.root -n '+sigFile[:-4]+'.root -o '+sigFile[:-4]+'_Tracks.root\n')
if PA=="":
	shFile.write('\nmkdir -p '+outputPath+'/'+boardName+'/output_'+os.environ["RUNNUMBER"]+'/Plots')
else:
        shFile.write('\nmkdir -p '+outputPath+'/'+boardName+'/'+PA+'/output_'+os.environ["RUNNUMBER"]+'/Plots')
shFile.write('\nroot -b -q '+os.environ["KEPLERROOT"]+'/../TbUT/scripts/runClusterWithTrackAna.C')
shFile.close()
subprocess.call("chmod +x "+os.environ["KEPLERROOT"]+"/../run_"+os.environ["RUNNUMBER"]+".sh",shell=True)
os.system('/$KEPLERROOT/../run_'+os.environ["RUNNUMBER"]+'.sh')
if PA=="":
	if os.path.exists(os.environ["KEPLERROOT"]+"/../LogRunAnalysis_"+os.environ['BOARD']+"_"+os.environ['RUNPLACE']+".dat"):os.system("mv"+os.environ["KEPLERROOT"]+"/../LogRunAnalysis_"+os.environ['BOARD']+"_"+os.environ['RUNPLACE']+".dat  "+outputPath+'/'+boardName+'/')
else:
	if os.path.exists(os.environ["KEPLERROOT"]+"/../LogRunAnalysis_"+os.environ['BOARD']+"_"+os.environ['RUNPLACE']+".dat"):os.system("mv"+os.environ["KEPLERROOT"]+"/../LogRunAnalysis_"+os.environ['BOARD']+"_"+os.environ['RUNPLACE']+".dat  "+outputPath+'/'+boardName+'/'+PA+'/')
if os.path.exists(os.environ["KEPLERROOT"]+"/../run_"+os.environ["RUNNUMBER"]+".sh"):os.system("mv"+os.environ["KEPLERROOT"]+"/../run_"+os.environ["RUNNUMBER"]+".sh  "+outputPath+'/'+boardName+'/'+PA+'/output_'+os.environ["RUNNUMBER"]+'/\n')
if os.path.exists(os.environ["KEPLERROOT"]+"/../clusterRun_"+os.environ["RUNNUMBER"]+".sh"):os.system("mv"+os.environ["KEPLERROOT"]+"/../clusterRun_"+os.environ["RUNNUMBER"]+".sh  "+outputPath+'/'+boardName+'/'+PA+'/output_'+os.environ["RUNNUMBER"]+'/\n')
