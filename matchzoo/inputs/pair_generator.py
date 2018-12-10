# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
import sys
import random
import numpy as np
from utils.rank_io import *
from layers import DynamicMaxPooling
import scipy.sparse as sp
import tqdm

class PairBasicGenerator(object):
    def __init__(self, config):
        self.__name = 'PairBasicGenerator'
        self.config = config
        rel_file = config['relation_file']
        self.rel = read_relation(filename=rel_file)
        self.batch_size = config['batch_size']
        #print("self.batch_size")
        #print(self.batch_size)
        self.check_list = ['relation_file', 'batch_size']
        self.point = 0
        if config['use_iter']:
            self.pair_list_iter = self.make_pair_iter(self.rel)
            self.pair_list = []
        else:
            self.pair_list = self.make_pair_static(self.rel, True)
            self.pair_list_iter = None

    def check(self):
        for e in self.check_list:
            if e not in self.config:
                print('[%s] Error %s not in config' % (self.__name, e), end='\n')
                return False
        return True
    def make_pair_static(self, rel, labels=False):
        rel_set = {}
        pair_list = []
        two_and_one = 0
        two_and_zero = 0
        one_and_zero = 0
        #print(rel)
        for label, d1, d2 in rel:
            #print(d2)
            if d1 not in rel_set:
                rel_set[d1] = {}
            if label not in rel_set[d1]:
                rel_set[d1][label] = []
            if ";" in d2:
                #print("Found a ; ")
                d2_high_doc = ""
                d2_low_doc = ""
                for d2_entry in d2.split(";"):
                    #print(d2_entry)
                    if d2_high_doc == "":
                        d2_high_doc = d2_entry
                    else:
                        #d2_low_doc = ""
                        d2_delta = -1
                        if "D" in d2_entry:
                            #print("Found D")
                            d2_low_doc = d2_entry
                        else:
                            d2_delta = d2_entry
                            rel_set[d1][label].append(d2_high_doc + ";" + d2_low_doc + ";" + d2_delta)
                            
                            #print(d2_high_doc, ";",d2_low_doc,";", str(d2_delta))
            else: #below these got wrongly assigned the 1 label
                if label == 1: # filter out those that have axiomatic precedence over an answer
                    if 0 not in rel_set[d1]:
                        #print([type(key) for key in rel_set.keys()])
                        rel_set[d1][0] = [d2]
                    else:
                        rel_set[d1][0].append(d2)
                else:
                    rel_set[d1][label].append(d2)
                #print(d2)
        print("Created rel_set")
        print(len(rel_set.keys()))

        #print(rel_set)
        pbar = tqdm.tqdm(total=len(rel_set))
        for qid, val in rel_set.iteritems():
            #print(key)
            for label in val:
               if type(label) != int:
                   print(label, type(label))
               #break
            #break
