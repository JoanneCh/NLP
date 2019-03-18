import collections
import re
import json
import sys

model = collections.defaultdict(dict)
CLASSES = ['True', 'Fake', 'Pos', 'Neg']

# remove certain punctuation and lowercase all the letters


def pre_process(doc):
    res = []
    for word in doc:
        tmp = re.sub(r'\W', "", word.lower())
        res.append(tmp)
    return res


for line_idx, line in enumerate(open(sys.argv[-1], encoding='utf-8', mode='r')):
    line_doc = line.split()
    t_f = line_doc[1]
    p_n = line_doc[2]
    model[t_f]['<PRIOR>'] = model[t_f].get('<PRIOR>', 0) + 1
    model[p_n]['<PRIOR>'] = model[p_n].get('<PRIOR>', 0) + 1
    line_doc = pre_process(line_doc[3:])

    for word in line_doc:
        for tag in [t_f, p_n]:
            model[tag][word] = model[tag].get(word, 0) + 1
            model[tag]['<TOTAL>'] = model[tag].get('<TOTAL>', 0) + 1


# add-one smoothing
words = model['True'].keys() | model['Fake'].keys()
words.remove('<TOTAL>')
words.remove('<PRIOR>')

for word in words:
    for tag in CLASSES:
        model[tag][word] = model[tag].get(word, 0) + 1
        model[tag]['<TOTAL>'] = model[tag].get('<TOTAL>', 0) + 1


# find "StopWords"
for word in words:
    model['Words'][word] = 0
    model['Freq'][word] = model['Pos'][word] + model['Neg'][word]

freq = sorted(model['Freq'].items(), key=lambda d: d[1], reverse=True)
stop = int(len(model['Freq']) * 0.01)
for word, count in freq[:stop]:
    model['<STOP>'][word] = count


# calculate probabilities
line_total = line_idx + 1
for tag in CLASSES:
    class_total = model[tag]['<TOTAL>']
    del model[tag]['<TOTAL>']
    for feature in model[tag]:
        if feature == '<PRIOR>':
            model[tag][feature] = 1.0 * model[tag][feature] / line_total
        else:
            model[tag][feature] = 1.0 * model[tag][feature] / class_total
    model[tag]['<TOTAL>'] = class_total


with open('nbmodel.txt', mode='w') as f:
    json.dump(model, f)
