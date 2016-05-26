import sys,getopt, os

if __name__=="__main__":
        try:
                opts,args = getopt.getopt(sys.argv[1:],"f:p:",["file"])
        except getopt.GetoptError as err:
                print str(err)
                usage()
                sys.exit(2)
        for o, a in opts:
                if o in ('-f','--file'):
                        fileName = str(a)
                        print fileName
                if o in ('-p'):
                        outputPath = str(a)
        if os.path.exists("options/TbUTRun.py"):os.system("rm options/TbUTRun.py")
        fileS = open("options/TbUTRun_"+os.environ["RUNNUMBER"]+".py","w")
        fileS.write("import sys\n")
        fileS.write("sys.path.append( '"+os.environ["KEPLERROOT"]+"/../TbUT/options/python' )\n")
	fileS.write("from TbUTClusterizator import TbUTClusterizator\n")
	fileS.write("app=TbUTClusterizator()\n")
	fileS.write("app.inputData="+'"'+str(fileName)+'"'+"\n")
        fileS.write("app.isAType=False\n")
        fileS.write("app.sensorType = '"+os.environ['sensorType']+"'\n")
	fileS.write("app.eventMax = -1\n")
	fileS.write('app.pedestalInputData = "'+outputPath+'/Pedestal-'+os.environ["BOARD"]+'-'+os.environ["RUNPLACE"]+'-'+os.environ["PEDESTALNUMBER"]+'.dat"\n')
	fileS.write('app.eventNumberDisplay = 100\n')
	fileS.write('app.runClusterization()\n')
        fileS.close()
