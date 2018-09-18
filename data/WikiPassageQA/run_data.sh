#!/bin/bash
# help, dos2unix file
# download the wiki-passage-qa dataset
#wget http://ciir.cs.umass.edu/downloads/wikipassageqa/WikiPassageQA.zip
#unzip WikiPassageQA.zip ./WikiPassageQA

# download the glove vectors
#wget http://nlp.stanford.edu/data/glove.840B.300d.zip
#unzip glove.840B.300d.zip
#wget http://nlp.stanford.edu/data/glove.6B.zip
#unzip glove.6B.zip

# tokenize data
# remove chars that can not be handled by the Indri engine
# filter queries which have no right or wrong answers
#python mypreprocessor.py

# transfer the dataset into matchzoo dataset format
python transfer_to_mz_format.py
# generate the mz-datasets
python prepare_mz_data.py

# generate word embedding
python gen_w2v.py glove.840B.300d.txt word_dict.txt embed_glove_d300
python norm_embed.py embed_glove_d300 embed_glove_d300_norm
python gen_w2v.py glove.6B.50d.txt word_dict.txt embed_glove_d50
python norm_embed.py embed_glove_d50 embed_glove_d50_norm

# generate data histograms for drmm model
# generate data bin sums for anmm model
# generate idf file
cat word_stats.txt | cut -d ' ' -f 1,4 > embed.idf
python gen_hist4drmm.py 60
python gen_binsum4anmm.py 20 # the default number of bin is 20

echo "Done ..."
