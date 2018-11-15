# 形態素解析の理論と実装
# Section 4.4

# 構築済みのダブル配列利用
# インデックスが1から始まることを想定しているため，baseとcheckにダミーの値を最初に入れる
code  = {'#': 0, 'a': 1, 'b': 2, 'c': 3, 'd': 4}
base  = [None, 1, 5, 6, 6, -1, -3, 9, 9, -2, 13, 12, -4, -5]
check = [None, 0, 1, 1, 1, 2, 3, 4, 2, 8, 4, 7, 11, 10]


def search(search_str):
    result = {}
    src = 1
    for i, c in enumerate(search_str):
        dst = base[src] + code[c]
        parent = check[dst]
        if src == parent:
            src = dst

            dst = base[src] + code['#']
            parent = check[dst]
            if src == parent:
                result[search_str[:i+1]] = -base[dst]

    return result


test_str_list = [
    'a',
    'ac',
    'b',
    'cab',
    'cd'
]


for test in test_str_list:
    result = search(test)
    print('Search: %s'.format(test))
    print(result)
