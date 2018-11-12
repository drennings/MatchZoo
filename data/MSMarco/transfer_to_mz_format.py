# coding: utf-8

import os
import sys


basedir = './MSMarco/'
dstdir = './'
infiles = [ basedir + 'MSMarco-train-filtered.txt', basedir + 'MSMarco-dev-filtered.txt', basedir + 'MSMarco-test-filtered.txt' ]
outfiles = [ dstdir + 'MSMarco-mz-train.txt', dstdir + 'MSMarco-mz-dev.txt', dstdir + 'MSMarco-mz-test.txt' ]

for idx, infile in enumerate(infiles):
    outfile = outfiles[idx]
    fout = open(outfile, 'w')
    for line in open(infile, 'r'):
        r = line.strip().split('\t')
        fout.write('%s\t%s\t%s\n' % (r[2], r[0], r[1]))
    fout.close()



