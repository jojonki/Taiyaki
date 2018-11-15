from collections import OrderedDict


base = [0] * 10
check = [0] * 10

code  = {'#': 0, 'a': 1, 'b': 2, 'c': 3, 'd': 4}


def build_double_array(dic):
    s = 1
    base[1] = s

    crnt_pref = ''

    pref_list = []
    for k in dic.keys():
        if k[0] not in pref_list:
            pref_list.append(k[0])

    ptr = s + 1
    for c in pref_list:
        print(c)
        check[ptr] = s

        # 葉ノードチェック
        pref = crnt_pref + c
        pref_count = 0
        for d in dic.keys():
            if d.startswith(pref):
                pref_count += 1
                if pref_count > 1: # cから始まるデータが２件以上見つかったら葉ノードではない
                    break
        if pref_count == 1:
            base[ptr] = -dic[pref]
        ptr += 1

    s = s + 1
    for c in pref_list:
        sub_pref_list = [d for d in dic.keys() if d.startswith(c)]
        for sub in sub_pref_list:
        
        print(sub_pref_list)


    print('base ', base)
    print('check', check)



dic = OrderedDict({'a': 1, 'ac': 2, 'b': 3, 'cab': 4, 'cd': 5})
build_double_array(dic)
