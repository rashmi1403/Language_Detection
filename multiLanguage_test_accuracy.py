#test accuracy and calculate precision, recall and F1 scores
#python multiLanguage_test_accuracy.py output.out reference.out

import sys

output=sys.argv[1]
reference=sys.argv[2]

def performance():
	with open(output,'r') as op,open(reference,'r') as ref:
		precision=0
		reflist=[]
		oplist=[]
		for (line,data) in zip(op.readlines(),ref.readlines()):
			words=line.split()
			dat=data.split()

			oplist.append(words[0])
			reflist.append(dat[0])
							
			if(words[0]==dat[0]):
				precision+=1
			#else:
				#print(words[0],' ',data[0])

		#print("precision=",precision)
		accuracy = precision / 12500.0
		print("overall accuracy=",accuracy*100)

		TP=0
		FP=0
		FN=0

		i=0
		while i<2500:
			if(oplist[i]=='1' and reflist[i]!='1'):
				FP+=1
			if(reflist[i]=='1' and oplist[i]!='1'):
				FN+=1
			if(reflist[i]=='1' and oplist[i]=='1'):
				TP+=1
			i+=1	

		#print('TP=',TP,' FP=',FP,' FN=',FN)
		precision=TP/float(TP+FP)  
		recall=TP/float(TP+FN)
		fscore=(2*precision*recall)/(precision+recall)
		print("Values for English data:")
		print('Precision =',precision,' Recall =',recall,' F-Score=',fscore)

		TP=0
		FP=0
		FN=0

		i=0
		while i<5000:
			if(oplist[i]=='2' and reflist[i]!='2'):
				FP+=1
			if(reflist[i]=='2' and oplist[i]!='2'):
				FN+=1
			if(reflist[i]=='2' and oplist[i]=='2'):
				TP+=1
			i+=1	

		#print('TP=',TP,' FP=',FP,' FN=',FN)
		precision=TP/float(TP+FP)  
		recall=TP/float(TP+FN)
		fscore=(2*precision*recall)/(precision+recall)
		print("Values for French data:")
		print('Precision =',precision,' Recall =',recall,' F-Score=',fscore)

		TP=0
		FP=0
		FN=0

		i=0
		while i<7500:
			if(oplist[i]=='3' and reflist[i]!='3'):
				FP+=1
			if(reflist[i]=='3' and oplist[i]!='3'):
				FN+=1
			if(reflist[i]=='3' and oplist[i]=='3'):
				TP+=1
			i+=1	

		#print('TP=',TP,' FP=',FP,' FN=',FN)
		precision=TP/float(TP+FP)  
		recall=TP/float(TP+FN)
		fscore=(2*precision*recall)/(precision+recall)
		print("Values for Dutch data:")
		print('Precision =',precision,' Recall =',recall,' F-Score=',fscore)

		TP=0
		FP=0
		FN=0

		i=0
		while i<10000:
			if(oplist[i]=='4' and reflist[i]!='4'):
				FP+=1
			if(reflist[i]=='4' and oplist[i]!='4'):
				FN+=1
			if(reflist[i]=='4' and oplist[i]=='4'):
				TP+=1
			i+=1	

		#print('TP=',TP,' FP=',FP,' FN=',FN)
		precision=TP/float(TP+FP)  
		recall=TP/float(TP+FN)
		fscore=(2*precision*recall)/(precision+recall)
		print("Values for German data:")
		print('Precision =',precision,' Recall =',recall,' F-Score=',fscore)

		TP=0
		FP=0
		FN=0

		i=0
		while i<12500:
			if(oplist[i]=='5' and reflist[i]!='5'):
				FP+=1
			if(reflist[i]=='5' and oplist[i]!='5'):
				FN+=1
			if(reflist[i]=='5' and oplist[i]=='5'):
				TP+=1
			i+=1	

		#print('TP=',TP,' FP=',FP,' FN=',FN)
		precision=TP/float(TP+FP)  
		recall=TP/float(TP+FN)
		fscore=(2*precision*recall)/(precision+recall)
		print("Values for Swedish data:")
		print('Precision =',precision,' Recall =',recall,' F-Score=',fscore)




if __name__=='__main__':
	performance()