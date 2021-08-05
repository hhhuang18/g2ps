# convert dataset
g2ps_solve_dataset.py -s ../../data/train_clean/ -o ./train_clean

# generate corpus
mkdir model
g2ps_gen_word_corpus.py --lexicon_path ../../data/lexicon.txt --dataset_path ./train_clean/ --corpus_path ./model/model.corpus

# train ngram model and convert to fst
estimate-ngram -o 3 -t ./model/model.corpus -wl ./model/model.arpa
phonetisaurus-arpa2wfst --lm=./model/model.arpa --ofile=./model/model.fst