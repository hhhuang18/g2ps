# convert dataset
g2ps_solve_dataset.py -s ../../data/test_clean/ -o ./test_clean

# inference
g2ps_apply_by_lexicon.py --model ./model_lex.fst --lexicon ./model/lexicon.txt --inputfile ./test_clean/data_split_graph.txt > ./test_clean/data_split_pred.txt  

# calculate accuracy
g2ps_cal_acc.py --graph ./test_clean/data_split_graph.txt --target ./test_clean/data_split_phone.txt --predict ./test_clean/data_split_pred.txt --result_csv result_test_clean.csv  --ignore_stress false