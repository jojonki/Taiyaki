"""Build script for Taiyaki

This scripts generate the following dictionaries.
1. DoubleArray dictionary
2. Vocabulary dictionary
3. Transition cost dictionary
"""

import argparse
import os
import time

from taiyaki.double_array import DoubleArray
import taiyaki.mecab_data_loader as mdl
from utils.common import savePickle


def build_double_array(da, word_list_file, da_dic_file):
    """Build a double-array dictionary file.
    """
    build_begin_time = time.time()
    with open(word_list_file, 'r') as fin:
        word_list = sorted([l.rstrip() for l in fin.readlines()])
    word_list = sorted([w + '#' for w in word_list if not w.startswith('#')])

    print('Building vocabuary...')
    da.build(word_list)
    print('Building time of your double-array: {:.1f}s'.format(time.time() - build_begin_time))
    print('You have built the double-array dictionary!: {}'.format(da_dic_file))
    da.save(da_dic_file)
    da.report()

    return da


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--word_list_file', type=str, default='./data/ipadic-words.txt', metavar='PATH', help='')
    parser.add_argument('--da_dic_file', type=str, metavar='PATH', default='./data/da.dict', help='')
    parser.add_argument('--ipadic_dir', type=str, metavar='PATH', default='./data/mecab-ipadic-2.7.0-20070801/', help='')
    parser.add_argument('--vocab_dic_file', type=str, metavar='PATH', default='./data/vocab.dict', help='')
    parser.add_argument('--trans_cost_file', type=str, metavar='PATH', default='./data/trans_cost.dict', help='')
    parser.add_argument('--char_cat_def_file', type=str, metavar='PATH', default='./data/char_cat_def.dict', help='')
    args = parser.parse_args()

    print('-------------------------------------------------------')
    print('Build your double-array!')
    da = DoubleArray()
    da = build_double_array(da, args.word_list_file, args.da_dic_file)

    print('-------------------------------------------------------')
    print('Build your vocabulary dictionary!')
    vocab = mdl.loadDictionary(args.ipadic_dir)
    savePickle(vocab, args.vocab_dic_file)

    print('-------------------------------------------------------')
    print('Build your transition cost dictionary!')
    trans_cost = mdl.loadMatrixDef(os.path.join(args.ipadic_dir, 'matrix.def'))
    savePickle(trans_cost, args.trans_cost_file)

    print('-------------------------------------------------------')
    print('Build your char.def dictionary!')
    char_cat_def = mdl.loadCharDef(os.path.join(args.ipadic_dir, 'char.def'))
    savePickle(char_cat_def, args.char_cat_def_file)


if __name__ == '__main__':
    main()
