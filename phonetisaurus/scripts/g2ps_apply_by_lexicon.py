#!/usr/bin/env python3
# coding: utf-8


from collections import defaultdict
import sys
import re
import subprocess


def get_lexicon(lexicon_file):
    lexicon = defaultdict(list)
    with open(lexicon_file, "r") as f:
        for line in f:
            # py2py3 compatbility,
            if sys.version_info[0] < 3:
                line = line.decode("utf8").strip()
            else:
                line = line.strip()
            try:
                word, pron = re.split(r'[;,\s]', line, 1)
            except:
                print(line)

            lexicon[word].append(pron)
    return lexicon


def get_phone_pred(word, model):
    g2p_command = ["phonetisaurus-g2pfst", "--model="+model, "--word="+word]
    proc = subprocess.Popen(g2p_command, stdout=subprocess.PIPE)
    for line in proc.stdout:
        parts = re.split(r"\t", line.decode("utf8").strip())
        if not len(parts) == 3:
            print("no pron for word", word)
            return ""
        else:
            return parts[-1]


def get_words_pred(words, lexicon, model):
    phones = []
    for word in words:
        phone = lexicon[word]
        if len(phone):
            phones.append(phone[0])
        else:
            # print('predict oov:',word)
            phones.append(get_phone_pred(word, model))
    phones = [p.strip() for p in phones]
    return phones


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='g2p sentence inference based on looking up lexicon and word prediction.')
    parser.add_argument('--model', type=str,
                        help='model file', required=True)
    parser.add_argument('--lexicon', type=str,
                        help='lexicon file', required=True)
    parser.add_argument('--input', type=str,
                        help='sentence or word to test.', required=False)
    parser.add_argument('--inputfile', type=str,
                        help='file to test.', required=False)
    args = parser.parse_args()

    lexicon = get_lexicon(args.lexicon)

    if args.input is not None:
        words = args.input.replace('\n', '').split(' ')
        phones = get_words_pred(words, lexicon, args.model)
        print(" ".join(words) + "\t" + " ".join(phones) + " \n")

    elif args.inputfile is not None:
        with open(args.inputfile, encoding='UTF-8') as f:
            lines = f.readlines()

            for line in lines:
                words = line.replace('\n', '').split(' ')
                phones = get_words_pred(words, lexicon, args.model)
                print(" ".join(words) + "\t" + " ".join(phones))
    else:
        print('please specify input or input file')
