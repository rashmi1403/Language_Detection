import sys
import random
import pdb
from copy import deepcopy

from collections import defaultdict

""" Usage: python3 nblearn.py training_file model_file """

def parse_data(training_file, split_percentage = 75):
	list_sentences = []
	all_sentences = []
	
	# create list of list for each review
	with open(training_file) as training_data:
	
		for line in training_data:
			list_sentences.append(line.strip().split())

	#create tuples out of all values
	for rev in list_sentences:
		all_sentences.append([tuple(x.split(':')) for x in rev])
	
	#shuffle data
	random.shuffle(all_sentences)

	#split data into test and train set based on %
	language = ['language', 'en', 'fr']

	split_value = int((split_percentage * len(all_sentences)) / 100)
	train_sentences = all_sentences[:split_value]
	test_sentences = all_sentences[split_value:]

	return train_sentences, test_sentences, language
	
def posterior_class_probability(train_sentences, language):

	count = 0
	english_count = 0
	french_count = 0
	english_sentences = []
	french_sentences = []

	#count number of positive and negative reviews
	for rev in train_sentences:
		count += 1
		if (rev[0][0]) == language[1]:
			english_count += 1
			english_sentences.append(rev)
		elif (rev[0][0]) == language[2]:
			french_count += 1
			french_sentences.append(rev)

	# calculate probability of class positive and negative
	prob_english = english_count / count
	prob_french = french_count / count

	print("english count = ", prob_english)
	print("french count = ", prob_french)		
	print("count = ", count)
	return english_sentences, prob_english, french_sentences, prob_french

def conditional_probabilities(english_sentences, french_sentences):

	english_sentences_vocab_count = []
	english_sentences_dict = defaultdict(list)
	french_sentences_dict = defaultdict(list)
	english_sentence_wordcount = defaultdict(list)
	french_sentence_wordcount = defaultdict(list)

	# combine all reviews for word probability
	positive_reviews_vocab_list = [rev for reviews in english_sentences for rev in reviews[1:]]
	negative_reviews_vocab_list = [rev for reviews in french_sentences for rev in reviews[1:]]
	
	# combine all counts for a word into a list
	for identifier, count in positive_reviews_vocab_list:
		english_sentences_dict[int(identifier)].append(int(count))

	for identifier, count in negative_reviews_vocab_list:
		french_sentences_dict[int(identifier)].append(int(count))

	for key in english_sentences_dict.keys():
		english_sentence_wordcount[key] = sum(english_sentences_dict[key])

	for key in french_sentences_dict.keys():
		french_sentence_wordcount[key] = sum(french_sentences_dict[key])
				
	# calculate vocabulary length
	unique_vocab = set(english_sentences_dict.keys()) | set(french_sentences_dict.keys())
	vocab_size = len(unique_vocab)

	return unique_vocab, vocab_size, english_sentence_wordcount, french_sentence_wordcount

def word_probabilities(unique_vocab, vocab_size, english_sentence_wordcount, french_sentence_wordcount):

	total_english_count = 0
	total_french_count = 0
	model_list = []
	
	unique_vocab = list(unique_vocab)
	#calculating total number of positive words and total negative words
	for key in english_sentence_wordcount.keys():
		total_english_count += english_sentence_wordcount[key]

	for key in french_sentence_wordcount.keys():
		total_french_count += french_sentence_wordcount[key]

	# calculating postive and negative probabilities for each word
	for word in unique_vocab:
		if english_sentence_wordcount[word]:
			english_probability = (english_sentence_wordcount[word] + 1) / (total_english_count + vocab_size)		
		else:
			english_probability = (0 + 1) / (total_english_count + vocab_size)		
		
		if french_sentence_wordcount[word]:
			french_probability = (french_sentence_wordcount[word] + 1) / (total_french_count + vocab_size)
		else:
			french_probability = (0 + 1) / (total_french_count + vocab_size)
		
		model_list.append(tuple([str(word), str(english_probability), str(french_probability)]))

	return model_list

def write_model(model_list, prob_english, prob_french, model_file):

		with open(model_file, 'w') as model_file:
			model_file.write( str(prob_english) + "\n")
			model_file.write( str(prob_french) + "\n")
			for prob in model_list:
				line = " ".join(prob)
				model_file.write("%s\n" %line)

def write_data_files(train_sentences, test_sentences, language):

	test_reviews1 = deepcopy(test_sentences)
	train_reviews1 = deepcopy(train_sentences)
	train_reviews2 = deepcopy(train_sentences)

	#
	with open("test_data.lang", 'w') as f:
		for x in test_reviews1:
			for t in range(1, len(x)):
				x[t] = str(x[t][0]) + ':' + str(x[t][1])
			x[0] = x[0][0]
			str1 = " ".join(x)
			f.write("%s\n" % str1)


	# # remove later if not required
	with open(language[0] +'_train.svm.feat', 'w') as f:
		for rev in train_reviews1:
			if rev[0][0] == language[1]:
		 		rev[0] = '1'
			elif rev[0][0] == language[2]:
				rev[0] = '-1'
			for t in range(1, len(rev)):
				rev[t] = str(rev[t][0]) + ':' + str(rev[t][1])
			str1 = " ".join(rev)
			f.write("%s\n" % str1)

	with open(language[0] +'_train.megam.feat', 'w') as f3:
		for rev in train_reviews2:
			if rev[0][0] == language[1]:
		 		rev[0] = '1'
			elif rev[0][0] == language[2]:
				rev[0] = '0'
			for t in range(1, len(rev)):
				rev[t] = str(rev[t][0]) + ' ' + str(rev[t][1])
			str1 = " ".join(rev)
			f3.write("%s\n" % str1)	


def main():
	
	args = sys.argv
	training_file = args[1]
	model_file = args[2]
	train_sentences, test_sentences, language = parse_data(training_file, 75)
	write_data_files(train_sentences, test_sentences, language)
	english_sentences, prob_english, french_sentences, prob_french = posterior_class_probability(train_sentences, language)
	unique_vocab,vocab_size, english_sentence_wordcount, french_sentence_wordcount = conditional_probabilities(english_sentences, french_sentences)
	model = word_probabilities(unique_vocab ,vocab_size, english_sentence_wordcount, french_sentence_wordcount)
	write_model(model, prob_english, prob_french, model_file)

if __name__ == "__main__":
    main()
