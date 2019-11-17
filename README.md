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
共通接頭辞検索，最小コスト法による分かち書き，最長一致法による分かち書き結果が表示されます．
`-q`オプションを入れない場合，標準入力で連続して文を入力できます．

```
python examples/run_tokenizer.py -q 吾輩は猫である
Loading dictionaries...
Loaded!
Input: 吾輩は猫である
Common prefixes: ['吾', '吾輩']
Tokenized tokens (min cost): [('__BOS__', None), ('吾輩', '名詞'), ('は', '助詞'), ('猫', '名詞'), ('で', '助動詞'), ('ある', '助動詞'), ('__EOS__', None)]
Tokenized tokens (longest match): ['吾輩', 'は', '猫', 'で', 'ある']
```


## TODOs
- [ ] refactoring an lattice node style
- [ ] remove TODOs
- [ ] [未知語処理](https://github.com/taku910/mecab/blob/32041d9504d11683ef80a6556173ff43f79d1268/mecab-ipadic/unk.def)
- [ ] [学習済みCRFを使った新語追加](https://taku910.github.io/mecab/dic.html)
- [ ] integrate dictionaries
- [ ] regularization
- [ ] always invoke category processing
- [ ] (bug) Unknown words found in double_array and will cause KeyError. 「はい，おっぱっぴー」
