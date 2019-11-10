"""Sample program to use Taiyaki
"""

import argparse
import gzip
import os
import sys
import time

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from taiyaki.taiyaki import Taiyaki


def main():
    begin_time = time.time()

    parser = argparse.ArgumentParser()
    parser.add_argument('--dic', required=True, type=str, metavar='PATH', help='double array dic file')
    args = parser.parse_args()

    taiyaki = Taiyaki(args.dic)
    query = '吾輩は猫である'
    taiyaki.longest_search(query)


if __name__ == '__main__':
    main()
