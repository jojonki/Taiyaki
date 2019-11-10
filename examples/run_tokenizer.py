"""Run tokenizer with the minimum cost
"""
import argparse
import copy
import os
import sys
import time

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from taiyaki.taiyaki import Taiyaki


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--da_dic', type=str, default='./models/ipadic-vocab.txt.dict', metavar='PATH', help='double-array dictionary')
    parser.add_argument('--word_dic_dir', type=str, default='./data/mecab-ipadic-2.7.0-20070801/', metavar='PATH', help='')
    parser.add_argument('--trans_def', type=str, default='./data/mecab-ipadic-2.7.0-20070801/matrix.def', metavar='PATH', help='')
    parser.add_argument('-q', '--query', type=str, help='query')
    args = parser.parse_args()

    query = args.query
    taiyaki = Taiyaki(args.da_dic, args.word_dic_dir, args.trans_def)
    tokens = taiyaki.tokenize(query)
    print('Input:', query)
    print('Tokens:', tokens)


if __name__ == '__main__':
    main()
