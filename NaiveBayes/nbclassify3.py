import math
import json
import sys
import re

CLASSES = ['True', 'Fake', 'Pos', 'Neg']

# read parameters from files
with open('nbmodel.txt', mode='r') as f:
    model = json.load(f)

res = ''


# remove certain punctuation and lowercase all the letters
def pre_process(doc):
    res = []
    for word in doc:
        tmp = re.sub(r'\W', "", word.lower())
        res.append(tmp)
    return res


def naiveBayes(doc, model):
    for tag in CLASSES:
        p_class[tag] = math.log(model[tag]['<PRIOR>'])
    for word in doc:
        word_low = word.lower()
        if word_low not in model['<STOP>']:
            for tag in CLASSES:
                if word_low in model['Words']:
                    p = model[tag][word_low]
                else:
                    p = 1
                p_class[tag] += math.log(p)
            if min(p_class.values()) < -1000:
                for tag in CLASSES:
                    p_class[tag] += 1000
    return p_class


p_class = {}
for line in open(sys.argv[-1], encoding='utf-8', mode='r'):
    line_doc = line.split()
    res += line_doc[0] + ' '
    line_doc = pre_process(line_doc[1:])
    p_class = naiveBayes(line_doc, model)
    tmp = 'True' + ' ' if p_class['True'] > p_class['Fake'] else 'Fake' + ' '
    tmp += 'Pos' + '\n' if p_class['Pos'] > p_class['Neg'] else 'Neg' + '\n'
    res += tmp


f = open("nboutput.txt", 'w')
f.write(res)
f.close()
