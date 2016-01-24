README

Instructions to process and run model2 (naive bayes only)

* Preprocessing data files 
     python3 process_language_files_model2.py <document_name> <language>
 eg: python3 process_language_files_model2.py small.fr fr

* Creating a vocabulary and test and train set
      python3 vocabulary_model2.py <processed_data_directory> <train or test>
  eg: python3 vocabulary_model2.py data/ train

* learning
 python3 nb_learn_model2.py tagged_data.lang model2.file

* classifying 
python3 nb_classify_model2.py model2.file test_data.lang


---------------------------------------------------------------------------------------
Instructions to process and run model1 (1-gram + naive bayes)

* Preprocessing data files and creating the vocabulary file
     python3 process_language_files_model1.py <english_document> <french_document>
 eg: python3 process_language_files_model1.py data.en data.fr

* Generating the training data set and testing data set by splitting the file generated from the previous program. 
     python3 split_trainingdata_model1.py

* Learning
     python3 nb_learn_model1.py training_75 model.75

*Classifying
     python3 nb_classify_model1.py model.75 training_25 >> output

*Evaluation
     python3 calculate_score_model1.py output training_25
     
---------------------------------------------------------------------------------------
Instructions to process and run multi-language classifier model 1 (n-gram + distance measure)

* Preprocessing data files and creating the training file
     python3 multiLanguage_create_trainfile.py <english_document> <french_document> <dutch_document> <german_document> <swedish_document> training.data
 eg: python3 multiLanguage_create_trainfile.py english.data french.data dutch.data german.data swedish.data training.data

* Geberating language profile for the training data : vocabulay and frequency of occurences
     python multiLanguage_generatelangprofile.py <training_file_language1> <model_file_language1>     
 eg. python multiLanguage_generatelangprofile.py english.data english.model

* Learning and classifiying using n-grams model
     python multiLanguage_nltk_ngrams.py test.data output.out

Instructions to process and run multi-language classifier model 2 (based on stopwords) 

* Learning and classifying based on stop-words
     python multiLanguage_stopwords.py test.data output.out

*Evaluation common for both models
     python3 multiLanguage_test_accuracy.py output.out test.data