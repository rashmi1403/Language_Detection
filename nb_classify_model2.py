import sys
import math
from collections import defaultdict

""" Usage: python3 nbclassify.py model_file testing_file"""

def parse_data(testing_file, model_file):
	data = []
	data_list = []
	test_reviews = []
	labels = []
	model = defaultdict(list)

	with open(testing_file) as test_data:

		for line in test_data:
			data_list.append(line.strip().split())

		for rev in data_list:
			test_reviews.append([tuple(x.split(':')) for x in rev])
		
		for rev in test_reviews:
			labels.append(rev.pop(0)[0])
			

	with open(model_file) as model_data:
		data = model_data.readlines()
		class_english_probability = float(data[0].strip())
		class_french_probability = float(data[1].strip())
		
		data = data [2:]
		for line in data:
			words = line.split()
			model[int(words[0])] = [float(words[1]), float(words[2])]

	return test_reviews, model, class_english_probability, class_french_probability, labels


def classify(test_reviews, model, class_english_probability, class_french_probability, category):

	word_probability = []
	output = []

	for review in test_reviews:
		english_probability = 0
		french_probability = 0

		sentence_dict_temp = dict(review)
		sentence_dict = defaultdict()
		
		#sentence_dict = [dict([int(key), int(value)]) for key, value in sentence_dict.items()]
		for key, value in sentence_dict_temp.items():
			sentence_dict[int(key)] = int(value)

		english_list = []
		french_list = []

		for key in sentence_dict.keys():

			if key in model.keys():

				english_list.append(math.log(math.pow(model[key][0], sentence_dict[key]) if math.pow(model[key][0], sentence_dict[key]) > 0 else math.pow(model[key][0], 40)))
				french_list.append(math.log(math.pow(model[key][1], sentence_dict[key]) if math.pow(model[key][1], sentence_dict[key]) > 0  else math.pow(model[key][1], 40)))

			else:
				english_list.append(1)
				french_list.append(1)
		
		mul_english_prob = 1
		mul_french_prob = 1

		for prob in english_list:
			mul_english_prob += (prob)

		for prob in french_list:
			mul_french_prob += (prob)
		#pdb.set_trace()
		word_english_probability = math.log(class_english_probability) + mul_english_prob
		word_french_probability = math.log(class_french_probability) + mul_french_prob

		word_probability.append([word_english_probability,word_french_probability])
		for t in range(0, len(review)):
	 		review[t] = str(review[t][0]) + ':' + str(review[t][1])
		str1 = " ".join(review)

		if word_english_probability > word_french_probability:
			if category[0] == 'language':
				sys.stdout.write(category[1] + '\n')
				output.append(category[1])
			else:
				sys.stdout.write(category[1] + '\n')
				output.append(category[1])
		else:
			if category[0] == 'language':
				sys.stdout.write(category[2] + '\n')
				output.append(category[2])
			else:
				output.append(category[2])
				sys.stdout.write(category[2] + '\n')
	
	return output

def precision_values(output, labels, category):

	correct_english = 0
	correct_french = 0
	count_english = 0
	count_french = 0
	actual_english = 0
	actual_french = 0

	
	for label in output:
		if label == category[1]:
			count_english +=1
		if label == category[2]:
			count_french += 1

	for label in labels:
		if label == category[1]:
			actual_english +=1
		if label == category[2]:
			actual_french += 1

	
	for i in range(0, len(output)):
		if (labels[i] == category[1]) and (output[i] == category[1]):
			correct_english += 1
		elif (labels[i] ==category[2]) and (output[i] == category[2]):
			correct_french += 1

	precision_positive = correct_english/count_english
	precision_negative = correct_french/count_french
	recall_positive = correct_english/ actual_english
	recall_negative = correct_french/actual_french
	f_positive = (2 * precision_positive * recall_positive) / (precision_positive + precision_negative)
	f_negative = (2 * precision_negative * recall_negative) / (precision_negative + precision_positive)

	print("precision english == ", precision_positive)
	print("precision french ==", precision_negative)
	print("recall english ==", recall_positive) 
	print("recall french == ", recall_negative)
	print("f english ==", f_positive)
	print("f french ==", f_negative)

def write_to_file(output, category):

	output_file = category[0] + ".nb.out"

	with open(output_file, 'w') as out_file:

		for word in output:
			out_file.write("%s\n" %word)

	 

def main():
	
	args = sys.argv
	model_file = args[1]
	testing_file = args[2]

	category = ['language', 'en', 'fr']

	test_reviews, model, class_english_probability, class_french_probability, labels = parse_data(testing_file, model_file)
	output = classify(test_reviews, model, class_english_probability, class_french_probability, category)
	write_to_file(output, category)
	precision_values(output, labels, category)

if __name__ == "__main__":
    main()
