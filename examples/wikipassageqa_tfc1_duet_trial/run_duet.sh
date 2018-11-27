cd ../../

currpath=`pwd`
# train the model
python matchzoo/main.py --phase train --model_file ${currpath}/examples/wikipassageqa_tfc1_duet_trial/config/duet_wikipassageqa.config


# predict with the model

python matchzoo/main.py --phase predict --model_file ${currpath}/examples/wikipassageqa_tfc1_duet_trial/config/duet_wikipassageqa.config