#            if len(rel_set[d1]) != 3:
#                print(rel_set[d1].keys())
        print("Creating regular training data")
        for d1 in rel_set:
            #print(d1)
            #print(rel_set[d1])
            label_list = sorted(rel_set[d1].keys(), reverse = True)
            #if len(label_list[:-(len(label_list)-1)]) == 0 or len(label_list[len(label_list)-1:]) == 0:
            #for hidx, high_label in enumerate(label_list[:-1]):
            #    for low_label in label_list[hidx+1:]:
            for high_label in label_list[:-(len(label_list)-1)]:
                #for low_label in label_list[len(label_list)-1:]:
                for low_label in label_list[1:]:
            #        prev_pair_list_len = len(pair_list)
                    #print("Lets check " + str(len(rel_set[d1][high_label])) + " high instances")
                    if high_label != 2 or low_label > 1:
                        print(high_label, low_label)
                        continue
                    for high_d2 in rel_set[d1][high_label]:
                        local_high_d2 = high_d2
                        #if high_d2 == "2":
                        #    local_label = "A"
                        #else:
                        #    local_label = "NA"
                        for low_d2 in rel_set[d1][low_label]:
                            local_low_d2 = low_d2
                            axiom = "NAX"
                            delta = -1
            #                prev_pair_list_len = len(pair_list)
                            if ";" in local_low_d2:
                                local_low_d2 = local_low_d2.split(";")[0]
                            if ";" in high_d2:
                                splitted_high_d2 = high_d2.split(";")
                                local_high_d2 = splitted_high_d2[0]
                                if local_low_d2 in splitted_high_d2:
                                    continue
                                    #index_of_low_d2 = splitted_high_d2.index(local_ow_d2)
                                    #delta = splitted_high_d2[index_of_low_d2+1]
                                    #axiom = "TFC1"
                            
                            #print((d1, local_high_d2, local_low_d2, delta, str(high_label)+"_"+str(low_label)+"_"+axiom))
                            pair_list.append( (d1, local_high_d2, local_low_d2, delta, str(high_label)+"_"+str(low_label)+"_"+axiom) )
                                    #print("Searching for 2,0 rels")
                                    #print("Found axiomatic instance, 2,0")
                                    #print(d1,high_d2,low_d2,delta)
                                    #print(splitted_high_d2)
                                    #return
                                #else:
                                #    pair_list.append( (d1, high_d2, low_d2, -1, "ANA-NAX") )
                            #else:
                            #    pair_list.append( (d1, high_d2, low_d2, -1, "ANA-NAX") )
                            #new_pair_list_len = len(pair_list)
                            #if new_pair_list_len == prev_pair_list_len:
                            #    print(high_d2, high_label)
                            #    print(low_d2, low_label)
        #print(high_label, low_label)
        #    break
            pbar.update(1)
            #break
        #print("FINISHED FIRST PART")
        #print(len(set([x for x,a,b,c,d in pair_list])))
        #missing_qs = set(rel_set.keys())-set([x for x,a,b,c,d in pair_list])
        #for d1 in rel_set:
        #    if d1 in missing_qs:
        #        print(rel_set[d1])
        pbar.close()

        print("Creating axiomatic training data")
        #pbar2 = tqdm.tqdm(total=len(rel_set))
        for d1 in rel_set:
            #print(d1)
            #print(rel_set[d1])
            for label, rels in rel_set[d1].iteritems():
                if label == 0: # 0's never have a naxiomatic rel
                    continue
                for rel in rels:
                    if ";" not in rel: #this doc has no axiomatic rel
                        continue
                    splitted_rel = rel.split(";")
                    #print(splitted_rel)
                    #print( (d1, splitted_rel[0], splitted_rel[1], splitted_rel[2], str(label)+"_1?0"+"_"+"TFC1")  )
                    pair_list.append( (d1, splitted_rel[0], splitted_rel[1], splitted_rel[2], str(label)+"_1?0"+"_"+"TFC1") ) 
                    #pbar2.update(1)
            #label_lp=ist = sorted(rel_set[d1].keys(), reverse = True)
            #print("Label_list")
            #print(label_list)
            #for hidx, high_label in enumerate(label_list[:-1]):
                #print("high_label")
                #print(high_label)
                #for low_label in label_list[hidx+1:]:
                    #print("low_label")
                    #print(low_label)
                    #break
                #break
                    #if high_label == "2" and low_label == "0":
                    #    continue
                    #for high_d2 in rel_set[d1][high_label]:
                    #    for low_d2 in rel_set[d1][low_label]:
                            #print("high_d2", str(high_d2), str(high_label))
                            #print("low_d2", str(low_d2), str(low_label))
                    #        delta = -1
                    #        high_d2_local = high_d2
                            
                            # remove our addition to low_d2 for the axiom
                    #        if ";" in low_d2:
                    #            low_d2 = low_d2.split(";")[0]
                            
                    #        if ";" in high_d2:
                    #            high_low_delta_d2 = high_d2.split(";")
                    #            high_d2_local = high_low_delta_d2[0]
                    #            low_d2_axiom = high_low_delta_d2[1]
                    #            delta = high_low_delta_d2[2]  
                                
                    #            if int(high_label) == 2 and low_d2 != low_d2_axiom: # if this rel is not axiomatic
                    #                delta = -1
                    #            elif int(high_label) == 1 and low_d2 != low_d2_axiom: # if this rel is not the (axiomatic) rel we are looking for
                    #                continue
                                
                                
                                #print("Inner")
                                #print(high_d2_local)
                            #print("Outer")
                            #print(high_d2_local) 
                            #if ";" in high_d2_local:
                                #print("Found ; in high_d2_local")
                                #print("extracted high_d2", str(high_d2))
                     #       if (d1, high_d2_local, low_d2, delta) not in pair_list:
                                #print("high_d2", str(high_d2), str(high_label))
                                #print("low_d2", str(low_d2), str(low_label))
                                #print("extracted high_d2_local", str(high_d2_local))
                                #print("extracted low_d2", str(low_d2))
                                #print("extracted delta", str(delta))
                     #           pair_list.append( (d1, high_d2_local, low_d2, delta) ) #pair_list.append( (d1, high_d2_local, low_d2, delta) )
                     #           if labels:
                     #               if int(high_label) == 2:
                     #                   if int(low_label) == 1:
                     #                       two_and_one += 1
                     #                   else:
                     #                       two_and_zero += 1
                     #               else:
                     #                   one_and_zero += 1
            #pbar.update(1)
        #if labels:
        #    print("two_and_one", "two_and_zero", "one_and_zero")
        #    print(two_and_one, two_and_zero, one_and_zero)
        
        #    pbar.update(1)
        #pbar2.close()
        print('Pair Instance Count:', len(pair_list), end='\n')
        #print(pair_list)
        #return pair_list

        ANA_TFC1 = 0
        NANA_TFC1 = 0
        ANA_NAX = 0
        #NANA_NAX = 0
        for entry in pair_list:
            label = entry[4]
            if label.endswith("TFC1"):
                if label.startswith("2"):
                    ANA_TFC1 += 1
                else:
                    NANA_TFC1 += 1
            else:
                if label.startswith("2"):
                    ANA_NAX += 1
                #else:
                #    NANA_NAX += 1

        print("Axiomatic entries")
        print("Answer, non_answer", str(ANA_TFC1))
        print("Non_answer, non_answer", str(NANA_TFC1))
        print("Regular entries")
        print("Answer, non_answer", str(ANA_NAX))
        #print("Non_answer, non_answer", str(NANA_NAX))
        return pair_list
    def make_pair_iter(self, rel):
        rel_set = {}
        pair_list = []
        for label, d1, d2 in rel:
            if d1 not in rel_set:
                rel_set[d1] = {}
            if label not in rel_set[d1]:
                rel_set[d1][label] = []
            rel_set[d1][label].append(d2)

        while True:
            rel_set_sample = random.sample(rel_set.keys(), self.config['query_per_iter'])

            for d1 in rel_set_sample:
                label_list = sorted(rel_set[d1].keys(), reverse = True)
                for hidx, high_label in enumerate(label_list[:-1]):
                    for low_label in label_list[hidx+1:]:
                        for high_d2 in rel_set[d1][high_label]:
                            for low_d2 in rel_set[d1][low_label]:
                                pair_list.append( (d1, high_d2, low_d2) )
            yield pair_list

    def get_batch_static(self):
        pass

    def get_batch_iter(self):
        pass

    def get_batch(self):
        if self.config['use_iter']:
            return next(self.batch_iter)
        else:
            return self.get_batch_static()

    def get_batch_generator(self):
        pass

    @property
    def num_pairs(self):
        return len(self.pair_list)

    def reset(self):
        self.point = 0

