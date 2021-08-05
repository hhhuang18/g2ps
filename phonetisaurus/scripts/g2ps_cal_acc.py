#!/usr/bin/env python3
# coding: utf-8

import argparse
import pandas as pd
from kaldialign import edit_distance

parser = argparse.ArgumentParser(description='convert dataset for g2p')
parser.add_argument('--graph', type=str,
                    help='graph file', required=True)
parser.add_argument('--target', type=str,
                    help='target phone file', required=True)
parser.add_argument('--predict', type=str,
                    help='predict phone file', required=True)
parser.add_argument('--top_n', type=int,
                    help='best N accuracy.', required=False, default=1)
parser.add_argument('--ignore_stress', type=str,
                    help='ignore the stress number in cmudict.', required=False, default='False')
parser.add_argument('--result_csv', type=str,
                    help='filename of results csv', required=False)

args = parser.parse_args()

phone_grap_file = args.graph
phone_targ_file = args.target
phone_pred_file = args.predict
top_n = args.top_n
ignore_stress = args.ignore_stress.lower() == 'true'
print('ignore stress:',ignore_stress)


with open(phone_grap_file, encoding='UTF-8') as f:
    grap = f.readlines()
grap = [l.replace('\n', '').strip() for l in grap]

with open(phone_targ_file, encoding='UTF-8') as f:
    targ = f.readlines()
targ = [l.replace('\n', '').strip() for l in targ]


with open(phone_pred_file, encoding='UTF-8') as f:
    pred_raw = f.readlines()


s_save = 1
pred_list = []
temp_list = []
count = 1

for l in pred_raw:
    split_line = l.replace('\n', '').split('\t')
    s_temp = split_line[0]
    ph = split_line[-1]
    if count <= top_n and s_temp == s_save:
        temp_list.append(ph)
        count += 1
    else:
        pred_list.append(temp_list)
        temp_list = []
        temp_list.append(ph)
        s_save = s_temp
        count = 1
pred_list.append(temp_list)
pred_list = pred_list[1:]


print('predicted and target len match:', len(pred_list) == len(targ))


word_count = len(targ)
word_err = []

phone_count = []
phone_err = []
phone_ins = []
phone_del = []
phone_sub = []

pred = []

for k in range(word_count):
    t = targ[k]

    if ignore_stress:
        for d in ['0', '1', '2']:
            t = t.replace(d, '')

    t = t.strip().split(' ')

    phone_count.append(len(t))
    ed = 0
    total_err = float('inf')
    for pr in pred_list[k]:

        if ignore_stress:
            for d in ['0', '1', '2']:
                pr = pr.replace(d, '')

        p = pr.strip().split(' ')

        ed_temp = edit_distance(t, p)
        if ed_temp['total'] < total_err:
            total_err = ed_temp['total']
            ed = ed_temp
            pred_temp = pr

    phone_ins.append(ed['ins'])
    phone_del.append(ed['del'])
    phone_sub.append(ed['sub'])
    phone_err.append(ed['total'])
    word_err.append(int(ed['total'] > 0))

    pred.append(pred_temp)

data_dict = {
    'grap': grap,
    'targ': targ,
    'pred': pred,
    'word_err': word_err,
    'phone_err': phone_err,
    'phone_count': phone_count,
    'phone_ins': phone_ins,
    'phone_del': phone_del,
    'phone_sub': phone_sub
}

result = pd.DataFrame(data_dict)
result['phone_err_rate'] = result['phone_err']/result['phone_count']

print('sentence accuracy:', 100 -
      result['word_err'].sum() / word_count * 100, '%')
print('phone accuracy:   ', 100 -
      result['phone_err'].sum() / result['phone_count'].sum() * 100, '%')

if args.result_csv is not None:
    result.to_csv(args.result_csv, index=False)
    print('detailed results exported as:', args.result_csv)
