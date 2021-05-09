import nltk
from nltk.corpus import stopwords
from pymongo import MongoClient
import pymongo

import os
import json
import re
import math
import time

# query = "inner class static\n"
# query
module_dir = os.path.dirname(__file__)
file_path = os.path.join(module_dir, 'index.txt')

with open(file_path) as f:
    index = json.loads(f.readlines()[0])
len(index)

N = 297501

nltk.download('stopwords')
common_words = stopwords.words('english')

client = MongoClient()
db = client.so_docs
docs = db.docs


def tokenize(s: str):
    unicode = re.compile(r"[^\U00000000-\U0000007F]")
    s = unicode.sub(" ", s)
    clean = re.compile(r'[#"():+*/$%&_]')
    delim = re.compile(r'\W+')
    newline = re.compile(r'\\n+')
    s = re.sub(newline, " ", s)
    s = clean.sub(" ", s)
    s = re.sub("'", "", s)
    s = s.lower()
    tokens = delim.split(s)
    # return tokens
    # print(tokens)
    # tokens = lemmatize_tokens(tokens)
    # print(new_tokens[:10])
    for token in tokens:
        if token in common_words:
            tokens.remove(token)
    return list(set(tokens))


def get_docs(query: str):
    tokens = tokenize(query)
    print(tokens)
    token_docs = {}
    for token in tokens:
        token_docs[token] = index[token]

    intersect = list(token_docs[tokens[0]].keys())
    for token in tokens:
        doc = list(token_docs[token].keys())
        # print(doc)
        intersect = list(set(intersect) & set(doc))
    return intersect, token_docs

    # print(tokens)


def get_rank(query: str):
    intersect, query_index = get_docs(query)
    doc_tfidf = {doc: 0 for doc in intersect}
    # print(len(intersect))
    for token in query_index.keys():
        for doc, tf in query_index[token].items():
            if doc in intersect:
                original = docs.find_one({"_id": f"{doc}"})
                # if doc not in doc_tfidf:
                #     doc_tfidf[doc] = 0
                doc_tfidf[doc] += tf / len(original['ques'].split()) * \
                    math.log(N / len(query_index[token]), 10)

    return doc_tfidf


def main(query: str):
    # query = input("Enter your query: ")
    # print(query.split())
    #
    start_time = time.time()
    ranks = get_rank(query)
    end_time = time.time()
    # print(f"{len(ranks)} results fetched in {end_time - start_time} sec:")
    # print(len(ranks))
    final_ranks = {key: value for key, value in sorted(
        ranks.items(), key=lambda x: x[1], reverse=True)}

    fetched_docs = []
    for id, tfidf in final_ranks.items():
        fetched_docs.append(tuple(docs.find_one({"_id": f"{id}"}).values()))
    print(len(fetched_docs))

    return fetched_docs, end_time - start_time
    # ranks = sorted(ranks, reverse=True)
    # print(final_ranks)
    # print(len(ranks))
