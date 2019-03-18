import json
import sys
import codecs

# read parameters from files
with open('emission.txt', mode='r') as f:
    em = json.load(f)

with open('transition.txt', mode='r') as f:
    tr = json.load(f)

with open('word_tag.txt', mode='r') as f:
    w_t = json.load(f)

tags = set(tr['start'])
words = set(w_t)


def prob_emission(word_low, words, em, state):
    if word_low in words:
        p_em = em[state].get(word_low, 0)
    else:
        # p_em = 1
        p_em = 1.0 * em[state]['<ONCE>'] / (unknow * em[state]['<TOTAL>'])
    return p_em


# viterbi algorithm
res = ""

# count unknown words
unknow = 0
for line in open(sys.argv[-1], encoding='utf-8', mode='r'):
    if 1 < 20:
        line_s = line.split()
        for idx, word in enumerate(line_s):
            if word not in words:
                unknow += 1

for line in open(sys.argv[-1], encoding='utf-8', mode='r'):
    if 1 < 20:
        v = []
        line_s = line.split()
        for idx, word in enumerate(line_s):
            word_low = word.lower()
            v.append({})

            if word_low not in words:
                search_states = tr['start']
            else:
                search_states = w_t[word_low]

            if idx == 0:
                for state in search_states:
                    p_em = prob_emission(word_low, words, em, state)
                    v[idx][state] = {}
                    v[idx][state]['prob'] = tr['start'][state] * p_em
                    v[idx][state]['pre'] = None

            else:
                for tag in search_states:
                    for idx_t, pre in enumerate(v[idx - 1]):
                        if idx_t == 0:
                            max_p = v[idx - 1][pre]['prob'] * tr[pre][tag]
                            max_pre = pre
                        else:
                            if max_p < v[idx - 1][pre]['prob'] * tr[pre][tag]:
                                max_p = v[idx - 1][pre]['prob'] * tr[pre][tag]
                                max_pre = pre

                    p_em = prob_emission(word_low, words, em, tag)
                    v[idx][tag] = {}
                    v[idx][tag]['prob'] = max_p * p_em
                    v[idx][tag]['pre'] = max_pre

        states = []
        for i in range(idx, -1, -1):
            if i == idx:
                for idx_s, tag in enumerate(v[i]):
                    if idx_s == 0:
                        max_s_p = v[i][tag]['prob']
                        max_pre_state = v[i][tag]['pre']
                        max_cur_state = tag
                    else:
                        if max_s_p < v[i][tag]['prob']:
                            max_s_p = v[i][tag]['prob']
                            max_pre_state = v[i][tag]['pre']
                            max_cur_state = tag
                states.append(max_cur_state)
            else:
                states.append(max_pre_state)
                max_pre_state = v[i][max_pre_state]['pre']

        for i in range(len(line_s)):
            if i == 0:
                w = line_s[i] + '/' + states[len(line_s) - i - 1]
            else:
                w += line_s[i] + '/' + states[len(line_s) - i - 1]
            if i < len(line_s) - 1:
                w += ' '
            else:
                w += "\n"
        res += w


f = open("hmmoutput.txt", 'w')
f.write(res)
f.close()


# (22453, 25148, 0.8928344202322253) for en
# (11087, 12663, 0.8755429203190397) for zh
