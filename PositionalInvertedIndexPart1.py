#!/usr/bin/env python
import os
import pickle

# This function gets the entire content of the document as input which further splits them into words and creates a dictionary of words and its positions in the document. This creates for a particular document that is being processed 
def split_into_words(text):
    word_list = []
    word_list_spl = []
    current_word = []
    # splitting text into words. Each character is checked and eliminated if it is a special character or a number. Once a whitespace is encountered it appends all the characters verified till that space into a word
    for each_char in text:
        if each_char.isalpha():
            current_word.append(each_char)
        elif current_word:
            word = u''.join(current_word)
            word_list_spl.append(word)
            current_word = []
    # Moving all the words to a list post removal of numbers, special characters        
    if current_word:
        word = u''.join(current_word)
        word_list_spl.append(word)
        
    word_list_pos = []
    noStop_lowerCase_words = []
    pos = 0  
    
    # Looping through every word in word_list_spl and getting the word positions using enumerate and finally appending them to word_list_pos 
    for pos, each_word in enumerate(word_list_spl,1):
        word_list_pos.append((each_word,pos))

    #Next looping through word_list_pos list and converting words to lowercase and Check if there is any word which is a Stop_word and exclude them from being appended to another list 
    for word,pos in word_list_pos:
        if word.lower() in ('and', 'but', 'is', 'the', 'to'):
            continue
        noStop_lowerCase_words.append((word.lower(),pos))
        
        
    inverted = {}
    # Looping through every word in noStop_lowerCase_words and Creating the Inverted dictionary with words as key and a list of positions as value using setdefault
    for word, pos in noStop_lowerCase_words:
        locations = inverted.setdefault(word, [])
        locations.append(pos)
    return inverted

# Defining function to create inverted index to include document ID for multi doc inverted index Example : {word :{'doc1': [pos1,pos2], 'doc2' : [pos1]})
def inverted_index_doc(inverted, doc_id, doc_ind):
    for word, locations in doc_ind.items():
        index = inverted.setdefault(word, {})
        index[doc_id] = locations
    return inverted

# Creating empty dictionary to store inverted index.
inverted = {}
documents_list = []
# Get the directory path from the user where all the input files are present
dirpath = input("Enter the directory path of the corpus where all the documents are present: ")
files = os.listdir(dirpath)
# Looping through every file present in the folder and storing its information in a list
for each_doc in files:
    doc_name = each_doc
    documents_list.append((each_doc, open(os.path.join(dirpath,each_doc))))
    
# Initializing a dictionary called documents
documents = {}
# Looping through every document present in documents_list and reading the content of each document and storing them in the dictionary 'document' with key being doc_id and value as the content of the doc
for doc_id, doc_file in documents_list:
    content = doc_file.read()
    documents[doc_id]=content
    
#Extract the content of every document into words and process words as per requirements by calling split_into_words() which later creates positional index for words present within a particular document. Now consider all other documents to create Inverted_Index for the entire corpus which will be of the form {word : {Doc1 : [pos1,pos2], Doc2 : [pos]}, word2 :...}
for doc_id, text in documents.items():
    doc_ind = split_into_words(text)
    inverted_index_doc(inverted, doc_id, doc_ind)

# Print the Inverted Index
for word, doc_locations in inverted.items():
    print(word, doc_locations)

#creating a file object using pickle and dumping the inverted index dictionary object into that file object. The file object is placed in the path same as the program file location
pickle_out = open("inverted_index.pickle","wb")
pickle.dump(inverted, pickle_out)
pickle_out.close()

