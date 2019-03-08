cd ../../

currpath=`pwd`
# train the model
python matchzoo/main.py --phase train --model_file ${currpath}/examples/msmarco/config/anmm_msmarco_289_40.config


# predict with the model

python matchzoo/main.py --phase predict --model_file ${currpath}/examples/msmarco/config/anmm_msmarco_289_40.config
