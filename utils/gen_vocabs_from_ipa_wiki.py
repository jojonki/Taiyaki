"""Generate a vocabulary file from ipadic"""

import argparse
import codecs
import glob
import gzip
import os
import time

from tqdm import tqdm

def main():
    begin_time = time.time()

    parser = argparse.ArgumentParser()
    parser.add_argument('--ipadic_dir', type=str, metavar='PATH', default='./utils/mecab-ipadic-2.7.0-20070801', help='mecab ipadic dir')
    parser.add_argument('--wiki', type=str, metavar='PATH',
                            default='./data/jawiki-latest-all-titles-in-ns0.gz',
                            help='wikipedia all titles file')
    parser.add_argument('--out', type=str, metavar='PATH', default='./utils/ipa-wiki-vocab.txt', help='output filename')
    args = parser.parse_args()

    # get all the csv files in that directory (assuming they have the extension .csv)
    print('Loading ipadic:', args.ipadic_dir)
    csv_files = glob.glob(os.path.join(args.ipadic_dir, '*.csv'))
    with open(args.out, 'w') as fout:
        for c in csv_files:
            print('Load', c)
            with codecs.open(c, 'r', 'euc_jp') as fin:
                for l in fin:
                    fout.write('{}\n'.format(l.split(',')[0]))

    print('Loading wiki data:', args.wiki)
    with gzip.open(args.wiki, 'r') as fin:
        with open(args.out, 'w', encoding='utf-8') as fout:
            lines = fin
            for ln in tqdm(lines):
                w = ln.decode('utf-8').strip()
                if len(w) >= 2:
                    print(w, file=fout)

    print('Output:', args.out)
    print('Process time: {:.1f}s'.format(time.time() - begin_time))


if __name__ == '__main__':
    main()
