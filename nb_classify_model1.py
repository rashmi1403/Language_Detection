from sys import argv
import ast
from math import log

script, inputf1, inputf2 = argv

file1 = open(inputf1, "r")	#model file
file2 = open(inputf2, "r")	#test file
#file3 = open(outputf1, "w") #results

#Extract all information from Model file
lines = file1.readlines()

list_f = []

for line in lines:
	list_f.append(ast.literal_eval(line))
	
file_list = list_f[0]

#print(str(file_list))

classification = file_list[0]
P_positive = float(file_list[1])
P_negative = float(file_list[2])
no_of_vocab = float(file_list[3])
P_word_positive = file_list[4]
P_word_negative = file_list[5]

#print("Prob = " +str(P_word_positive[9]))
#print("Prob = " +str(P_word_negative[9]))

#print("classification = " +classification)
#print("P_positive = " +str(P_positive))
#print("P_negative = " +str(P_negative))
#print("no_of_vocab = " +str(no_of_vocab))

#Extract all the test documents into a list
test_data = []

line = file2.readline()
while line:
	test_data.append(line.strip("english ").strip("french ").strip("\n"))
	line = file2.readline()
	

#Check the class of the docs
tokens = []
for data in test_data:
	tokens = data.split(" ")
	P_positive_doc = log(float(P_positive))
	P_negative_doc = log(float(P_negative))
	for token in tokens:
		feature = token.split(":")
		key = int(feature[0])
		powf = int(feature[1])
		#P(positive/ doc)
		valp = P_word_positive.get(key)
		#print(valp)
		if(valp != None):
			P_positive_doc += (powf*log(float(valp)))
		#else:
			#print(feature[0])
			#P_positive_doc += (powf*log(1/no_of_vocab))
		#P(negative/ doc)
		valn = P_word_negative.get(key)
		#print(valn)
		if(valn != None):
			P_negative_doc += (powf*log(float(valn)))
		#else:
			#print(feature[0])
			#P_negative_doc += (powf*log(1/no_of_vocab))
	#Decide the class	
	#P_positive_doc = 10 ** P_positive_doc
	#P_negative_doc = 10 ** P_negative_doc
	#print(P_positive_doc)
	#print(P_negative_doc)
	if(P_positive_doc > P_negative_doc):
		p_class = 1
	else:
		p_class = 0

	if(classification == "english_french"):
		if(p_class == 1):
			#file3.write("POSITIVE" +"\n")
			print("english")
		else:
			#file3.write("NEGATIVE" +"\n")
			print("french")
	
	if(classification == "spam_ham"):
		if(p_class == 1):
			#file3.write("SPAM" +"\n")
			print("SPAM")
		else:
			#file3.write("HAM" +"\n")
			print("HAM")

file1.close()
file2.close()
#file3.close()
#print("finished processing!")


		




