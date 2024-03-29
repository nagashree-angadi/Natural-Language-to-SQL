import json
import torch
from sqlnet.utils import *
import numpy as np
import datetime

import mxnet as mx
from bert_embedding import BertEmbedding

LOCAL_TEST=True


if LOCAL_TEST:
    N_word=768
    B_word=6
    USE_SMALL=True
else:
    N_word=300
    B_word=42
    USE_SMALL=False

sql_data, table_data, val_sql_data, val_table_data,\
        test_sql_data, test_table_data, TRAIN_DB, DEV_DB, TEST_DB = \
        load_dataset(0, use_small=USE_SMALL)
word_emb = load_word_emb('glove/glove.%dB.50d.txt'%(B_word),
        use_small=USE_SMALL)



# bert_abstract = ["i.c."]
# sentences = bert_abstract.split('\n')
ctx = mx.gpu(0)
bert = BertEmbedding(ctx=ctx)
# result = bert(bert_abstract)
# print(result)
# print(result[0][1][0])
# exit(0)

# print("Length of word vocabulary: %d"%len(word_emb))

word_to_idx = {'<UNK>':0, '<BEG>':1, '<END>':2}
word_num = 3
embs = [np.zeros(N_word,dtype=np.float32) for _ in range(word_num)]

def check_and_add(tok):
    #Check if the tok is in the vocab. If not, add it.
    global word_num
    if tok not in word_to_idx:
        # print("token=",tok)
        word_to_idx[tok] = word_num
        word_num += 1
        embs.append(bert(tok,'sum')[0][1][0])

for sql in sql_data:
    for tok in sql['question_tok']:
        check_and_add(tok)
for tab in list(table_data.values()):
    for col in tab['header_tok']:
        for tok in col:
            check_and_add(tok)
for sql in val_sql_data:
    for tok in sql['question_tok']:
        check_and_add(tok)
for tab in list(val_table_data.values()):
    for col in tab['header_tok']:
        for tok in col:
            check_and_add(tok)
for sql in test_sql_data:
    for tok in sql['question_tok']:
        check_and_add(tok)
for tab in list(test_table_data.values()):
    for col in tab['header_tok']:
        for tok in col:
            check_and_add(tok)

print("Length of used word vocab: %s"%len(word_to_idx))

emb_array = np.stack(embs, axis=0)
with open('bert/word2idx.json', 'w') as outf:
    json.dump(word_to_idx, outf)
np.save(open('bert/usedwordemb.npy', 'wb'), emb_array)
