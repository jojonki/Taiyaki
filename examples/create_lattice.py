"""Create a lattice
"""

import argparse
import os
import sys
import time

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from double_array import DoubleArray
from lattice import Lattice


def main():
    # begin_time = time.time()

    parser = argparse.ArgumentParser()
    parser.add_argument('--dict', type=str, default='./models/ipadic-vocab.txt.dict', metavar='PATH', help='double-array dictionary')
    parser.add_argument('-q', '--query', type=str, help='query')
    args = parser.parse_args()

    da = DoubleArray()
    print('Loading dic...')
    da.load(args.dict)
    print('Loaded!')

    query = args.query
    lattice = Lattice(query)
    
    for idx in range(len(query)):
        cps_q = query[idx:]
        print('=====Search {}======'.format(cps_q))
        cp_list = da.commonPrefixSearch(cps_q)
        print('commonPrefixSearch("{}"): {}'.format(cps_q, cp_list))
        for cp in cp_list:
            lattice.insert(idx, idx + len(cp), cp)


    # print('Process time: {:.1f}s'.format(time.time() - begin_time))
    lattice.pprint()
    lattice.plot()



if __name__ == '__main__':
    main()
