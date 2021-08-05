#!/usr/bin/env python3
# coding: utf-8

# English sentences g2p using g2p_en module
# https://github.com/Kyubyong/g2p


from g2p_en import G2p
input_file = './test_clean/data_split_graph.txt'
output_file = './test_clean/data_split_pred.txt'

with open(input_file, encoding='UTF-8') as f:
    lines = f.readlines()

g2p = G2p()

results = []
for line in lines:
    out_filtered = []
    out = g2p(line)
    for o in out:
        if o != ' ':
            out_filtered.append(o)
    results.append(line.replace("\n", "") + "\t" +
                   " ".join(out_filtered) + " \n")


with open(output_file, 'w', encoding='UTF-8') as f:
    f.writelines(results)
