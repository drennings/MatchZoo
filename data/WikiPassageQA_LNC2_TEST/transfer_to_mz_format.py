# coding: utf-8

import os
import sys


basedir = './WikiPassageQA_LNC2_TEST/'
dstdir = './'
infiles = [ basedir + 'WikiPassageQA-train-filtered.txt', basedir + 'WikiPassageQA-dev-filtered.txt', basedir + 'WikiPassageQA_LNC2-test-filtered.txt' ]
outfiles = [ dstdir + 'WikiPassageQA-mz-train.txt', dstdir + 'WikiPassageQA-mz-dev.txt', dstdir + 'WikiPassageQA_LNC2_TEST-mz-test.txt' ]

for idx, infile in enumerate(infiles):
    outfile = outfiles[idx]
    fout = open(outfile, 'w')
    for line in open(infile, 'r'):
        r = line.strip().split('\t')
        if len(r) < 3:
            continue
        fout.write('%s\t%s\t%s\n' % (r[2], r[0], r[1]))
    fout.close()



