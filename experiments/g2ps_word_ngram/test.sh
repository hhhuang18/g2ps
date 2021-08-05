# convert dataset
g2ps_solve_dataset.py -s ../../data/test_clean/ -o ./test_clean

# inference
g2ps_apply.py --model ./model/model.fst --inputfile ./test_clean/data_split_graph.txt --score True > ./test_clean/data_split_pred.txt

# calculate accuracy
g2ps_cal_acc.py --graph ./test_clean/data_split_graph.txt --target ./test_clean/data_split_phone.txt --predict ./test_clean/data_split_pred.txt --result_csv result_test_clean.csv  --ignore_stress false