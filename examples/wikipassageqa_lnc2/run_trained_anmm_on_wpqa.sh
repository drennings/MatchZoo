cd ../../

currpath=`pwd`
# train the model
#python matchzoo/main.py --phase train --model_file ${currpath}/examples/wikipassageqa_lnc2/config/anmm_wikipassageqa_lnc2.config


# predict with the model

python matchzoo/main.py --phase predict --model_file ${currpath}/examples/wikipassageqa_lnc2/config/anmm_wpqa_lnc2.config
