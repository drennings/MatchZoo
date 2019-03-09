# coding: utf-8

import os
import sys
import codecs
import re
basedir = './MSMarco/'
dstdir = './'
infiles = [ basedir + 'MSMarco_LNC2-train-filtered.txt', basedir + 'MSMarco_LNC2-dev-filtered.txt', basedir + 'MSMarco_LNC2-test-filtered.txt' ]
outfiles = [ dstdir + 'MSMarco-mz-train.txt', dstdir + 'MSMarco-mz-dev.txt', dstdir + 'MSMarco-mz-test.txt' ]

#for idx, infile in enumerate(infiles):
#    outfile = outfiles[idx]
#    fout = open(outfile, 'w')#, "utf-8")
#    for line in open(infile, 'r'):#, "utf-8"):
#        #line = re.sub("[^A-Za-z0-9]+", " ", line)
#        r = line.strip().split('\t')
#        if len(r) != 3:
#            print("HERE")
#            print(r)
#        for i in range(len(r)):
#            r[i] = r[i].strip("\n").strip("\t")
#        #for i in range(len(r)): #TODO rem0ved this
#        #    r[i] = re.sub("[^A-Za-z0-9]+", " ", r[i])
#        fout.write('%s\t%s\t%s\n' % (r[2], r[0], r[1]))
#    fout.close()

for idx, infile in enumerate(infiles):
    print(infile)
    outfile = outfiles[idx]
    fout = open(outfile, 'w')#, "utf-8")
    for line in open(infile, 'r'):#, "utf-8"):
        #line = re.sub("[^A-Za-z0-9]+", " ", line)
        r = line.strip().split('\t')
        if len(r) != 5:
            #print("HERE")
            print(r)
        for i in range(len(r)):
            r[i] = r[i].strip("\n").strip("\t")
        #for i in range(len(r)): #TODO rem0ved this
        #    r[i] = re.sub("[^A-Za-z0-9]+", " ", r[i])
        fout.write('Q%s\tD%s\t%s\t%s\t%s\n' % (r[0], r[1], r[2], r[3], r[4]))
    fout.close()


