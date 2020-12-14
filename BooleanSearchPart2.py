#!/usr/bin/env python
import os
import pickle

# The file object created using pickle from part1 has the inverted index object dumped into it. 
# This pickle file is opened in read mode and load method is called which loads the inverted index object present within the file object
pickle_inverted = open("inverted_index.pickle","rb")
pickle_inverted_index = pickle.load(pickle_inverted)

# The Query terms are processed in the same way as document terms to convert them to lowercase and remove numbers, special characters, stopwords,etc
def process_Query(query):
    q_word_list = []
    qword_list_spl = []
    current_qword = []
    # Each character in Query term is checked and eliminated if it is a special character or a number. Once a whitespace is encountered it appends all the characters till that space into a word
    for each_char in query:
        if each_char.isalpha():
            current_qword.append(each_char)
        elif current_qword:
            qword = u''.join(current_qword)
            qword_list_spl.append(qword)
            current_qword = []
    # Moving all the words to a list - qword_list_spl, post removal of numbers, special characters        
    if current_qword:
        qword = u''.join(current_qword)
        qword_list_spl.append(qword)
        
    qword_list_pos = []
    noStop_lowerCase_qwords = []
    pos = 0  
    
    #Next looping through qword_list_spl list and converting words to lowercase and Check if there is word which is a Stop_word and exclude them from being appended to another list 
    for word in qword_list_spl:
        # WOrds other than "AND","OR" from Query list are converted to lowercase since we want to use "AND","OR" as Boolean operators   
        if word not in ('AND', 'OR'):
            word = word.lower()
            if word in ('but', 'is', 'the', 'to'):
                continue
        noStop_lowerCase_qwords.append(word)
        
    return noStop_lowerCase_qwords

Query = input("Enter Query as a Single String without paranthesis, operators as CAPS and within double quotes if running in linux : ")
Q_list = process_Query(Query)

resulted_docs = []
doc_IDs = []
prev_word_docIDs = []
curr_word_docIDs = []
current_operator = ""
curr_search_result = []

# Handling the cases when the user enters 0, 1 or more Query terms
if(len(Q_list)==0):
    print("\n Query List is Empty post query processing of your query: ",Query,". Please enter a valid query")
elif(len(Q_list)==1):
    for single_q in Q_list:
        if(single_q in pickle_inverted_index):
            for each_doc_res in pickle_inverted_index[single_q]:
                doc_IDs.append(each_doc_res)
            print("\n'",single_q,"' occurs in document(s): ",doc_IDs)
            print("Detailed positions in respective documents for '",single_q,"': ",pickle_inverted_index[single_q].items(),"\n")
        else:
            print ("\nNO RESULTS FOUND for the Simple Query Search!!")
else:
    # For every element in the query list, check if it's a query token or an operator
    for each_q in Q_list:
        if(each_q in ('AND', 'OR')):
            current_operator = each_q
        else:
            # Check if the query token is present in inverted index. prev_word_docIDs stores the list of DocIDs of left word and curr_word_docIDs stores the list of DOCIds of current_word(right word after operator) 
            if(each_q in pickle_inverted_index):
                if prev_word_docIDs == []:
                    for each_doc_res in pickle_inverted_index[each_q]:
                        prev_word_docIDs.append(each_doc_res)
                    print("\n'",each_q,"' occurs in document(s): ",prev_word_docIDs)
                    print("Detailed positions in respective documents for '",each_q,"': ",pickle_inverted_index[each_q].items(),"\n")
                else:
                    # Controls transfers here when prev_word_docIDs is not empty, indicating there exists some previous word and an operator before this current_word. SO get the list of docIDs of current_word
                    for each_doc_res2 in pickle_inverted_index[each_q]:
                        curr_word_docIDs.append(each_doc_res2)
                    print("\n'",each_q,"' occurs in document(s): ",curr_word_docIDs)
                    print("Detailed positions in respective documents for '",each_q,"': ",pickle_inverted_index[each_q].items(),"\n")
                    
                    # After getting list of DOC IS for right operand, check the operator - AND/OR and perform the boolean operation on the Doc lists from left word and right word  
                    if current_operator == 'AND':
                        curr_search_result = set(prev_word_docIDs) & set(curr_word_docIDs)
                        prev_word_docIDs = []
                        curr_word_docIDs = []
                    else:
                        curr_search_result = set(prev_word_docIDs) | set(curr_word_docIDs)
                        prev_word_docIDs = []
                        curr_word_docIDs = []
                    prev_word_docIDs = curr_search_result
            else:
                #control transfers here when the query term is not present in the inverted index. Hence, assign empty list to current_word_docIDs 
                curr_word_docIDs = []
                print("\n'",each_q,"' is not present in the inverted index\n")
                #IF there exists a previous word which is present in index then perform boolean operation (AND/OR) between previous_word_docIDs and current_word_docIDs which is will be empty in this block
                if prev_word_docIDs != []:
                    if current_operator == 'AND':
                        curr_search_result = set(prev_word_docIDs) & set(curr_word_docIDs)
                        prev_word_docIDs = []
                        curr_word_docIDs = []
                    else:
                        curr_search_result = set(prev_word_docIDs) | set(curr_word_docIDs)
                        prev_word_docIDs = []
                        curr_word_docIDs = []
                    prev_word_docIDs = curr_search_result
    
    if(len(prev_word_docIDs) == 0):
        print ("\nNO RESULTS FOUND for this combination of Boolean Query Search!!")
    else:
        print("\nFinal Boolean Query Search result is : ", prev_word_docIDs)