class PairGenerator(PairBasicGenerator):
    def __init__(self, config):
        super(PairGenerator, self).__init__(config=config)
        self.__name = 'PairGenerator'
        self.config = config
        self.data1 = config['data1']
        self.data2 = config['data2']
        self.data1_maxlen = config['text1_maxlen']
        self.data2_maxlen = config['text2_maxlen']
        self.fill_word = config['vocab_size'] - 1
        self.check_list.extend(['data1', 'data2', 'text1_maxlen', 'text2_maxlen'])
        if config['use_iter']:
            self.batch_iter = self.get_batch_iter()
        if not self.check():
            raise TypeError('[PairGenerator] parameter check wrong.')
        print('[PairGenerator] init done', end='\n')

    def get_batch_static(self):
        X1 = np.zeros((self.batch_size*2, self.data1_maxlen), dtype=np.int32)
        X1_len = np.zeros((self.batch_size*2,), dtype=np.int32)
        X2 = np.zeros((self.batch_size*2, self.data2_maxlen), dtype=np.int32)
        X2_len = np.zeros((self.batch_size*2,), dtype=np.int32)
        Y = np.zeros((self.batch_size*2,), dtype=np.int32)

        Y[::2] = 1
        X1[:] = self.fill_word
        X2[:] = self.fill_word
        for i in range(self.batch_size):
            d1, d2p, d2n, delta,label = random.choice(self.pair_list)
            print(d1,d2p,d2n,delta,label)
            #if ";" in d2p:
            #    d2p = d2p.split(";")[0]
            d1_cont = list(self.data1[d1])
            d2p_cont = list(self.data2[d2p])
            d2n_cont = list(self.data2[d2n])
            d1_len = min(self.data1_maxlen, len(d1_cont))
            d2p_len = min(self.data2_maxlen, len(d2p_cont))
            d2n_len = min(self.data2_maxlen, len(d2n_cont))
            X1[i*2,   :d1_len],  X1_len[i*2]   = d1_cont[:d1_len],   d1_len
            X2[i*2,   :d2p_len], X2_len[i*2]   = d2p_cont[:d2p_len], d2p_len
            X1[i*2+1, :d1_len],  X1_len[i*2+1] = d1_cont[:d1_len],   d1_len
            X2[i*2+1, :d2n_len], X2_len[i*2+1] = d2n_cont[:d2n_len], d2n_len

        return X1, X1_len, X2, X2_len, Y

    def get_batch_iter(self):
        while True:
            self.pair_list = next(self.pair_list_iter)
            for _ in range(self.config['batch_per_iter']):
                X1 = np.zeros((self.batch_size*2, self.data1_maxlen), dtype=np.int32)
                X1_len = np.zeros((self.batch_size*2,), dtype=np.int32)
                X2 = np.zeros((self.batch_size*2, self.data2_maxlen), dtype=np.int32)
                X2_len = np.zeros((self.batch_size*2,), dtype=np.int32)
                Y = np.zeros((self.batch_size*2,), dtype=np.int32)

                Y[::2] = 1
                X1[:] = self.fill_word
                X2[:] = self.fill_word
                for i in range(self.batch_size):
                    d1, d2p, d2n = random.choice(self.pair_list)
                    d1_len = min(self.data1_maxlen, len(list(self.data1[d1])))
                    d2p_len = min(self.data2_maxlen, len(list(self.data2[d2p])))
                    d2n_len = min(self.data2_maxlen, len(list(self.data2[d2n])))
                    X1[i*2,   :d1_len],  X1_len[i*2]   = self.data1[d1][:d1_len],   d1_len
                    X2[i*2,   :d2p_len], X2_len[i*2]   = self.data2[d2p][:d2p_len], d2p_len
                    X1[i*2+1, :d1_len],  X1_len[i*2+1] = self.data1[d1][:d1_len],   d1_len
                    X2[i*2+1, :d2n_len], X2_len[i*2+1] = self.data2[d2n][:d2n_len], d2n_len

                yield X1, X1_len, X2, X2_len, Y

    def get_batch_generator(self):
        while True:
            X1, X1_len, X2, X2_len, Y = self.get_batch()
            if self.config['use_dpool']:
                yield ({'query': X1, 'query_len': X1_len, 'doc': X2, 'doc_len': X2_len, 'dpool_index': DynamicMaxPooling.dynamic_pooling_index(X1_len, X2_len, self.config['text1_maxlen'], self.config['text2_maxlen'])}, Y)
            else:
                yield ({'query': X1, 'query_len': X1_len, 'doc': X2, 'doc_len': X2_len}, Y)

