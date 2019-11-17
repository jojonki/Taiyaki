"""Generate a vocabulary file from ipadic

Generated word_list file is like below:
東京
東京都
桜
犬
"""

import argparse
import codecs
import glob
import os
import time


def main():
    begin_time = time.time()

    parser = argparse.ArgumentParser()
    parser.add_argument('--ipadic_dir', type=str, metavar='PATH', default='./data/mecab-ipadic-2.7.0-20070801/', help='mecab ipadic dir')
    parser.add_argument('--out', type=str, metavar='PATH', default='./data/ipadic-words.txt', help='output filename')
    args = parser.parse_args()

    # get all the csv files in that directory (assuming they have the extension .csv)
    csv_files = glob.glob(os.path.join(args.ipadic_dir, '*.csv'))
    words = []
    for c in csv_files:
        print('Load', c)
        with codecs.open(c, 'r', 'euc_jp') as fin:
            for l in fin:
                words.append(l.split(',')[0])
    words = sorted(list(set(words)))
    print('# of words:', len(words))
    with open(args.out, 'w') as fout:
        fout.write('\n'.join(words))

    print('Output:', args.out)
    print('Process time: {:.1f}s'.format(time.time() - begin_time))


if __name__ == '__main__':
    main()
