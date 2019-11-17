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


def loadCharDef(fpath):
    """Load char.def for unk tokens
    Returns
    -------
    chart_cat_def: dictionary
        {
            'HIRAGANA': {
                'invoke'     : 0,
                'group'      : 0,
                'length'     : 2,
                'code_begin' : '0x3041',
                'code_end'   : '0x309F'
            },
            'KATAKANA': {..},
        }
    """
    char_cat_def = {}
    cat_def_done = False
    with codecs.open(fpath, 'r', 'euc_jp') as fin:
        for l in fin:
            l = l.strip()
            if not cat_def_done:
                if not l.startswith('#') and l:
                    # DEFAULT	       0 1 0  # DEFAULT is a mandatory category!
                    parse = l.split()
                    assert len(parse) >= 4
                    cat_name = parse[0]
                    char_cat_def[cat_name] = {}
                    #   - CATEGORY_NAME: Name of category. you have to define DEFAULT class.
                    #   - INVOKE: 1/0:   always invoke unknown word processing, evan when the word can be found in the lexicon
                    #   - GROUP:  1/0:   make a new word by grouping the same chracter category
                    #   - LENGTH: n:     1 to n length new words are added
                    char_cat_def[cat_name]['invoke'] = int(parse[1])
                    char_cat_def[cat_name]['group'] = int(parse[1])
                    char_cat_def[cat_name]['length'] = int(parse[3])
                    continue

                if not l and char_cat_def:
                    cat_def_done = True
                    continue
            else:
                if cat_def_done and not l.startswith('#') and l:
                    l = l.split()
                    # ['0x5146', 'KANJINUMERIC', 'KANJI']
                    # ['0xFF10..0xFF19', 'NUMERIC']
                    code_point = [l[0], l[0]]
                    if '..' in l[0]:
                        code_point = l[0].split('..', 1)
                    cat_name = l[1]
                    if 'code_points' not in char_cat_def[cat_name]:
                        char_cat_def[cat_name]['code_points'] = []
                    char_cat_def[cat_name]['code_points'].append(code_point)

    return char_cat_def


def analyzeCharCategory(char_cat_def, char):
    """Analyze a given character category by checking code points
    Parameters
    ----------
    char_cat_def: dictionary
        Dcitionary which is obtained by loadCharDef function.
    char: string
        A character to analyze

    Returns
    -------
    cat_name: string
       Category name
    """
    assert len(char) == 1
    cp = ord(char)
    for cat_name, params in char_cat_def.items():
        if 'code_points' in params:
            for cand_cp in params['code_points']:
                cp_beg, cp_end = cand_cp
                if cp >= int(cp_beg, 16) and cp <= int(cp_end, 16):
                    return cat_name


if __name__ == '__main__':
    # vocab = loadDictionary('./data/mecab-ipadic-2.7.0-20070801/')
    # trans_cost = loadMatrixDef('./data/mecab-ipadic-2.7.0-20070801/matrix.def')
    char_cat_def = loadCharDef('./data/mecab-ipadic-2.7.0-20070801/char.def')
    # print(char_cat_def)
    for c in ['a', 'お', '1', '化', 'ア']:
        print(c, analyzeCharCategory(char_cat_def, c))
