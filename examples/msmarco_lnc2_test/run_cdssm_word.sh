cd ../../

currpath=`pwd`
# train the model
python matchzoo/main.py --phase train --model_file ${currpath}/examples/msmarco_lnc2_test/config/cdssm_word_msmarco_lnc2_test.config


# predict with the model

python matchzoo/main.py --phase predict --model_file ${currpath}/examples/msmarco_lnc2_test/config/cdssm_word_msmarco_lnc2_test.config
