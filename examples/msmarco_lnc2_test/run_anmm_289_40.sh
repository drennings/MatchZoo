cd ../../

currpath=`pwd`
# train the model
python matchzoo/main.py --phase train --model_file ${currpath}/examples/msmarco_lnc2_test/config/anmm_msmarco_lnc2_test_289_40.config


# predict with the model

python matchzoo/main.py --phase predict --model_file ${currpath}/examples/msmarco_lnc2_test/config/anmm_msmarco_lnc2_test_289_40.config
