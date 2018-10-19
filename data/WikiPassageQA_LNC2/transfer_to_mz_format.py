# coding: utf-8

import os
import sys


basedir = './WikiPassageQA_LNC2/'
dstdir = './'
infiles = [ basedir + 'WikiPassageQA_LNC2-train-filtered.txt', basedir + 'WikiPassageQA_LNC2-dev-filtered.txt', basedir + 'WikiPassageQA_LNC2-test-filtered.txt' ]
outfiles = [ dstdir + 'WikiPassageQA_LNC2-mz-train.txt', dstdir + 'WikiPassageQA_LNC2-mz-dev.txt', dstdir + 'WikiPassageQA_LNC2-mz-test.txt' ]

for idx, infile in enumerate(infiles):
    outfile = outfiles[idx]
    fout = open(outfile, 'w')
    for line in open(infile, 'r'):
        if line == "":
            continue
        r = line.strip().split('\t')
        #print(r)###TODO REMOVE TODO
        if r == [""]:
            continue
        if len(r) != 3:
            print(r)
        fout.write('%s\t%s\t%s\n' % (r[2], r[0], r[1]))
        #break###TODO REMOVE TODO
    fout.close()



