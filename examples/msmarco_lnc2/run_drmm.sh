cd ../../

currpath=`pwd`
# train the model
python matchzoo/main.py --phase train --model_file ${currpath}/examples/msmarco_lnc2/config/drmm_msmarco.config


# predict with the model

python matchzoo/main.py --phase predict --model_file ${currpath}/examples/msmarco_lnc2/config/drmm_msmarco.config
