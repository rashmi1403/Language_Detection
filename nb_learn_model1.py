from sys import argv
import pickle 

script, inputf1, outputf1 = argv

file1 = open(inputf1, "r")	#training file
file2 = open(outputf1, "w") #model file

#read input data into the list - training_data
line = file1.readline()
training_data = []

while line:
	training_data.append(line)
	line = file1.readline()

#split training data into positive and negative list
positive_l = []
negative_l = []

"""print(training_data[0])
print(training_data[1])
print(training_data[2])
print(training_data[3])"""

for data in training_data:
	item = data.split(" ")
	if(item[0] == "english"):
		positive_l.append(data)
	else:
		negative_l.append(data)

#assigning general labels
l_data = positive_l[0].split(" ")
if(l_data[0] == "english"):
	classification = "english_french"

"""print(positive_l[0])
print(positive_l[1])
print(negative_l[0])
print(negative_l[1])"""

#list for all words --> Vocab of training data 
vocab_l = []

#make a dictionary of unique words which are in positive_l
positive_d = {}

for data in positive_l:
	item = data.split(" ")
	for i in range(1,len(item)):
		token = item[i].split(":")
		vocab_l.append(token[0])
		key = int(token[0])
		val = positive_d.get(key)
		if(val != None):
			val = int(val) + int(token[1])
			positive_d[key] = val
		else:
			positive_d[key] = int(token[1])

#make a dictionary of negative words in negative_l
negative_d = {}

for data in negative_l:
	item = data.split(" ")
	for i in range(1,len(item)):
		token = item[i].split(":")
		vocab_l.append(token[0])
		key = int(token[0])
		val = negative_d.get(key)
		if(val != None):
			val = int(val) + int(token[1])
			negative_d[key] = val
		else:
			negative_d[key] = int(token[1])

#Number of positive and negative examples and total
no_of_positive = len(positive_l)
no_of_negative = len(negative_l)
total_reviews = no_of_positive + no_of_negative

#convert vocab list to set so that we have only the unique tokens
vocab_unique = set(vocab_l)
#print(positive_l)
#print(negative_l)

print("Positive ex no = " +str(no_of_positive))
print("Negative ex no = " +str(no_of_negative))
print("total ex no = " +str(total_reviews))

no_of_vocab = len(vocab_unique)
P_positive = no_of_positive/ total_reviews
P_negative = no_of_negative/ total_reviews

print("Prob of positive = " +str(P_positive))
print("Prob of negative = " +str(P_negative))
print("V = " +str(no_of_vocab))

#print(positive_d)
#print(negative_d)
#Total no of words in positive
no_words_positive = 0
for key in positive_d:
	#print("Value = " +str(positive_d[value]))
	no_words_positive += int(positive_d[key])

print("No Words in positive = " +str(no_words_positive))

#Total no of words in negative
no_words_negative = 0
for key in negative_d:
	no_words_negative += int(negative_d[key])

print("No Words in negative = " +str(no_words_negative))

#Find P(word/ positive) and P(word/ negative) using "add-one smoothing"
P_word_positive = {}
P_word_negative = {}

for key in positive_d:
	#if(key == 1):
	#	print(str(positive_d[key]))
	res = (positive_d[key] + 1)/ (no_words_positive + no_of_vocab)
	P_word_positive[key] = res
	#if(key == 1):
	#	print(str(res))

for key in negative_d:
	res = (negative_d[key] + 1)/ (no_words_negative + no_of_vocab)
	P_word_negative[key] = res

for key in negative_d:
	val = positive_d.get(key)
	if(val == None):
		res = (1)/(no_words_positive + no_of_vocab)
		P_word_positive[key] = res

for key in positive_d:
	val = negative_d.get(key)
	if( val == None):
		res = (1)/ (no_words_negative + no_of_vocab)
		P_word_negative[key] = res


#print(P_word_positive)

#print(P_word_negative)

#Add the probabilities to the model file
final_res = [classification, P_positive, P_negative, no_of_vocab, P_word_positive, P_word_negative]
file2.write(str(final_res))

file1.close()
file2.close()

print("Finished processing!")