class Triletter_PairGenerator(PairBasicGenerator):
    def __init__(self, config):
        super(Triletter_PairGenerator, self).__init__(config=config)
        self.__name = 'Triletter_PairGenerator'
        self.data1 = config['data1']
        self.data2 = config['data2']
        self.dtype = config['dtype'].lower()
        if self.dtype == 'cdssm':
            self.data1_maxlen = config['text1_maxlen']
            self.data2_maxlen = config['text2_maxlen']
        self.vocab_size = config['vocab_size']
        self.fill_word = self.vocab_size - 1
        self.check_list.extend(['data1', 'data2', 'dtype', 'vocab_size', 'word_triletter_map_file'])
        if config['use_iter']:
            self.batch_iter = self.get_batch_iter()
        if not self.check():
            raise TypeError('[Triletter_PairGenerator] parameter check wrong.')
        self.word_triletter_map = self.read_word_triletter_map(self.config['word_triletter_map_file'])
        print('[Triletter_PairGenerator] init done', end='\n')

    def read_word_triletter_map(self, wt_map_file):
        word_triletter_map = {}
        for line in open(wt_map_file):
            r = line.strip().split()
            word_triletter_map[int(r[0])] = list(map(int, r[1:]))
        return word_triletter_map

    def map_word_to_triletter(self, words):
        triletters = []
        for wid in words:
            triletters.extend(self.word_triletter_map[wid])
        return triletters

    def transfer_feat2sparse(self, dense_feat):
        data = []
        indices = []
        indptr = [0]
        for feat in dense_feat:
            for val in feat:
                indices.append(val)
                data.append(1)
            indptr.append(indptr[-1] + len(feat))
        res = sp.csr_matrix((data, indices, indptr), shape=(len(dense_feat), self.vocab_size), dtype="float32")
        return sp.csr_matrix((data, indices, indptr), shape=(len(dense_feat), self.vocab_size), dtype="float32")

    def transfer_feat2fixed(self, feats, max_len, fill_val):
        num_feat = len(feats)
        nfeat = np.zeros((num_feat, max_len), dtype=np.int32)
        nfeat[:] = fill_val
        for i in range(num_feat):
            rlen = min(max_len, len(feats[i]))
            nfeat[i,:rlen] = feats[i][:rlen]
        return nfeat

    def get_batch_static(self):
        X1_len = np.zeros((self.batch_size*2,), dtype=np.int32)
        X2_len = np.zeros((self.batch_size*2,), dtype=np.int32)
        Y = np.zeros((self.batch_size*2,), dtype=np.int32)

        Y[::2] = 1
        X1, X2 = [], []
        for i in range(self.batch_size):
            d1, d2p, d2n, delta, label = random.choice(self.pair_list)
            #if ";" in d2n:
            #    d2n = d2n.split(";")[0]
            d1_len = len(list(self.data1[d1]))
            d2p_len = len(list(self.data2[d2p]))
            d2n_len = len(list(self.data2[d2n]))
            X1_len[i*2], X1_len[i*2+1]  = d1_len,  d1_len
            X2_len[i*2], X2_len[i*2+1]  = d2p_len, d2n_len
            X1.append(self.map_word_to_triletter(self.data1[d1]))
            X1.append(self.map_word_to_triletter(self.data1[d1]))
            X2.append(self.map_word_to_triletter(self.data2[d2p]))
            X2.append(self.map_word_to_triletter(self.data2[d2n]))
        if self.dtype == 'dssm':
            return self.transfer_feat2sparse(X1).toarray(), X1_len, self.transfer_feat2sparse(X2).toarray(), X2_len, Y
        elif self.dtype == 'cdssm':
            return self.transfer_feat2fixed(X1, self.data1_maxlen, self.fill_word), X1_len,  \
                    self.transfer_feat2fixed(X2, self.data2_maxlen, self.fill_word), X2_len, Y


    def get_batch_iter(self):
        while True:
            self.pair_list = next(self.pair_list_iter)
            for _ in range(self.config['batch_per_iter']):
                X1_len = np.zeros((self.batch_size*2,), dtype=np.int32)
                X2_len = np.zeros((self.batch_size*2,), dtype=np.int32)
                Y = np.zeros((self.batch_size*2,), dtype=np.int32)

                Y[::2] = 1
                X1, X2 = [], []
                for i in range(self.batch_size):
                    d1, d2p, d2n = random.choice(self.pair_list)
                    d1_cont = list(self.data1[d1])
                    d2p_cont = list(self.data2[d2p])
                    d2n_cont = list(self.data2[d2n])
                    d1_len = len(d1_cont)
                    d2p_len = len(d2p_cont)
                    d2n_len = len(d2n_cont)
                    X1_len[i*2],  X1_len[i*2+1]   = d1_len, d1_len
                    X2_len[i*2],  X2_len[i*2+1]   = d2p_len, d2n_len
                    X1.append(self.map_word_to_triletter(d1_cont))
                    X1.append(self.map_word_to_triletter(d1_cont))
                    X2.append(self.map_word_to_triletter(d2p_cont))
                    X2.append(self.map_word_to_triletter(d2n_cont))
                if self.dtype == 'dssm':
                    yield self.transfer_feat2sparse(X1).toarray(), X1_len, self.transfer_feat2sparse(X2).toarray(), X2_len, Y
                elif self.dtype == 'cdssm':
                    yield self.transfer_feat2fixed(X1, self.data1_maxlen, self.fill_word), X1_len, \
                            self.transfer_feat2fixed(X2, self.data2_maxlen, self.fill_word), X2_len, Y

    def get_batch_generator(self):
        while True:
            X1, X1_len, X2, X2_len, Y = self.get_batch()
            yield ({'query': X1, 'query_len': X1_len, 'doc': X2, 'doc_len': X2_len}, Y)

