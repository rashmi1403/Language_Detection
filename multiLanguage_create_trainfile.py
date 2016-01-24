##create training data from the given dataset
#To run: python multiLanguage_create_trainfile.py english.data french.data dutch.data german.data swedish.data training.data

import sys

def readdata(engfile,frenchfile,dutchfile,germanfile,swedishfile,traindata):
	with open(engfile,'r') as eng, open(frenchfile, 'r') as fr, open(dutchfile, 'r') as du, open(germanfile, 'r') as ge, open(swedishfile, 'r') as sw, open(traindata,'a') as train:
		i=0
		for line in eng.readlines():
			if(i<2500):
				msg='1 '+str(line)
				train.write(msg)
				i+=1
		i=0
		for line in fr.readlines():
			if(i<2500):
				msg='2 '+str(line)
				train.write(msg)
				i+=1
		i=0
		for line in du.readlines():
			if(i<2500):
				msg='3 '+str(line)
				train.write(msg)
				i+=1
		i=0
		for line in ge.readlines():
			if(i<2500):
				msg='4 '+str(line)
				train.write(msg)
				i+=1
		i=0
		for line in sw.readlines():
			if(i<2500):
				msg='5 '+str(line)
				train.write(msg)
				i+=1

if __name__=='__main__':
	engfile=sys.argv[1]
	frenchfile=sys.argv[2]
	dutchfile=sys.argv[3]
	germanfile=sys.argv[4]
	swedishfile=sys.argv[5]
	traindata=sys.argv[6]
	readdata(engfile,frenchfile,dutchfile,germanfile,swedishfile,traindata)