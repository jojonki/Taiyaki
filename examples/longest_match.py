"""Longest match search sample"""

import argparse
import os
import sys
import time

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from double_array import DoubleArray


def longest_search(da, query):
    print('Input:', query)
    begin = 0
    end = len(query)
    result = []
    while begin < end:
        cp_list = da.commonPrefixSearch(query[begin:])
        if len(cp_list):
            longest = max(cp_list, key=len)
        else:
            longest = query[begin]
        result.append(longest)
        begin += len(longest)

    print('Result:', result)


def main():
    begin_time = time.time()

    parser = argparse.ArgumentParser()
    parser.add_argument('--dict', required=True, type=str, metavar='PATH', help='double-array dictionary')
    parser.add_argument('--q', required=True, type=str, help='Query for longest match search')
    args = parser.parse_args()

    da = DoubleArray()
    print('Loading dic...')
    da.load(args.dict)
    print('Loaded!')

    if args.q:
        query = args.q
    else:
        query = '行き当りばったりにみじめでみごとに素敵な人ですね'
    longest_search(da, query)

    print('Process time: {:.1f}s'.format(time.time() - begin_time))


if __name__ == '__main__':
    main()
