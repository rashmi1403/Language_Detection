from sys import argv

def get_list_of_data(input_data):
	data = []					#list of data [i.e., words] to be written in training file along with the lang tag

	for line in input_data:
		for word in line.split():
			data.append(word.lower())

	return data

def get_unique_vocab_list(data1, data2):
	#open the vocab file
	
	vocab_list = [] 		#list of characters in the data

	for samp in data1:
		for ch in samp:
			vocab_list.append(ch.lower())

	for samp in data2:
		for ch in samp:
			vocab_list.append(ch)

	unique_vocab = set(vocab_list)	#list of unique characters in the data
	vocabulary = list(unique_vocab)
	vocab_dict = {}

	for v in range(len(vocabulary)):
		vocab_dict[vocabulary[v]] = v+1

	print(vocab_dict)

	return vocab_dict

def generate_training_data(data, vocab_dict, lang):

	with open("training." + lang, 'w') as outputfile:
		for samp in data:
			output_d = {}
			for ch in samp:
				key = int(vocab_dict.get(ch))
				val = output_d.get(key)
				if(val != None):
					output_d[key] = int(val) + 1
				else:
					output_d[key] = 1
			#join the dictionary k1:v1 k2:v2 k3:v3
			output_res = []
			for key in sorted(output_d):
				ostr = str(key) +":" + str(output_d[key])
				output_res.append(ostr)
			res = lang + " " + " ".join(output_res)
			outputfile.write(res + "\n")
	outputfile.close()    




def main():
	file1 = argv[1]			#english file
	file2  = argv[2]		#french file
	inputf1 = open(file1,"r")
	inputf2 = open(file2,"r")
	#input_data = inputf.read().strip(',.?/').splitlines()   --> Strip makes no difference
	input_data1 = inputf1.read().splitlines()			#list of input lines
	input_data2 = inputf2.read().splitlines()			#list of input lines
	inputf1.close()
	inputf2.close()
	data1 = get_list_of_data(input_data1)
	data2 = get_list_of_data(input_data2)
	vocab_dict = get_unique_vocab_list(data1, data2)
	generate_training_data(data1, vocab_dict, "english")
	generate_training_data(data2, vocab_dict, "french")

if __name__ == "__main__":
    main()