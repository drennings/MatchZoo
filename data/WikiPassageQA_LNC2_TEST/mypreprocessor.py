# coding: utf-8
"""
tokenize and filter data
Given train.tsv, dev.tsv, test.tsv
Output WikiPassageQA_LNC2_TEST-train-filtered.txt, WikiPassageQA_LNC2_TEST-dev-filtered.txt, WikiPassageQA_LNC2_TEST-test-filtered.txt
"""
from __future__ import print_function

import os
import sys
import json
import nltk
#nltk.download('punkt')
import re

# Returns a dict that contains all passages in document_passages file
def read_passages(path_to_passages):
    document_dict = {}
    
    with open(path_to_passages, 'r') as documents_json:
        document_dict = json.load(documents_json)
        
    return document_dict

def clean_special_chars(q_id, question_text):
    symbols_to_remove = ['?', "'", '"', '(', ')', ',', '.', ':', '>']
    for symbol in symbols_to_remove:
        question_text = question_text.replace(symbol, '')  
        
    question_text = question_text.replace('-',' ')
    question_text = question_text.replace('&',' and ')

    if "[" in question_text:
        if q_id == "3340": #remove contents
            question_text = re.sub(r'\[[^\(]*?\]', r'', question_text)
        else: #keep contents
            question_text = re.sub(r'\[(?:[^\]|]*\|)?([^\]|]*)\]', r'\1', question_text)
    if "/" in question_text:
        if q_id == "104" or q_id == "857":
            question_text = question_text.replace('/','')
        else:
            question_text = question_text.replace('/',' or ')
    
    return question_text

def preprocess_q_text(q_text):
    q_text = clean_special_chars(q_id, q_text) #needed for our indri run
    q_text = ' '.join(nltk.word_tokenize(q_text))
    q_text = q_text.strip()
    #print("q_text == ' '.join(nltk.word_tokenize(q_text))")
    #print(q_text == ' '.join(nltk.word_tokenize(q_text)))
    return q_text

def remove_tabs(text):
    return text.replace('\t', ' ')

def preprocess_passage(passage):
    passage = remove_tabs(passage)
    passage = ' '.join(nltk.word_tokenize(passage))
    passage = passage.strip()
    #print("passage == ' '.join(nltk.word_tokenize(passage))")
    #print(passage == ' '.join(nltk.word_tokenize(passage)))
    #if(passage != ' '.join(nltk.word_tokenize(passage))):
    #    print(passage)
    #    print()
    #    print(' '.join(nltk.word_tokenize(passage)))
    return passage

if __name__ == '__main__':

    basedir = './WikiPassageQA_LNC2_TEST/'
    in_corpfile = [basedir + 'train.tsv', basedir + 'dev.tsv', basedir + 'test.tsv']
    doc_file = basedir + 'document_passages.json'
    outfile = [basedir + 'WikiPassageQA_LNC2_TEST-train-filtered.txt', basedir + 'WikiPassageQA_LNC2_TEST-dev-filtered.txt', basedir + 'WikiPassageQA_LNC2_TEST-test-filtered.txt']
    
    q_ids_that_contain_no_question = ["4149", "4148", "1315"]
    q_ids_that_are_contained_in_the_train_and_dev_set = ["3566"] # remove it from the train set
    q_ids_that_contain_the_same_question_but_different_answers = ["3731", "3732"]
    q_ids_that_are_on_a_doc_which_has_a_duplicate_passage = ["2230", "2231", "2232", "2233", "2234"] #see description for doc 769
    q_ids_that_should_be_skipped = q_ids_that_contain_no_question + q_ids_that_are_contained_in_the_train_and_dev_set + q_ids_that_contain_the_same_question_but_different_answers + q_ids_that_are_on_a_doc_which_has_a_duplicate_passage
    
    doc_ids_that_have_no_question = ["188"] #The current matchzoo style for processing WikiQA which we follow, does not add the document to the corpus if there is no q about it
    doc_ids_that_have_a_duplicate_passage_with_another_doc = ["769"] #We remove 769 since 769-14 == 243-10, 769 has less questions than 243, hence we remove this doc and its questions
    doc_ids_that_should_be_skipped = doc_ids_that_have_no_question + doc_ids_that_have_a_duplicate_passage_with_another_doc #although this variable is never used, we leave it here for documentation
    
    document_dict = read_passages(doc_file)
    
    for i in range(len(in_corpfile)):
        fout = open(outfile[i], 'w')
        firstline = True
        for line in open(in_corpfile[i], 'r'):
            if firstline == True: #skip the header
                firstline = False
                continue

            q_id, q_text, doc_id, doc_name, a_ids = line.split('\t')
            
            if q_id in q_ids_that_should_be_skipped:
                continue
            q_text = preprocess_q_text(q_text)
            
            document = document_dict[doc_id]
            for p_id, passage in document.iteritems():
                passage = preprocess_passage(passage)
                if p_id in a_ids:
                    print(q_text + "\t" + passage + "\t" + "1", file=fout)
                else:
                    print(q_text + "\t" + passage + "\t" + "0", file=fout)
        
        fout.close()
