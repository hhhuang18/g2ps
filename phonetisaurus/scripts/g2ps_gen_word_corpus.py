#!/usr/bin/env python3
# coding: utf-8

from collections import defaultdict
import os
import pandas as pd


def get_lexicon_dict(lexicon_path):
    lexicon = defaultdict(list)

    with open(lexicon_path, "r") as ifp:
        for line in ifp:
            line = line.strip()
            try:
                ls = line.split('\t', 1)
                if len(ls) > 1:
                    word, pron = ls[0].strip(), ls[1].strip()
                else:
                    ls = line.split(' ', 1)
                    word, pron = ls[0].strip(), ls[1].strip()
                lexicon[word].append(pron)
            except:
                print(line)
    print('lexicon len :', len(lexicon))
    return lexicon


def get_sen_phone_split(sen_graph, sen_phone, lexicon):
    if 'SPN' in sen_phone:
        return 0
    else:
        s_try = ''
        s_save = ''
        s_split = []

        for w in sen_graph.split(' '):
            phones = lexicon[w][::-1]

            if phones == []:
                print('OOV:', w)

            for p in phones:
                s_try = s_save + ' ' + p
                s_try = s_try.strip()

                if s_try == sen_phone[:len(s_try)]:
                    s_save = s_try
                    s_split.append([w, p])
                    break

        if (s_save + ' ') == sen_phone:
            return s_split
        else:
            return -1


def convert_to_corpus(s_split):
    cor = ''
    for s in s_split:
        k = s[0].replace('', '|')[1:-1]
        v = s[1].replace(' ', '|')
        cor += (k + '}' + v + ' -}| ')
    cor = cor[:-5] + '\n'
    return cor


def gen_corpus(lexicon_path, dataset_path, corpus_path):
    lexicon = get_lexicon_dict(lexicon_path)

    with open(os.path.join(dataset_path, 'data_split_graph.txt'), encoding='UTF-8') as f:
        graph_lines = f.readlines()
        graph_lines = [l.replace('\n', '') for l in graph_lines]

    with open(os.path.join(dataset_path, 'data_split_phone.txt'), encoding='UTF-8') as f:
        phone_lines = f.readlines()
        phone_lines = [l.replace('\n', '') for l in phone_lines]

    data_merge = pd.DataFrame({'1_x': graph_lines, '1_y': phone_lines})

    print('sentence len  :', len(data_merge))
    print('please wait for several minutes...')

    err_count = 0
    spn_count = 0

    with open(corpus_path, 'w', encoding='UTF-8') as f:
        ' -}| '
        f.write('-}|\n')
        for k in lexicon.keys():
            for v in lexicon[k]:
                cor_line = (k.replace('', '|')[
                            1:-1] + '}' + v.replace(' ', '|') + '\n')
                f.write(cor_line)

        for index, r in enumerate(data_merge.iterrows()):
            sen_graph = r[1]['1_x']
            sen_phone = r[1]['1_y']
            s_split = get_sen_phone_split(sen_graph, sen_phone, lexicon)
            if type(s_split) is list:
                cor_line = convert_to_corpus(s_split)
                f.write(cor_line)
            elif s_split < 0:
                err_count += 1
            elif s_split == 0:
                spn_count += 1

    print('mismatch len  :', err_count)
    print('spn len       :', spn_count)
    print('final len     :', len(data_merge)-err_count-spn_count)


if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(
        description='generate word corpus for ngram model.')
    parser.add_argument('--lexicon_path', type=str,
                        help='path of lexicon.txt file.', required=True)
    parser.add_argument('--dataset_path', type=str,
                        help='path of solved dataset folder.', required=True)
    parser.add_argument('--corpus_path', type=str,
                        help='path to save the corpus.', required=True)
    args = parser.parse_args()

    print('start generate corpus')
    gen_corpus(args.lexicon_path, args.dataset_path, args.corpus_path)
