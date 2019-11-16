"""Load mecab vocabulary dictionaries and matrix.dex
"""
import codecs
import glob
import os

# (表層形),左文脈ID,右文脈ID,コスト,品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用型,活用形,原形,読み,発音
DIC_FORM = ['surface', 'lctx_id', 'rctx_id', 'cost', 'pos', 'spos1', 'spos2', 'spos3', 'conjug_type', 'conjug_form', 'org_form', 'ruby', 'pron']
H2I = {h:i for i, h in enumerate(DIC_FORM)}

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
                '__BOS__': [0, 0, 0, None, None, None, None, None, None, None, None, None, None],
                '__EOS__': [1316, 1316, 0, None, None, None, None, None, None, None, None, None, None]
            } # TODO must load the number from matrix.def
    for c in csv_files:
        print('Load', c)
        with codecs.open(c, 'r', 'euc_jp') as fin:
            for l in fin:
                # ex)
                # 文明,1285,1285,5336,名詞,一般,*,*,*,*,文明,ブンメイ,ブンメイ
                d = l.strip().split(',')
                if d[0] not in vocab: # TODO should support duplicate surfaces (e.g., 生野(イクノ, イケノ))
                    vocab[d[0]] = []
                if d[0] == '生野':
                    print(d)

                d[H2I['lctx_id']] = int(d[H2I['lctx_id']])
                d[H2I['rctx_id']] = int(d[H2I['rctx_id']])
                d[H2I['cost']] = int(d[H2I['cost']])

                vocab[d[0]].append(d[1:])

    return vocab


if __name__ == '__main__':
    vocab = loadDictionary('./data/mecab-ipadic-2.7.0-20070801/')
    trans_cost = loadMatrixDef('./data/mecab-ipadic-2.7.0-20070801/matrix.def')
