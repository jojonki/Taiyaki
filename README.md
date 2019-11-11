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
```
python examples/run_tokenizer.py -q 吾輩は猫である
```


## TODOs
- [ ] udpate documents
- [ ] refactoring an lattice node style
- [ ] remove TODOs
- [ ] save original dictionary data as pkl which includes double array and ipadic data
