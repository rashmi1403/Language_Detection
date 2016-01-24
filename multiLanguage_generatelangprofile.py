
#Create language profile as the training data with vocabulay and frequency to train the model
#python multiLanguage_generatelangprofile.py english.data english.model

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


LANGDATA_FOLDER = '.'

class NGramBasedTextCategorizer:


    #----------------------------------------------------------------------
    def __init__(self):
        
        self._languages_statistics = {}
        self._tokenizer = RegexpTokenizer("[a-zA-Z]+")
        self._langdata_path = LANGDATA_FOLDER
    
    #----------------------------------------------------------------------

    def _tokenize_text(self, raw_text):
        
        tokens = self._tokenizer.tokenize(raw_text)
        
        return tokens
    
    #----------------------------------------------------------------------
    def _generate_ngrams(self, tokens):
        
        generated_ngrams = []
        
        for token in tokens:            
            for x in xrange(1, 5): # generate N-grams, for N=1 to 5
                xngrams = ngrams(token, x,pad_left=True, pad_right=True, pad_symbol=' ')
                
                for xngram in xngrams:
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
        


if __name__=='__main__':
    
    infile=sys.argv[1]
    outfile=sys.argv[2]
    

    text_categorizer = NGramBasedTextCategorizer()

    text_categorizer.generate_ngram_frequency_profile_from_file(infile,outfile)