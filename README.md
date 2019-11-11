# Taiyaki
日本語形態素解析エンジン．

## セットアップ

1. [mecab-ipadic-2.7.0-20070801.tar.gz](https://ja.osdn.net/projects/sfnet_mecab/downloads/mecab-ipadic/2.7.0-20070801/mecab-ipadic-2.7.0-20070801.tar.gz/)をダウンロードして`./data/`において解凍．

2. Cython (dobule array)のビルド
```
python setup.py build_ext --inplace
```

3. 辞書構築
ダブル配列の辞書，語彙辞書，連接コスト辞書の３ファイルが生成されます．
```
python build.py
```

## サンプルの実行
最小コスト法による結果と最長一致法による結果が表示されます．`-q`オプションを入れない場合，標準入力で文を入力できます．
```
python examples/run_tokenizer.py -q 吾輩は猫である
Loading dictionaries...
Loaded!
Input: 吾輩は猫である
Tokens (min cost): [('__BOS__', None), ('吾輩', '名詞'), ('は', '助詞'), ('猫', '名詞'), ('で', '助動詞'), ('ある', '助動詞'), ('__EOS__', None)]
Tokens (longest match): ['吾輩', 'は', '猫', 'で', 'ある']

```


## TODOs
- [ ] udpate documents
- [ ] refactoring an lattice node style
- [ ] remove TODOs
- [ ] save original dictionary data as pkl which includes double array and ipadic data
