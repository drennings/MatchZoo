# coding: utf-8
"""
filter queries which have no wrong answers
Given train.txt, dev.txt, test.txt
Output train-filtered.txt, dev-filtered.txt, test-filtered.txt
"""
from __future__ import print_function

import os
import sys

if __name__ == '__main__':

    basedir = './WikiPassageQA/'
    #filter_reffile = [basedir + 'WikiQA-dev-filtered.ref', basedir + 'WikiQA-test-filtered.ref']
    #in_reffile = [basedir + 'WikiQA-dev.ref', basedir + 'WikiQA-test.ref']
    in_corpfile = [basedir + 'WikiPassageQA-train.txt', basedir + 'WikiPassageQA-dev.txt', basedir + 'WikiPassageQA-test.txt']
    outfile = [basedir + 'WikiPassageQA-train-filtered.txt', basedir + 'WikiQA-dev-filtered.txt', basedir + 'WikiQA-test-filtered.txt']

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

