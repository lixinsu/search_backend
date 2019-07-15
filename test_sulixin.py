#!/usr/bin/env python
# coding: utf-8

import requests

response = requests.post('http://10.60.1.71:9999/en_rc', json={'question': 'what is your name?', 'contexts': ['my name is XXX.', 'your name is rc']})
print(response.json())
