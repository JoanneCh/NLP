import collections
import random
import re
import json
import sys

doc = collections.defaultdict(dict)
param_v = collections.defaultdict(dict)
param_a = collections.defaultdict(dict)

BINARY_CLASS = ['<T_F>', '<P_N>']
MAXITER = 30


def suffix(a):
    b = a
    if a.endswith('sses'):
        a = a[:-2]

    if a.endswith('ational'):
        a = a[:-5] + 'e'
    if a.endswith('tional'):
        a = a[:-2]
    if a.endswith('ation'):
        a = a[:-3] + 'e'
    if a.endswith('fulness'):
        a = a[:-4]

    return a


# remove certain punctuation and lowercase all the letters
def pre_process(line, words):
    res = {}
    res['<Words>'] = {}
    line_doc = line.split()
    res['<ID>'] = line_doc[0]
    res['<T_F>'] = 1 if line_doc[1] == 'True' else -1
    res['<P_N>'] = 1 if line_doc[2] == 'Pos' else -1

    for word in line_doc[3:]:
        tmp = re.sub(r'\W', "", word)
        if tmp == '':
            res['<Words>'][tmp] = res['<Words>'].get(tmp, 0) + 1
            words[tmp] = words.get(tmp, 0) + 1
            continue
        if not re.sub(r'[0-9]', "", tmp):
            res['<Words>']['<NUM>'] = res['<Words>'].get('<NUM>', 0) + 1
            words['<NUM>'] = words.get('<NUM>', 0) + 1
            continue
        if not re.sub(r'[A-Z]', "", tmp):
            res['<Words>']['<CA>'] = res['<Words>'].get('<CA>', 0) + 1
            words['<CA>'] = words.get('<CA>', 0) + 1
        tmp = tmp.lower()
        # tmp = suffix(tmp)
        res['<Words>'][tmp] = res['<Words>'].get(tmp, 0) + 1
        words[tmp] = words.get(tmp, 0) + 1

    return res


def stop_word(weight):
    stop = set()
    freq = sorted(weight.items(), key=lambda d: d[1], reverse=True)
    thres = 0
    for i in range(len(freq)):
        if abs(freq[i][1]) <= thres:
            stop.add(freq[i][0])
    return stop


def shuffle(doc_len):
    return random.sample(range(doc_len), doc_len)


def feature_tuning(doc, line_idx, bi_class, vanilla):
    func = vanilla_percep if vanilla else averaged_percep
    weight, b = func(doc, line_idx, bi_class, {})
    stop_list = stop_word(weight)
    weight_new, b_new = func(doc, line_idx, bi_class, stop_list)
    return weight_new, b_new


def vanilla_percep(doc, line_idx, bi_class, stop_list):
    weight = {}
    for word in doc['<WordList>']:
        weight[word] = 0
    b = 0

    random.seed(6)
    for iter_idx in range(MAXITER):
        seed = random.sample(range(10), 1)
        random.seed(seed[0])
        doc_order = shuffle(line_idx + 1)
        for doc_idx in doc_order:
            a = 0
            for word in doc[doc_idx]['<Words>']:
                if word not in stop_list:
                    x = doc[doc_idx]['<Words>'][word]
                    a += 1.0 * weight[word] * x
            a += b

            y = doc[doc_idx][bi_class]
            if y * a <= 0:
                for word in doc[doc_idx]['<Words>']:
                    if word not in stop_list:
                        x = doc[doc_idx]['<Words>'][word]
                        weight[word] += y * x
                b += y

    return weight, b


def averaged_percep(doc, line_idx, bi_class, stop_list):
    weight, u = {}, {}
    for word in doc['<WordList>']:
        weight[word] = 0
        u[word] = 0
    b, beta = 0, 0
    c = 1

    random.seed(6)
    for iter_idx in range(MAXITER):
        seed = random.sample(range(10), 1)
        random.seed(seed[0])
        doc_order = shuffle(line_idx + 1)
        for doc_idx in doc_order:
            a = 0
            for word in doc[doc_idx]['<Words>']:
                if word not in stop_list:
                    x = doc[doc_idx]['<Words>'][word]
                    a += 1.0 * weight[word] * x
            a += b

            y = doc[doc_idx][bi_class]
            if y * a <= 0:
                for word in doc[doc_idx]['<Words>']:
                    if word not in stop_list:
                        x = doc[doc_idx]['<Words>'][word]
                        weight[word] += y * x
                        u[word] += y * c * x
                b += y
                beta += y * c
            c += 1

    for word in doc['<WordList>']:
        weight[word] -= 1.0 * u[word] / c
    b -= 1.0 * beta / c

    return weight, b


words = {}
for line_idx, line in enumerate(open(sys.argv[-1], encoding='utf-8', mode='r')):
    doc[line_idx] = pre_process(line, words)
doc['<WordList>'] = words


# train perceptron classifiers
for bi_class in BINARY_CLASS:
    weight, b = vanilla_percep(doc, line_idx, bi_class, {})
    stop_list = stop_word(weight)

    param_v[bi_class], param_v[bi_class]['<b>'] = vanilla_percep(
        doc, line_idx, bi_class, stop_list)
    param_a[bi_class], param_a[bi_class]['<b>'] = averaged_percep(
        doc, line_idx, bi_class, {})


with open('vanillamodel.txt', mode='w') as f:
    json.dump(param_v, f)

with open('averagedmodel.txt', mode='w') as f:
    json.dump(param_a, f)
