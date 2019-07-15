#!/usr/bin/env python
# coding: utf-8

import requests
from pprint import pprint
q = 'When year did Trump co-author a book about his life'
q = 'What award did Obama win?'
response = requests.post('http://10.60.1.71:8992/search', json={'query': q,'category':'wiki_data'})

pprint(response.json())

