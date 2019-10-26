"""Generate a vocabulary file from ipadic"""

import argparse
import codecs
import glob
import os
import time


def main():
    begin_time = time.time()

    parser = argparse.ArgumentParser()
    parser.add_argument('--ipadic_dir', type=str, metavar='PATH', default='./utils/mecab-ipadic-2.7.0-20070801', help='mecab ipadic dir')
    parser.add_argument('--out', type=str, metavar='PATH', default='./utils/ipadic-vocab.txt', help='output filename')
    args = parser.parse_args()

    # get all the csv files in that directory (assuming they have the extension .csv)
    csv_files = glob.glob(os.path.join(args.ipadic_dir, '*.csv'))
    with open(args.out, 'w') as fout:
        for c in csv_files:
            print('Load', c)
            with codecs.open(c, 'r', 'euc_jp') as fin:
                for l in fin:
                    fout.write('{}\n'.format(l.split(',')[0]))

    print('Output:', args.out)
    print('Process time: {:.1f}s'.format(time.time() - begin_time))


if __name__ == '__main__':
    main()
