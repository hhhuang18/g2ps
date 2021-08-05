#!/usr/bin/env python3
# coding: utf-8

import argparse
import pandas as pd
import os
import sys

parser = argparse.ArgumentParser(description='convert dataset for g2p')
parser.add_argument('--source', '-s', type=str,
                    help='source folder.', required=True)
parser.add_argument('--output', '-o', type=str,
                    help='output folder.', required=True)
parser.add_argument('--remove_spn', '-r', type=bool,
                    help='remove lines contain SPN in the dataset.', required=False, default=True)
parser.add_argument('--sample', help='sampling from the whole dataset.',
                    required=False, choices=['top', 'rand'])
parser.add_argument('--sample_len', type=int,help='sampling length.',
                    required='--sample' in sys.argv)
args = parser.parse_args()

path_source = args.source
path_output = args.output

if not os.path.exists(path_output):
    os.makedirs(path_output)

data_text = pd.read_table(os.path.join(path_source, 'text'), header=None)
data_phone = pd.read_table(os.path.join(
    path_source, 'ali.phones.sym'), header=None)

data_text = data_text[0].str.split(' ', 1, expand=True)
data_phone = data_phone[0].str.split(' ', 1, expand=True)

data_merge = pd.merge(data_text, data_phone, left_on=0, right_on=0)
len_original = len(data_merge)
print('total lines:       ', len_original)

if args.remove_spn is not None:
    data_merge = data_merge[~data_merge['1_y'].str.contains('SPN')]
    len_no_spn = len(data_merge)
    print('removed SPN lines: ', len_original-len_no_spn)
    print('left lines:        ', len_no_spn)

if args.sample is not None and args.sample_len is not None:
    if args.sample == 'top':
        data_merge = data_merge[:args.sample_len]
        print('sampled top lines: ', len(data_merge))
    elif args.sample == 'rand':
        data_merge = data_merge.sample(args.sample_len)
        print('sampled rand lines:', len(data_merge))


# data_merge['1_x'] = data_merge['1_x'].str.replace(' ', '-')
data_merge[['1_x']].to_csv(os.path.join(
    path_output, 'data_split_graph.txt'), header=None, index=None)
data_merge[['1_y']].to_csv(os.path.join(
    path_output, 'data_split_phone.txt'), header=None, index=None)

print('dataset solved')
