import random
import math

def split_data(data):
	training_data = []
	length = len(data)
	d_75 = 75/100 * length
	d_75 = (math.floor(d_75))
	random.shuffle(data)
	training_data = data[:d_75]
	dev_data = data[d_75:]

	with open("training_75" , 'w') as outputfile:
		for data in training_data:
			outputfile.write(data + "\n")
	outputfile.close()

	with open("training_25" , 'w') as outputfile:
		for data in dev_data:
			outputfile.write(data + "\n")
	outputfile.close()


def main():
	inputf1 = open("training.english","r")
	inputf2 = open("training.french","r")
	input_data1 = inputf1.read().splitlines()			#list of input lines
	input_data2 = inputf2.read().splitlines()			#list of input lines
	inputf1.close()
	inputf2.close()
	len1 = len(input_data1)
	len2 = len(input_data2)
	if(len1 < len2):
		data = input_data1 + input_data2[:len1]
	else:
		data = input_data2 + input_data1[:len2]
	split_data(data)

if __name__ == "__main__":
    main()
