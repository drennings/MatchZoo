cd ../../

currpath=`pwd`
# train the model
python matchzoo/main.py --phase train --model_file ${currpath}/examples/wikipassageqa_tfc1_all/config/conv_knrm_wikipassageqa.config


# predict with the model

python matchzoo/main.py --phase predict --model_file ${currpath}/examples/wikipassageqa_tfc1_all/config/conv_knrm_wikipassageqa.config
