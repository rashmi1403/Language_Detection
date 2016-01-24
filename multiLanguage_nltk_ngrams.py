
#Run the ngrams models on the test data using langauge model files to predict langiage detected for each line
#python multiLanguage_nltk_ngrams.py test.data output.out

####

import glob
import operator
import os
import sys
import argparse

try:
    import nltk.corpus
except ImportError:
    print '[!] You need to install nltk (http://nltk.org/index.html)'
    sys.exit(-1)

try:
    from nltk.tokenize import RegexpTokenizer
    from nltk.util import ngrams
except ImportError:
    print '[!] You need to install nltk (http://nltk.org/index.html)'
    sys.exit(-1)


LANGDATA_FOLDER = './data/'

class NGramBasedTextCategorizer:


    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        
        self._languages_statistics = {}
        self._tokenizer = RegexpTokenizer("[a-zA-Z]+")
        self._langdata_path = LANGDATA_FOLDER
    
    #----------------------------------------------------------------------
    def _load_ngram_statistics(self):

        
        languages_files = glob.glob('%s*.dat' %self._langdata_path)
        
        for language_file in languages_files:
            filename = os.path.basename(language_file)
            language = os.path.splitext(filename)[0]
            #print(language)
            ngram_statistics = open(language_file, mode='r').readlines()
            ngram_statistics = map(str.rstrip, ngram_statistics) # remove edge trailing
            
            self._languages_statistics.update({language:ngram_statistics})
    
    #----------------------------------------------------------------------
    def _tokenize_text(self, raw_text):
        
        tokens = self._tokenizer.tokenize(raw_text)
        
        return tokens
    
    #----------------------------------------------------------------------
    def _generate_ngrams(self, tokens):
        
        generated_ngrams = []
        
        for token in tokens:            
            for x in xrange(1, 5): # generate N-grams, for N=1 to 5
                xngrams = ngrams(token, x, pad_left=True, pad_right=True, pad_symbol=' ')
                
                for xngram in xngrams:
                    # convert ('E', 'X', 'T', ' ') to 'EXT '
                    ngram = ''.join(xngram)
                    generated_ngrams.append(ngram)
        
        return generated_ngrams
    
    #----------------------------------------------------------------------
    def _count_ngrams_and_hash_them(self, ngrams):
        
        ngrams_statistics = {}
        
        for ngram in ngrams:
            if not ngrams_statistics.has_key(ngram):
                ngrams_statistics.update({ngram:1})
            else:
                ngram_occurrences = ngrams_statistics[ngram]
                ngrams_statistics.update({ngram:ngram_occurrences+1})
        
        return ngrams_statistics
        
    #----------------------------------------------------------------------
    def _calculate_ngram_occurrences(self, text):
        
        tokens = self._tokenize_text(text)
        ngrams_list = self._generate_ngrams(tokens)
        
        ngrams_statistics = self._count_ngrams_and_hash_them(ngrams_list)

        ngrams_statistics_sorted = sorted(ngrams_statistics.iteritems(),\
                                          key=operator.itemgetter(1),\
                                          reverse=True)[0:300]
        
        return ngrams_statistics_sorted
    
    #----------------------------------------------------------------------
    def _compare_ngram_frequency_profiles(self, category_profile, document_profile):
        
        document_distance = 0
        
        # convert [['eas ', 487], ['going', 437], ...] to ['eas', 'going', ...]
        category_ngrams_sorted = [ngram[0] for ngram in category_profile]
        document_ngrams_sorted = [ngram[0] for ngram in document_profile]
        
        maximum_out_of_place_value = len(document_ngrams_sorted)
        
        for ngram in document_ngrams_sorted:
            # pick up index position of ngram
            document_index = document_ngrams_sorted.index(ngram)
            try:
                # check if analyzed ngram exists in pre-computed category
                category_profile_index = category_ngrams_sorted.index(ngram)
            except ValueError:
                category_profile_index = maximum_out_of_place_value

            distance = abs(category_profile_index-document_index) # absolute value
            document_distance+=distance
        
        return document_distance
    
    #----------------------------------------------------------------------
    def guess_language(self, raw_text):
        
        languages_ratios = {}
        self._load_ngram_statistics() # load pre-computed data
        
        '''
        Finally, the bubble labelled "Find Minimum`Distance" simply takes
        the distance measures from all of the category profiles to the
        document profile, and picks the smallest one.
        '''
        for language, ngrams_statistics in self._languages_statistics.iteritems():
            language_ngram_statistics = self._calculate_ngram_occurrences(raw_text)
            distance = self._compare_ngram_frequency_profiles(ngrams_statistics, language_ngram_statistics)
            
            languages_ratios.update({language:distance})
            #print("ratios=",languages_ratios)
        nearest_language = min(languages_ratios, key=languages_ratios.get)
        
        return nearest_language
    
    
    #----------------------------------------------------------------------
    def generate_ngram_frequency_profile_from_raw_text(self, raw_text, output_filename):
        
        output_filenamepath = os.path.join(self._langdata_path, output_filename)
        
        profile_ngrams_sorted = self._calculate_ngram_occurrences(raw_text)
        
        fd = open(output_filenamepath, mode='w')
        for ngram in profile_ngrams_sorted:
            fd.write('%s\t%s\n' % (ngram[0], ngram[1]))
        fd.close()
    
    #----------------------------------------------------------------------
    def generate_ngram_frequency_profile_from_file(self, file_path, output_filename):

        
        raw_text = open(file_path, mode='r').read()
        self.generate_ngram_frequency_profile_from_raw_text(raw_text, 
                                                           output_filename)
        profile_ngrams_sorted = self._calculate_ngram_occurrences(raw_text)
        

#----------------------------------------------------------------------
def guess_language(raw_text):
    
    return NGramBasedTextCategorizer().guess_language(raw_text)

if __name__=='__main__':
    
    f1=sys.argv[1]
    f2=sys.argv[2]
    #unknown_language_text = open(args.textfile, mode='r').read()
    with open(f1,'r') as f,open(f2,'w') as o:
        for line in f:
            text_categorizer = NGramBasedTextCategorizer()
            guessed_language = text_categorizer.guess_language(line)
            #print '[*] %s seems to be written in %s' %(line, guessed_language)
            if(guessed_language=='english'):
                o.write('1 '+guessed_language+'\n')
            elif(guessed_language=='french'):
                o.write('2 '+guessed_language+'\n')
            elif(guessed_language=='dutch'):
                o.write('3 '+guessed_language+'\n')
            elif(guessed_language=='german'):
                o.write('4 '+guessed_language+'\n')
            elif(guessed_language=='swedish'):
                o.write('5 '+guessed_language+'\n')
            else:
                o.write('0 '+guessed_language+'\n')