class DRMM_PairGenerator(PairBasicGenerator):
    def __init__(self, config):
        super(DRMM_PairGenerator, self).__init__(config=config)
        self.__name = 'DRMM_PairGenerator'
        self.data1 = config['data1']
        self.data2 = config['data2']
        self.data1_maxlen = config['text1_maxlen']
        self.data2_maxlen = config['text2_maxlen']
        self.embed = config['embed']
        if 'bin_num' in config:
            self.hist_size = config['bin_num']
        else:
            self.hist_size = config['hist_size']
        self.fill_word = config['vocab_size'] - 1
        self.check_list.extend(['data1', 'data2', 'text1_maxlen', 'text2_maxlen', 'embed'])
        self.use_hist_feats = False
        if 'hist_feats_file' in config:
            hist_feats = read_features_without_id(config['hist_feats_file'])
            self.hist_feats = {}
            for idx, (label, d1, d2) in enumerate(self.rel):
                self.hist_feats[(d1, d2)] = hist_feats[idx]
            self.use_hist_feats = True
        if config['use_iter']:
            self.batch_iter = self.get_batch_iter()
        if not self.check():
            raise TypeError('[DRMM_PairGenerator] parameter check wrong.')
        print('[DRMM_PairGenerator] init done', end='\n')

    def cal_hist(self, t1, t2, data1_maxlen, hist_size):
        mhist = np.zeros((data1_maxlen, hist_size), dtype=np.float32)
        t1_cont = list(self.data1[t1])
        t2_cont = list(self.data2[t2])
        d1len = len(t1_cont)
        if self.use_hist_feats:
            assert (t1, t2) in self.hist_feats
            curr_pair_feats = list(self.hist_feats[(t1, t2)])
            caled_hist = np.reshape(curr_pair_feats, (d1len, hist_size))
            if d1len < data1_maxlen:
                mhist[:d1len, :] = caled_hist[:, :]
            else:
                mhist[:, :] = caled_hist[:data1_maxlen, :]
        else:
            t1_rep = self.embed[t1_cont]
            t2_rep = self.embed[t2_cont]
            mm = t1_rep.dot(np.transpose(t2_rep))
            for (i,j), v in np.ndenumerate(mm):
                if i >= data1_maxlen:
                    break
                vid = int((v + 1.) / 2. * ( hist_size - 1.))
                mhist[i][vid] += 1.
            mhist += 1.
            mhist = np.log10(mhist)
        return mhist

    def get_batch_static(self):
        X1 = np.zeros((self.batch_size*2, self.data1_maxlen), dtype=np.int32)
        X1_len = np.zeros((self.batch_size*2,), dtype=np.int32)
        X2 = np.zeros((self.batch_size*2, self.data1_maxlen, self.hist_size), dtype=np.float32)
        X2_len = np.zeros((self.batch_size*2,), dtype=np.int32)
        Y = np.zeros((self.batch_size*2,), dtype=np.int32)

        Y[::2] = 1
        X1[:] = self.fill_word
        for i in range(self.batch_size):
            d1, d2p, d2n, delta, label = random.choice(self.pair_list)
            
            d1_cont = list(self.data1[d1])
            d2p_cont = list(self.data2[d2p])
            d2n_cont = list(self.data2[d2n])
            d1_len = min(self.data1_maxlen, len(d1_cont))
            d2p_len = len(d2p_cont)
            d2n_len = len(d2n_cont)
            X1[i*2,   :d1_len],  X1_len[i*2]   = d1_cont[:d1_len],   d1_len
            X1[i*2+1, :d1_len],  X1_len[i*2+1] = d1_cont[:d1_len],   d1_len
            X2[i*2], X2_len[i*2]   = self.cal_hist(d1, d2p, self.data1_maxlen, self.hist_size), d2p_len
            X2[i*2+1], X2_len[i*2+1] = self.cal_hist(d1, d2n, self.data1_maxlen, self.hist_size), d2n_len

        return X1, X1_len, X2, X2_len, Y

    def get_batch_iter(self):
        while True:
            self.pair_list = next(self.pair_list_iter)
            for _ in range(self.config['batch_per_iter']):
                X1 = np.zeros((self.batch_size*2, self.data1_maxlen), dtype=np.int32)
                X1_len = np.zeros((self.batch_size*2,), dtype=np.int32)
                X2 = np.zeros((self.batch_size*2, self.data1_maxlen, self.hist_size), dtype=np.float32)
                X2_len = np.zeros((self.batch_size*2,), dtype=np.int32)
                Y = np.zeros((self.batch_size*2,), dtype=np.int32)

                Y[::2] = 1
                X1[:] = self.fill_word
                #X2[:] = 0.
                for i in range(self.batch_size):
                    d1, d2p, d2n = random.choice(self.pair_list)
                    d1_cont = list(self.data1[d1])
                    d2p_cont = list(self.data2[d2p])
                    d2n_cont = list(self.data2[d2n])
                    d1_len = min(self.data1_maxlen, len(d1_cont))
                    d2p_len = len(d2p_cont)
                    d2n_len = len(d2n_cont)
                    X1[i*2,   :d1_len],  X1_len[i*2]   = d1_cont[:d1_len],   d1_len
                    X1[i*2+1, :d1_len],  X1_len[i*2+1] = d1_cont[:d1_len],   d1_len
                    X2[i*2], X2_len[i*2]   = self.cal_hist(d1, d2p, self.data1_maxlen, self.hist_size), d2p_len
                    X2[i*2+1], X2_len[i*2+1] = self.cal_hist(d1, d2n, self.data1_maxlen, self.hist_size), d2n_len

                yield X1, X1_len, X2, X2_len, Y

    def get_batch_generator(self):
        while True:
            X1, X1_len, X2, X2_len, Y = self.get_batch()
            yield ({'query': X1, 'query_len': X1_len, 'doc': X2, 'doc_len': X2_len}, Y)

