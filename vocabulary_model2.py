import sys
import os
import pdb
from itertools import chain
from collections import defaultdict, Counter

def read_traning_data(data_dir):

	english_lines = []
	french_lines = []			# list of list of lines in a file
	file_lines_list = []
	vocab_list = []					# list of all words in a file

	files = os.listdir(data_dir)

	# reading lines of a file into a list
	try:
		for f in files:
			with open(data_dir + f) as text:
				for line in text:
					
					line = [x.encode('utf-8') for x in line.strip(',.?/').split()]
					file_lines_list.append(line[1:])

					if line[0] == b'en':
						english_lines.append(line[1:])

					if line[0] == b'fr':
						french_lines.append(line[1:])

		vocab_list = list(chain.from_iterable(file_lines_list))
		vocabulary = set(vocab_list)
		vocabulary_dict = vocab_to_number(vocabulary)


		number_transformed_english_sentences = replace_text_with_number_vocab(vocabulary_dict, english_lines)
		tagged_data_to_file(number_transformed_english_sentences, 'en')
		number_transformed_french_sentences = replace_text_with_number_vocab(vocabulary_dict, french_lines)
		tagged_data_to_file(number_transformed_french_sentences, 'fr')


	except OSError:
		print('File Not Found')


def test_data_replace_vocab(data_dir):
	english_lines = []
	french_lines = []			# list of list of lines in a file
	file_lines_list = []
	vocab_list = []					# list of all words in a file
	vocabulary_dict = defaultdict(list)
	files = os.listdir(data_dir)

	# reading lines of a file into a list
	try:
		for f in files:
			with open(data_dir + f) as text:
				for line in text:
					
					line = [x.encode('utf-8') for x in line.strip().split()]
					file_lines_list.append(line[1:])

					if line[0] == b'en':
						english_lines.append(line[1:])

					if line[0] == b'fr':
						french_lines.append(line[1:])

		with open('vocab.all') as vocab_file:
			for x in vocab_file:
				words = x.strip().split()
				vocabulary_dict[words[0]] = words[1]


		number_transformed_english_sentences = test_replace_text_with_number_vocab(vocabulary_dict, english_lines)
		test_tagged_data_to_file(number_transformed_english_sentences, 'en')
		number_transformed_french_sentences = test_replace_text_with_number_vocab(vocabulary_dict, french_lines)
		test_tagged_data_to_file(number_transformed_french_sentences, 'fr')


	except OSError:
		print('File Not Found')

def replace_text_with_number_vocab(vocabulary_dict, text):

	number_transformed_sentences = []
	vocabulary_dict = vocabulary_dict
	for sub_list in text:
		numbered_list = [vocabulary_dict[word] for word in sub_list]
		number_transformed_sentences.append(Counter(numbered_list))

	return number_transformed_sentences

def test_replace_text_with_number_vocab(vocabulary_dict, text):

	number_transformed_sentences = []
	vocabulary_dict = vocabulary_dict
	for sub_list in text:
		numbered_list = [vocabulary_dict[word.decode()] for word in sub_list]
		number_transformed_sentences.append(Counter(numbered_list))

	return number_transformed_sentences

def tagged_data_to_file(number_transformed_sentences, language):
	
	with open('tagged_data.lang' , 'a') as write_file:
		for sentence in number_transformed_sentences:
			ids = [int(x) for x in sentence]
			sentence =  [(str(x)+':'+str(sentence[x])) for x in sorted(ids)]
			
			write_file.write(language + ' ' +' '.join(str(x) for x in sentence) + '\n')


def test_tagged_data_to_file(number_transformed_sentences, language):
	
	with open('test_tagged_data.lang' , 'a') as write_file:
		for sentence in number_transformed_sentences:
			
			ids = sentence.keys()
			sentence =  [(str(x)+':'+str(sentence[x])) for x in sorted(ids)]
			write_file.write(language + ' ' +' '.join(str(x) for x in sentence) + '\n')
		

def vocab_to_number(vocabulary):

	vocabulary_dict = defaultdict(list)
	vocabulary = list(vocabulary)
	for x in range(len((vocabulary))):
		vocabulary_dict[vocabulary[x]] = x + 1          #starting word -> number values from 1

	write_vocab_to_file(vocabulary_dict)

	return vocabulary_dict
				


def write_vocab_to_file(vocabulary_dict):
	"write words to a file for reference"

	with open("vocab.all" , 'w') as write_file:
		for x in vocabulary_dict.keys():
			write_file.write(x.decode() + " " + str(vocabulary_dict[x]) + "\n")




def main():
	args = sys.argv
	data_dir = args[1]
	category = args[2]
	print(data_dir)
	
	if category == 'train':
		read_traning_data(data_dir)
	elif category == 'test':
		test_data_replace_vocab(data_dir)

if __name__ == "__main__":
    main()
