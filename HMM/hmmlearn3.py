import collections
import sys
em = collections.defaultdict(dict)
w_t = collections.defaultdict(dict)
tr = collections.defaultdict(dict)
tags = set()

for line in open(sys.argv[-1], encoding='utf-8', mode='r'):
    for idx, pair in enumerate(line.split()):
        word, tag = pair.rsplit('/', 1)
        word_low = word.lower()

        # count tag-word pairs
        em[tag][word_low] = em[tag].get(word_low, 0) + 1
        em[tag]['<TOTAL>'] = em[tag].get('<TOTAL>', 0) + 1

        # save word-tag pairs
        w_t[word_low][tag] = 0

        # count tag-tag pairs
        if idx == 0:
            tag_pre = 'start'
        tr[tag_pre][tag] = tr[tag_pre].get(tag, 0) + 1
        tr[tag_pre]['<total>'] = tr[tag_pre].get('<total>', 0) + 1

        tag_pre = tag

        if tag not in tags:
            tags.add(tag)

# add one smooth & transition probabilities
total_tags = tags | {'start'}
for pre_tag in total_tags:
    for tag in tags:
        tr[pre_tag][tag] = tr[pre_tag].get(tag, 0) + 1
        tr[pre_tag]['<total>'] = tr[pre_tag].get('<total>', 0) + 1
    for tag in tr[pre_tag]:
        if tag != '<total>':
            tr[pre_tag][tag] = 1.0 * tr[pre_tag][tag] / tr[pre_tag]['<total>']
    del tr[pre_tag]['<total>']


# emission probabilities
for tag in em:
    once = 0
    for word in em[tag]:
        if word != '<TOTAL>':
            if em[tag][word] == 1:
                once += 1
            em[tag][word] = 1.0 * em[tag][word] / em[tag]['<TOTAL>']
    em[tag]['<ONCE>'] = once


import json
with open('emission.txt', mode='w') as f:
    json.dump(em, f)

with open('transition.txt', mode='w') as f:
    json.dump(tr, f)

with open('word_tag.txt', mode='w') as f:
    json.dump(w_t, f)
