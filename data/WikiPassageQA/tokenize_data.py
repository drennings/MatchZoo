# coding: utf-8
"""
tokenize data
Given train.tsv, dev.tsv, test.tsv
Output train-filtered.txt, dev-filtered.txt, test-filtered.txt
"""
from __future__ import print_function

import os
import sys

def prepare_question_text(q_id, question_text):
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
        #print q_id,question_text
        if q_id == "3340": #remove contents
            question_text = re.sub(r'\[[^\(]*?\]', r'', question_text)
        else: #keep contents
            question_text = re.sub(r'\[(?:[^\]|]*\|)?([^\]|]*)\]', r'\1', question_text)
    if "/" in question_text:
        #print q_id,question_text
        if q_id == "104" or q_id == "857":
            question_text = question_text.replace('/','')
        else:
            question_text = question_text.replace('/',' or ')
    
    return question_text

if __name__ == '__main__':

    basedir = './WikiPassageQA/'
    in_corpfile = [basedir + 'train.tsv', basedir + 'dev.tsv', basedir + 'test.tsv']
    outfile = [basedir + 'train.txt', basedir + 'dev.txt', basedir + 'test.txt']

    for i in range(len(filter_reffile)):
        fout = open(outfile[i], 'w')

        filtered_qids = set()
        for line in open(filter_reffile[i], 'r'):
            r = line.strip().split()
            filtered_qids.add(r[0])

        all_qids = []
        for line in open(in_reffile[i], 'r'):
            r = line.strip().split()
            all_qids.append(r[0])

        for idx,line in enumerate(open(in_corpfile[i], 'r')):
            if all_qids[idx] not in filtered_qids:
                continue
            print(line.strip(), file=fout)
        fout.close()

