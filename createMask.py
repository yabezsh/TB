# script to generate a masking file
# python createMask.py -b 13HM2 -s 144 -e 207     ; also there is should be a file exceptions13_HM2, if you want to mask additional files 
import getopt, sys, os

def readExcept(excepFile):
	if os.path.exists(excepFile):
 	  with open(excepFile) as f:
		for line in f:
			int_exception = [int(i) for i in line.split()]
	else: int_exception = []
	return int_exception

def headerBitNoise():
	noise = []
	for N in xrange(1,16):
		noise.append(32*N+1)
		noise.append( 32*N+2)
	return noise
	

if __name__=="__main__":
        try:
                opts,args = getopt.getopt(sys.argv[1:],"b:s:e:",["board","start","end"])
        except getopt.GetoptError as err:
                print str(err)
                usage()
                sys.exit(2)
        for o, a in opts:
		if o in ('-b','--board'):
                        boardName = str(a)
		if o in ('-s','--start'):
			start = int(a)
		if o in ('-e','--end'):
			end = int(a)


	name = os.environ["KEPLERROOT"]+"/../TbUT/options/UT/MambaMasks_"+boardName+".dat"
	outputFile = open(name,"w")
	print start,"  ",end
	exeptionList = readExcept(os.environ["KEPLERROOT"]+"/../TbUT/options/UT/exceptions"+boardName+".dat")
	print exeptionList
	noise = headerBitNoise()
	print 'noise  ',noise
	for i in xrange(1,513):
		if i<start or i>end: outputFile.write("0\n")
		elif i in exeptionList: outputFile.write("0\n")
		elif i in noise: outputFile.write("0\n")
		else: outputFile.write("1\n")
	outputFile.close()
