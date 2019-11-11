"""Load mecab vocabulary dictionaries and matrix.dex
"""
import codecs
import glob
import os


def loadMatrixDef(fpath):
    print('Loading', fpath)
    trans_cost = {}
    with open(fpath, 'r') as fin:
        next(fin)
        for l in fin:
            d = l.split(' ')
            trans_cost['{}:{}'.format(d[0], d[1])] = int(d[2])
    print('Loaded!')

    return trans_cost


def loadDictionary(dic_dir):
    csv_files = glob.glob(os.path.join(dic_dir, '*.csv'))
    vocab = {
            '__BOS__': {'lctx_id': 0, 'rctx_id': 0, 'emission_cost': 0, 'pos': None},
            '__EOS__': {'lctx_id': 1316, 'rctx_id': 1316, 'emission_cost': 0, 'pos': None}} # TODO must load the number from matrix.def
    for c in csv_files:
        print('Load', c)
        with codecs.open(c, 'r', 'euc_jp') as fin:
            for l in fin:
                d = l.split(',')
                if d[0] not in vocab: # TODO should support duplicate surfaces (e.g., 生野(イクノ, イケノ))
                    vocab[d[0]] = {
                        'lctx_id': int(d[1]),
                        'rctx_id': int(d[2]),
                        'emission_cost': int(d[3]),
                        'pos': d[4]
                    }

    return vocab


if __name__ == '__main__':
    vocab = loadDictionary('./data/mecab-ipadic-2.7.0-20070801/')
    trans_cost = loadMatrixDef('./data/mecab-ipadic-2.7.0-20070801/matrix.def')
