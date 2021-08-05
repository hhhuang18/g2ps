# install g2p_en
# pip3 install g2p_en

# convert dataset
g2ps_solve_dataset.py -s ../../data/test_clean/ -o ./test_clean

# inference
./g2p_en_module_apply.py

# calculate accuracy
g2ps_cal_acc.py --graph ./test_clean/data_split_graph.txt --target ./test_clean/data_split_phone.txt --predict ./test_clean/data_split_pred.txt --result_csv result_test_clean.csv --ignore_stress false