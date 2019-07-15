#!/usr/bin/env python
# coding: utf-8


import requests
q_q_post_data = {
    "query": "who is president of US",
    "topk": 2,
    "category": "wiki_data"
}
q_q_search = requests.post('http://10.60.1.124:8000/ques_search', data=q_q_post_data)
assert  q_q_search.status_code == 200
# assert necessary field
print (q_q_search.json())
doc_post_data = {
    "query": "who is president of US",
    "doc_top_num": 2,
    "para_top_num": 3,
    "category": "wiki_data"
}
docs_search = requests.post('http://10.60.1.124:8000/docs_search', data=doc_post_data)
assert  docs_search.status_code == 200
# assert necessary field
print (docs_search.json())


