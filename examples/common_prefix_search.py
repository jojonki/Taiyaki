"""Sample of common prefix search
"""

import argparse
import os
import sys
import time

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from double_array import DoubleArray


def main():
    begin_time = time.time()

    parser = argparse.ArgumentParser()
    parser.add_argument('--dict', required=True, type=str, metavar='PATH', help='double-array dictionary')
    parser.add_argument('--q', type=str, help='query of commonPrefixSearch. Use commna (,) to specify multi queries.')
    args = parser.parse_args()

    da = DoubleArray()
    print('Loading dic...')
    da.load(args.dict)
    print('Loaded!')

    query_list = args.q.split(',')
    for q in query_list:
        print('=====Search {}======'.format(q))
        cp_list = da.commonPrefixSearch(q)
        print('commonPrefixSearch("{}"): {}'.format(q, cp_list))

    print('Process time: {:.1f}s'.format(time.time() - begin_time))


if __name__ == '__main__':
    main()
