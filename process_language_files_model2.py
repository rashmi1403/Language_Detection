import sys
import pdb

def read_traning_data(language_file, language):

	file_lines_list = []			# list of list of lines in a file
	vocab_list = []					# list of all words in a file

	# reading lines of a file into a list
	try:
		with open(language_file) as text:
			for line in text:
				encoded_list = [x for x in line.strip(',.?/').split()]
				encoded_list = [language] + encoded_list
				file_lines_list.append(encoded_list)


	except OSError:
		print('File Not Found')

	return file_lines_list

def write_to_file(file_content, language):

	with open("data/data."+language, 'w') as write_file:
		for line in file_content:
			write_file.write(' '.join(str(x) for x in line) + '\n')

def main():
	args = sys.argv
	language_file = args[1]
	language = args[2]
	file_content = read_traning_data(language_file, language)
	write_to_file(file_content, language)

if __name__ == "__main__":
	main()