#!/usr/bin/env python
# coding: utf-8

import requests
data = {
  'query': 'who is the president of American',
  'candidates': [
    {'id': 123, 'content': 'jinping xi, chairman of China'},
    {'id': 352, 'content': 'is trump the president of the U.S.'}
  ]
}
r = requests.post('http://10.60.1.79:9191/path', json=data)
assert r.status_code == 200, r.status_code
# assert necessary field
assert 'response' in r.json()
print (r.json())

