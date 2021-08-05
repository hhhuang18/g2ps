#!/usr/bin/env python3
# coding: utf-8

import argparse
import os

parser = argparse.ArgumentParser(
    description='g2p sentence inference based on word ngram.')
parser.add_argument('--model', type=str,
                    help='model file', required=True)
parser.add_argument('--input', type=str,
                    help='sentence or word to test.', required=False)
parser.add_argument('--inputfile', type=str,
                    help='file to test.', required=False)
parser.add_argument('--nbest', type=int,
                    help='export best n results.', required=False, default=1)
parser.add_argument('--score', type=bool,
                    help='print scores.', required=False, default=False)
parser.add_argument('--pair', type=bool,
                    help='print pairs.', required=False, default=False)
args = parser.parse_args()

if args.input is not None:
    temp_str = args.input.replace(' ', '-')
    command = 'phonetisaurus-g2pfst --model={} --nbest={} \
        --word={} --print_pairs={} --print_scores={}'.format(args.model, str(args.nbest),
        temp_str, str(args.pair).lower(), str(args.score).lower())
    res = os.popen(command).read()

elif args.inputfile is not None:
    with open(args.inputfile, encoding='UTF-8') as f:
        lines = f.readlines()

    with open('./temp_input', 'w', encoding='UTF-8') as f:
        lines = [f.write(l.replace(' ', '-')) for l in lines]

    command = 'phonetisaurus-g2pfst --model={} --nbest={} \
        --wordlist={} --print_pairs={} --print_scores={}'.format(args.model, str(args.nbest),
        './temp_input', str(args.pair).lower(), str(args.score).lower())
    res = os.popen(command).read()
    os.popen('rm -rf ./temp_input')

else:
    print('please specify input or input file')

if args.pair:
    res = res.replace('{-:|}', '')

res = res.replace('-', ' ')
res = res.replace('  ', ' ')
print(res[:-1])
