"""Generate an entry file from Wikipedia data
"""

import argparse
import gzip
import random
from tqdm import tqdm


random.seed(1111)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--N', type=int, help='Number of samples. Use all lines if this is not specified')
    parser.add_argument('--wiki', type=str, metavar='PATH',
                            default='./data/jawiki-latest-all-titles-in-ns0.gz',
                            help='wikipedia all titles file')
    parser.add_argument('--out', type=str, metavar='PATH', required=True, help='output file path')
    args = parser.parse_args()
    with gzip.open(args.wiki, 'r') as fin:
        with open(args.out, 'w', encoding='utf-8') as fout:
            if args.N:
                lines = random.sample(fin.readlines(), args.N)
            else:
                lines = fin
            for ln in tqdm(lines):
                w = ln.decode('utf-8').strip()
                if len(w) >= 2:
                    print(w, file=fout)


if __name__ == '__main__':
    main()