class PairGenerator_Feats(PairBasicGenerator):
    def __init__(self, config):
        super(PairGenerator_Feats, self).__init__(config=config)
        self.__name = 'PairGenerator'
        self.config = config
        self.check_list.extend(['data1', 'data2', 'text1_maxlen', 'text2_maxlen', 'pair_feat_size', 'pair_feat_file', 'query_feat_size', 'query_feat_file'])
        if not self.check():
            raise TypeError('[PairGenerator] parameter check wrong.')

        self.data1 = config['data1']
        self.data2 = config['data2']
        self.data1_maxlen = config['text1_maxlen']
        self.data2_maxlen = config['text2_maxlen']
        self.fill_word = config['vocab_size'] - 1
        self.pair_feat_size = config['pair_feat_size']
        self.query_feat_size = config['query_feat_size']
        pair_feats = read_features_without_id(config['pair_feat_file'])
        self.query_feats = read_features_with_id(config['query_feat_file'])
        self.pair_feats = {}
        for idx, (label, d1, d2) in enumerate(self.rel):
            self.pair_feats[(d1, d2)] = pair_feats[idx]
        if config['use_iter']:
            self.batch_iter = self.get_batch_iter()
        print('[PairGenerator] init done', end='\n')

    def get_batch_static(self):
        X1 = np.zeros((self.batch_size*2, self.data1_maxlen), dtype=np.int32)
        X1_len = np.zeros((self.batch_size*2,), dtype=np.int32)
        X2 = np.zeros((self.batch_size*2, self.data2_maxlen), dtype=np.int32)
        X2_len = np.zeros((self.batch_size*2,), dtype=np.int32)
        X3 = np.zeros((self.batch_size * 2, self.pair_feat_size), dtype=np.float32)
        X4 = np.zeros((self.batch_size * 2, self.query_feat_size), dtype=np.float32)
        Y = np.zeros((self.batch_size*2,), dtype=np.int32)

        Y[::2] = 1
        X1[:] = self.fill_word
        X2[:] = self.fill_word
        for i in range(self.batch_size):
            d1, d2p, d2n, delta, label = random.choice(self.pair_list)
            d1_len = min(self.data1_maxlen, len(self.data1[d1]))
            d2p_len = min(self.data2_maxlen, len(self.data2[d2p]))
            d2n_len = min(self.data2_maxlen, len(self.data2[d2n]))
            X1[i*2,   :d1_len],  X1_len[i*2]   = self.data1[d1][:d1_len],   d1_len
            X2[i*2,   :d2p_len], X2_len[i*2]   = self.data2[d2p][:d2p_len], d2p_len
            X3[i*2,   :self.pair_feat_size]    = self.pair_feats[(d1, d2p)][:self.pair_feat_size]
            X4[i*2,   :self.query_feat_size] = self.query_feats[d1][:self.query_feat_size]
            X1[i*2+1, :d1_len],  X1_len[i*2+1] = self.data1[d1][:d1_len],   d1_len
            X2[i*2+1, :d2n_len], X2_len[i*2+1] = self.data2[d2n][:d2n_len], d2n_len
            X3[i*2+1, :self.pair_feat_size]    = self.pair_feats[(d1, d2n)][:self.pair_feat_size]
            X4[i*2+1, :self.query_feat_size] = self.query_feats[d1][:self.query_feat_size]

        return X1, X1_len, X2, X2_len, X3, X4, Y

    def get_batch_iter(self):
        while True:
            self.pair_list = next(self.pair_list_iter)
            for _ in range(self.config['batch_per_iter']):
                X1 = np.zeros((self.batch_size*2, self.data1_maxlen), dtype=np.int32)
                X1_len = np.zeros((self.batch_size*2,), dtype=np.int32)
                X2 = np.zeros((self.batch_size*2, self.data2_maxlen), dtype=np.int32)
                X2_len = np.zeros((self.batch_size*2,), dtype=np.int32)
                X3 = np.zeros((self.batch_size*2, self.pair_feat_size), dtype=np.float32)
                X4 = np.zeros((self.batch_size*2, self.query_feat_size), dtype=np.int32)
                Y = np.zeros((self.batch_size*2,), dtype=np.int32)

                Y[::2] = 1
                X1[:] = self.fill_word
                X2[:] = self.fill_word
                for i in range(self.batch_size):
                    d1, d2p, d2n = random.choice(self.pair_list)
                    d1_len = min(self.data1_maxlen, len(self.data1[d1]))
                    d2p_len = min(self.data2_maxlen, len(self.data2[d2p]))
                    d2n_len = min(self.data2_maxlen, len(self.data2[d2n]))
                    X1[i*2,   :d1_len],  X1_len[i*2]   = self.data1[d1][:d1_len],   d1_len
                    X2[i*2,   :d2p_len], X2_len[i*2]   = self.data2[d2p][:d2p_len], d2p_len
                    X3[i*2,   :self.pair_feat_size]    = self.pair_feats[(d1, d2p)][:self.pair_feat_size]
                    X4[i*2,   :d1_len] = self.query_feats[d1][:self.query_feat_size]
                    X1[i*2+1, :d1_len],  X1_len[i*2+1] = self.data1[d1][:d1_len],   d1_len
                    X2[i*2+1, :d2n_len], X2_len[i*2+1] = self.data2[d2n][:d2n_len], d2n_len
                    X3[i*2+1, :self.pair_feat_size]    = self.pair_feats[(d1, d2n)][:self.pair_feat_size]
                    X4[i*2+1, :d1_len] = self.query_feats[d1][:self.query_feat_size]

                yield X1, X1_len, X2, X2_len, X3, X4, Y

    def get_batch_generator(self):
        while True:
            X1, X1_len, X2, X2_len, X3, X4, Y = self.get_batch()
            yield ({'query': X1, 'query_len': X1_len, 'doc': X2, 'doc_len': X2_len, 'query_feats': X4, 'pair_feats': X3}, Y)

