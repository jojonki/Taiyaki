"""Main program to build or use your double-array
"""

import argparse
import gzip
import os
import sys
import time
from tqdm import tqdm

from double_array import DoubleArray


def build(da, vocab_file):
    with open(vocab_file, 'r') as f:
        word_list = sorted([l.rstrip() for l in f.readlines()])
    word_list = sorted([w + '#' for w in word_list if not w.startswith('#')])
    print('Sample words', word_list[:10])

    print('Building vocabuary...')
    da.build(word_list)
    dic_file = './models/{}.dict'.format(vocab_file.split('/')[-1])
    print('You have built the double-array dictionary!: {}'.format(dic_file))
    da.save(dic_file)
    da.report()


def main():
    begin_time = time.time()

    parser = argparse.ArgumentParser()
    parser.add_argument('--vocab', required=True, type=str, metavar='PATH', help='vocabulary file')
    args = parser.parse_args()

    da = DoubleArray()
    build(da, args.vocab)

    sample_query_list = ['東', '東京', '東京タワー', '東京都議会', '別個']
    for q in sample_query_list:
        print('=====Search {}======'.format(q))
        cp_list = da.commonPrefixSearch(q)
        print('commonPrefixSearch("{}"): {}'.format(q, cp_list))

    print('Process time: {:.1f}s'.format(time.time() - begin_time))


if __name__ == '__main__':
    # import cProfile
    main()
    # cProfile.run('main()', sort='time')
