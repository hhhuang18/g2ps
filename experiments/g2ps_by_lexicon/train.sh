mkdir model
cp ../../data/lexicon.txt ./model/
phonetisaurus-align --input=./model/lexicon.txt --ofile=./model/aligned.corpus --grow=true
estimate-ngram -o 6 -t ./model/aligned.corpus -wl ./model/model.arpa
phonetisaurus-arpa2wfst --lm=./model/model.arpa --ofile=./model/model.fst