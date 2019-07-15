#!/usr/bin/env python
# coding: utf-8

import requests

response = requests.post('http://10.60.1.124:8627/sentence_ranking', data={'query': 'what is your name?', 'passage': 'my name is XXX. hellow.'})

print(response.json())
