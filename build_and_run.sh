#!/bin/sh

if [ $# -ne 1 ]; then
    echo "Usage: ./build_and_run.sh <vocab_file_path>" 1>&2
    exit 1
fi

python setup.py build_ext --inplace
python main.py --vocab $1

