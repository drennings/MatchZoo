cd ../../

currpath=`pwd`
# train the model
python matchzoo/main.py --phase train --model_file ${currpath}/examples/msmarco_lnc2_test/config/conv_knrm_msmarco_lnc2_test.config


# predict with the model

python matchzoo/main.py --phase predict --model_file ${currpath}/examples/msmarco_lnc2_test/config/conv_knrm_msmarco_lnc2_test.config
