import nltk
from nltk.corpus import stopwords
from pymongo import MongoClient
import pymongo

import json
import math
import time
import sys
import re
import os

nltk.download('stopwords')
common_words = stopwords.words('english')


client = MongoClient()
db = client.so_docs
docs = db.docs

# file_list = ['q1', 'q2', 'q3', 'q4'] ## TODO:
file_list = ['t1']
index = {}


def tokenize_add_index(s: str, file_num: str):
    unicode = re.compile(r"[^\U00000000-\U0000007F]")
    s = unicode.sub(" ", s)
    clean = re.compile(r'[#"():+*/$%&_]')
    delim = re.compile(r'\W+')
    newline = re.compile(r'\\n+')
    s = re.sub(newline, " ", s)
    s = clean.sub(" ", s)
    s = re.sub("'", "", s)
    s = s.lower()
    tokens = delim.split(s)[:-1]
    # print(tokens)
    N = len(tokens)
    # tokens = lemmatize_tokens(tokens)
    # print(new_tokens[:10])
    for i in range(N):
        if tokens[i] not in common_words:
            if tokens[i] not in index:
                index[tokens[i]] = {}
                index[tokens[i]][file_num] = 0
            elif file_num not in index[tokens[i]]:
                index[tokens[i]][file_num] = 0
            index[tokens[i]][file_num] += 1


def create_index():
    fnum = 1
    for file in file_list:
        fname = file + ".txt"
        with open(fname) as f:
            lines = f.readlines()
            for i in range(0, len(lines) - 1, 2):
                doc = {}
                doc["_id"] = str(fnum)
                doc['ques'] = lines[i]
                doc['url'] = lines[i + 1]
                # doc_id = docs.insert_one(doc).inserted_id #TODO
                # print(doc)
                tokenize_add_index(lines[i], fnum)
                fnum += 1


start_time = time.time()
create_index()
end_time = time.time()
print("time taken to create sorted index:", end_time - start_time)

idx = open(f'index2.txt', 'w')
# idx = open(f'index.txt', 'w') #TODO
idx.write(json.dumps(
    dict(sorted(index.items(), key=lambda t: t[0]))))
idx.close()

len(index)
