### G2P Tool for Sentences

**To run the demos, you would need**

- python3
- pandas
- kaldialign  

**Run the demos**

```shell
# Have a look at the contents
ls
# README.md  data  experiments  models  phonetisaurus  setup.sh

# Initialize
source setup.sh

# Quick test with the pretrained model for English sentence
g2ps_apply.py --model ./models/model.fst --input "I HAVE A DREAM"
# I HAVE A DREAM  AY1 HH AE1 V AH0 D R IY1 M

# Show scores and G-P pairs
g2ps_apply.py --model ./models/model.fst --input "I HAVE A DREAM" --score true --pair true
# I HAVE A DREAM  18.216  {I:AY1} {H|A|V|E:HH|AE1|V} {A:AH0} {D|R|E|A|M:D|R|IY1|M}
```

1. G2P based on word ngram (the main method in this tool)

```shell
cd experiments/g2ps_word_ngram/

./train.sh
# please wait a while... (~2 minutes)

./test.sh
# total lines:        2620
# removed SPN lines:  193
# left lines:         2427
# dataset solved
# ignore stress: False
# predicted and target len match: True
# sentence accuracy: 19.15945611866502 %
# phone accuracy:    96.05527944187017 %
# detailed results exported as: result_test_clean.csv

./test_top5_ignore_stress.sh
# total lines:        2620
# removed SPN lines:  193
# left lines:         2427
# dataset solved
# ignore stress: True
# predicted and target len match: True
# sentence accuracy: 53.77008652657602 %
# phone accuracy:    98.48288900616471 %
# detailed results exported as: result_test_clean.csv
```

2. G2P based on looking up lexicon and WFST out-of-vocabulary prediction (for comparison)

```shell
cd experiments/g2ps_by_lexicon/

./train.sh
# please wait a while... (~10 minutes)

./test.sh
# total lines:        2620
# removed SPN lines:  193
# left lines:         2427
# dataset solved
# ignore stress: False
# predicted and target len match: True
# sentence accuracy: 9.10589204779562 %
# phone accuracy:    93.65144722877872 %
# detailed results exported as: result_test_clean.csv
```

3. G2P based on g2p_en module (for comparison)

   https://github.com/Kyubyong/g2p

```shell
cd experiments/3rdparty_g2p_en/
# directly test using the pretrained model provided by the g2p_en

# need to install g2p_en
pip install g2p_en

./test.sh
# total lines:        2620
# removed SPN lines:  193
# left lines:         2427
# dataset solved
# ignore stress: False
# predicted and target len match: True
# sentence accuracy: 7.787391841779979 %
# phone accuracy:    92.53797127000053 %
# detailed results exported as: result_test_clean.csv
```

**If you would like to compile phonetisaurus, you would need** 

- openfst >= 1.6.0
- mitlm 

For more details about phonetisaurus, please refer to:

https://github.com/AdolfVonKleist/Phonetisaurus