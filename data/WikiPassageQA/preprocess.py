# coding: utf-8
"""
tokenize data
Given train.tsv, dev.tsv, test.tsv
Output train-filtered.txt, dev-filtered.txt, test-filtered.txt
"""
from __future__ import print_function

import os
import sys
import json
import nltk
import re

def remove_special_chars(q_id, question_text):
    question_text = question_text.replace('?','') #remove ?
    question_text = question_text.replace("'",'')
    question_text = question_text.replace('"','')
    question_text = question_text.replace('-',' ')
    question_text = question_text.replace('(','')
    question_text = question_text.replace(')','')
    question_text = question_text.replace(',','')
    question_text = question_text.replace('.','')
    question_text = question_text.replace('&',' and ')
    question_text = question_text.replace(':','')
    question_text = question_text.replace('>','')#error in dataset

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

def remove_tabs(text):
    return text.replace('\t', ' ')

# Returns a dict that contains all passages in document_passages file
def read_passages(path_to_passages):
    document_dict = {}
    
    with open(path_to_passages, 'r') as documents_json:
        document_dict = json.load(documents_json)
        
    return document_dict
    
    
if __name__ == '__main__':

    basedir = './WikiPassageQA/'
    in_corpfile = [basedir + 'train.tsv', basedir + 'dev.tsv', basedir + 'test.tsv']
    doc_file = basedir + 'document_passages.json'
    outfile = [basedir + 'train-filtered.txt', basedir + 'dev-filtered.txt', basedir + 'test-filtered.txt']
    
    document_dict = read_passages(doc_file)
    
    for i in range(len(in_corpfile)):
        fout = open(outfile[i], 'w')
        firstline = True
        for line in open(in_corpfile[i], 'r'):
            if firstline == True: #skip the header
                firstline = False
                continue

            q_id, q_text, doc_id, doc_name, a_ids = line.split('\t')
            
            document = document_dict[doc_id]
            q_text = ' '.join(nltk.word_tokenize(q_text))
            q_text = remove_special_chars(q_id, q_text) #needed for our indri run            
            
            for p_id, passage in document.iteritems():
                passage = ' '.join(nltk.word_tokenize(passage))
                passage = remove_tabs(passage)
                if p_id in a_ids:
                    print(q_text.strip() + "\t" + passage.strip() + "\t" + "1", file=fout)
                else:
                    print(q_text.strip() + "\t" + passage.strip() + "\t" + "0", file=fout)
        
        fout.close()