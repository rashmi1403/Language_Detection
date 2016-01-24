#use stopwords to improve rate of prediciton of language
#python multiLanguage_stopwords.py train.data output.out

#!/usr/bin/env python
import sys
from nltk import wordpunct_tokenize
from nltk.corpus import stopwords


def calculate_languages_ratios(text):
	languages_ratios = {}
	tokens = wordpunct_tokenize(text)
	words = [word.lower() for word in tokens]
	for language in stopwords.fileids():
		stopwords_set = set(stopwords.words(language))
		words_set = set(words)
		common_elements = words_set.intersection(stopwords_set)
		languages_ratios[language] = len(common_elements) # language "score"
	return languages_ratios

def detect_language(text):
	ratios=calculate_languages_ratios(text)
	most_rated_language = max(ratios, key=ratios.get)
	return most_rated_language

if __name__=='__main__':
	#text='On y cite Mme Reding.'
	traindata=sys.argv[1]
	result=sys.argv[2]
	with open(traindata,'r') as train, open(result,'w') as res:
		for line in train.readlines():
			language=detect_language(str(line))
			if(language=='english'):
				res.write('1 '+language+'\n')
			elif(language=='french'):
				res.write('2 '+language+'\n')
			elif(language=='dutch'):
				res.write('3 '+language+'\n')
			elif(language=='german'):
				res.write('4 '+language+'\n')
			elif(language=='swedish'):
				res.write('5 '+language+'\n')
			else:
				res.write('0 '+language+'\n')
			print(language)