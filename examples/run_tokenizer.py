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


def run(taiyaki, query):
    cp_list = taiyaki.commonPrefixSearch(query)
    print('Common prefixes: {}'.format(cp_list))

    tokens = taiyaki.tokenize(query)
    print('Tokenized tokens (min cost):', tokens)

    tokens = taiyaki.longestSearch(query)
    print('Tokenized tokens (longest match):', tokens)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--da_dic_file',
                        type=str,
                        default='./data/da.dict',
                        metavar='PATH',
                        help='double-array dictionary')
    parser.add_argument('--vocab_dic_file',
                        type=str,
                        metavar='PATH',
                        default='./data/vocab.dict',
                        help='vocabulary dictionary')
    parser.add_argument('--trans_cost_file',
                        type=str,
                        metavar='PATH',
                        default='./data/trans_cost.dict',
                        help='token transition cost dictionary')
    parser.add_argument('-q', '--query',
                        type=str,
                        help='input query')
    args = parser.parse_args()

    taiyaki = Taiyaki(args.da_dic_file, args.vocab_dic_file, args.trans_cost_file)

    query = args.query
    if query:
        print('Input:', query)
        run(taiyaki, query)
    else:
        while True:
            query =input('Query (press "end" to exit)>> ')
            if query == 'end':
                break
            run(taiyaki, query)


if __name__ == '__main__':
    main()
