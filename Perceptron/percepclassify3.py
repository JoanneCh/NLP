import collections
import math
import json
import sys
import re

CLASSES = {'True', 'Fake', 'Pos', 'Neg'}
BINARY_CLASS = ['<T_F>', '<P_N>']


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
def pre_process(line):
    res = {}
    res['<Words>'] = {}
    line_doc = line.split()
    res['<ID>'] = line_doc[0]

    for word in line_doc[3:]:
        tmp = re.sub(r'\W', "", word)
        if tmp == '':
            res['<Words>'][tmp] = res['<Words>'].get(tmp, 0) + 1
            continue
        if not re.sub(r'[0-9]', "", tmp):
            res['<Words>']['<NUM>'] = res['<Words>'].get('<NUM>', 0) + 1
            continue
        if not re.sub(r'[A-Z]', "", tmp):
            res['<Words>']['<CA>'] = res['<Words>'].get('<CA>', 0) + 1
        tmp = tmp.lower()
        # tmp = suffix(tmp)
        res['<Words>'][tmp] = res['<Words>'].get(tmp, 0) + 1

    return res


def classifier(doc, word_list, bi_class, param, line_idx):
    res = collections.OrderedDict()
    for doc_idx in range(line_idx + 1):
        doc_id = doc[doc_idx]['<ID>']
        a = 0
        for word in doc[doc_idx]['<Words>']:
            if word in word_list:
                w = param[bi_class][word]
                x = doc[doc_idx]['<Words>'][word]
                a += w * x
        a += param[bi_class]['<b>']

        if bi_class == '<T_F>':
            res[doc_id] = 'True' if a >= 0 else 'Fake'

        if bi_class == '<P_N>':
            res[doc_id] = 'Pos' if a >= 0 else 'Neg'

    return res


with open(sys.argv[-2], encoding='utf-8', mode='r') as f:
    param = json.load(f)
word_list = param['<P_N>'].keys()


doc = collections.defaultdict(dict)
for line_idx, line in enumerate(open(sys.argv[-1], encoding='utf-8', mode='r')):
    doc[line_idx] = pre_process(line)

label = collections.defaultdict(dict)
for bi_class in BINARY_CLASS:
    label[bi_class] = classifier(doc, word_list, bi_class, param, line_idx)

res = ''
for id_idx in label['<P_N>']:
    res += '%s %s %s\n' % (id_idx, label['<T_F>']
                           [id_idx], label['<P_N>'][id_idx])


f = open('percepoutput.txt', 'w')
f.write(res)
f.close()
