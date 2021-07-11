import numpy as np
import random,os,sys


def top_one_result(tmp_list):
    index_list = sorted(range(len(tmp_list)), key=lambda k: tmp_list[k], reverse=True)[:1]
    return index_list[0]


def gen_on_keyword(tmp_Vocab, keyword, tmp_list, lookup_table):

    keyword_index = tmp_Vocab.get_idx(keyword)
    index_list = sorted(range(len(tmp_list)), key=lambda k: tmp_list[k], reverse=True)[:3]

    if (float(tmp_list[index_list[0]]) / tmp_list[index_list[1]] > 1.3):
        return index_list[0]


    # print(np.sum(np.array(lookup_table[keyword_index]) * np.array(lookup_table[keyword_index_2])))

    # similar = 0
    index = 0
    for i in range(len(index_list)):
        if (i == 0):
            # similar = abs(np.sum(np.array(lookup_table[keyword_index]) * np.array(lookup_table[index_list[0]])))
            similar = np.linalg.norm(np.array(lookup_table[keyword_index]) - np.array(lookup_table[index_list[0]]))
        else:
            dist = np.linalg.norm(np.array(lookup_table[keyword_index]) - np.array(lookup_table[index_list[i]]))
            if (dist < similar):
                similar = dist
                index = i

    return index_list[index]


def gen_diversity(tmp_list):
    index_list = sorted(range(len(tmp_list)), key=lambda k: tmp_list[k], reverse=True)[:3]
    #index_list = sorted(range(len(tmp_list)), key=lambda k: tmp_list[k], reverse=True)

    sum0 = int(round(tmp_list[index_list[0]]))
    sum1 = int(round(tmp_list[index_list[1]]))
    sum2 = int(round(tmp_list[index_list[2]]))
    numsum = sum0+sum1+sum2
    index1 = random.randint(1,numsum)
    if index1 <= sum0:
        index = index_list[0]
        return index
    elif index1 <= (sum0+sum1):
        index = index_list[1]
        return index
    else:
        index = index_list[2]
        return index
