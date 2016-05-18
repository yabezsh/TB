import sys, getopt, os
if __name__=="__main__":
	try:
		opts,args = getopt.getopt(sys.argv[1:],"f:",["file"])
	except getopt.GetoptError as err:
		print str(err)
		usage()
		sys.exit(2)
	for o, a in opts:
		if o in ('-f','--file'):
			fileName = str(a)
			print fileName
	if os.path.exists("options/TbUTPedestal.py"):os.system("rm options/TbUTPedestal.py")
	fileP = open("options/TbUTPedestal.py","a")
	fileP.write("import sys\n")
        fileP.write("sys.path.append( '../Tb/TbUT/options/python' )\n")
	fileP.write("from TbUTPedestalRunner import TbUTPedestalRunner\n")
	fileP.write("app=TbUTPedestalRunner()\n")
        fileP.write("app.inputData="+'"'+str(fileName)+'"'+"\n")
	fileP.write("app.isAType=False\n")
	fileP.write("app.eventMax=20000\n")
	fileP.write("app.pedestalOutputData ='$KEPLERROOT/../../output/"+os.path.basename(fileName)+"'\n")
	fileP.write("app.runPedestals()\n")
	fileP.close()

