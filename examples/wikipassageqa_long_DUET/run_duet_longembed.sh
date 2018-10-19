cd ../../

currpath=`pwd`
# train the model
python matchzoo/main.py --phase train --model_file ${currpath}/examples/wikipassageqa_long_DUET/config/duet_wikipassageqa_longembed.config


# predict with the model

python matchzoo/main.py --phase predict --model_file ${currpath}/examples/wikipassageqa_long_DUET/config/duet_wikipassageqa_longembed.config
