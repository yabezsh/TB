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
			if int(a)==0 or int(a)==1: mask = int(a)
			else: sys.exit("choose right masking option: 0 or 1")
		if o in('-l','--sector'):
                        os.environ['SECTORPOS'] = str(a)			
		if o in('-y','--rot'):
			os.environ['ROTATION'] = str(a)
		if o in('-v','--bias'):
			os.environ['SENSORBIAS'] = str(a)
		

#telescopePath = "$KEPLERROOT/eos_"+str(sigFile.split('-')[3])+"/lhcb/testbeam/ut/TemporaryData/May2016/TimePix/RootFiles"
#telescopePath = "$KEPLERROOT/eos_"+str(sigFile.split('-')[3])+"/lhcb/testbeam/ut/TemporaryData/October2016/TelescopeFiles/RootFiles"
#telescopePath = "$KEPLERROOT/eos_"+str(sigFile.split('-')[3])+"/lhcb/testbeam/ut/TelescopeData/Oct2016/RootFiles"
telescopePath = "/eos/lhcb/testbeam/ut/TelescopeData/June2017/RootFiles"
telescopePath = "/eos/lhcb/testbeam/ut/TelescopeData/August2017/RootFiles"



#outputPath = "$KEPLERROOT/eos_"+str(sigFile.split('-')[3])+"/lhcb/testbeam/ut/TemporaryData/May2016/DQMTest"
#outputPath = "$KEPLERROOT/eos_"+str(sigFile.split('-')[3])+"/lhcb/testbeam/ut/TemporaryData/October2016/DQMTest"
#outputPath = "/afs/cern.ch/work/m/mrudolph/public/testbeam/ut/TemporaryData/October2016/DQMTemporary"
outputPath = "/eos/lhcb/testbeam/ut/TemporaryData/June2017/DQMTemporary"
#outputPath = "/eos/lhcb/testbeam/ut/TemporaryData/August2017/DQMTemporary"
#outputPath = "/afs/cern.ch/work/m/mrudolph/public/testbeam/August2017"


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

else:
        os.environ['OUTPUTFILE'] = sigFile.split('-')[4][:-4]
        os.environ['BOARD'] = sigFile.split('-')[2]
        os.environ['RUNPLACE'] = sigFile.split('-')[1]
        os.environ['RUNNUMBER'] = sigFile.split('-')[3]
        os.environ['SCANTYPE'] = sigFile.split('-')[0].split('_')[1]
        os.environ['DEFRUN'] = sigFile.split('-')[4][:-4]
        os.environ['PEDESTALNUMBER'] = pedFile.split('-')[3][:-4]
        os.environ['OUTPUTPATH'] = outputPath
        os.environ['EVENTSNUMBER'] = NEvents


if mask == 0: os.environ['MAMBAMASK'] = 'No'
else: os.environ['MAMBAMASK'] = os.environ['BOARD']

shFile = open(os.environ["KEPLERROOT"]+"/../runsummary_"+os.environ["RUNNUMBER"]+".sh","w")
shFile.write('#!/bin/bash\n')

if PA=="":
	shFile.write('\nmkdir -p '+outputPath+'/'+boardName+'/output_'+os.environ["RUNNUMBER"]+'/Plots')
else:
        shFile.write('\nmkdir -p '+outputPath+'/'+boardName+'/'+PA+'/output_'+os.environ["RUNNUMBER"]+'/Plots')

shFile.write('\ncd ' +outputPath+'/'+boardName+'/'+PA+'/output_'+os.environ["RUNNUMBER"] )
shFile.write('\nlb-run ROOT python '+os.environ["KEPLERROOT"]+'/../TbUT/scripts/runsummary.py -b')
shFile.close()

subprocess.call("chmod +x "+os.environ["KEPLERROOT"]+"/../runsummary_"+os.environ["RUNNUMBER"]+".sh",shell=True)
os.system('$KEPLERROOT/../runsummary_'+os.environ["RUNNUMBER"]+'.sh')

if PA=="":
	if os.path.exists(os.environ["KEPLERROOT"]+"/../LogRunAnalysis_"+os.environ['BOARD']+"_"+os.environ['RUNPLACE']+".dat"):
                os.system("mv "+os.environ["KEPLERROOT"]+"/../LogRunAnalysis_"+os.environ['BOARD']+"_"+os.environ['RUNPLACE']+".dat  "+outputPath+'/'+boardName+'/')
else:
	if os.path.exists(os.environ["KEPLERROOT"]+"/../LogRunAnalysis_"+os.environ['BOARD']+"_"+os.environ['RUNPLACE']+".dat"):
                os.system("mv "+os.environ["KEPLERROOT"]+"/../LogRunAnalysis_"+os.environ['BOARD']+"_"+os.environ['RUNPLACE']+".dat  "+outputPath+'/'+boardName+'/'+PA+'/')

if os.path.exists(os.environ["KEPLERROOT"]+"/../runsummary_"+os.environ["RUNNUMBER"]+".sh"):
        os.system("mv "+os.environ["KEPLERROOT"]+"/../runsummary_"+os.environ["RUNNUMBER"]+".sh  "+outputPath+'/'+boardName+'/'+PA+'/output_'+os.environ["RUNNUMBER"]+'/\n')
