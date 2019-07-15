#!/usr/bin/env python
# coding: utf-8

from flask import Flask
from flask import request
from flask import Flask, jsonify
import requests
from loguru import logger
from pprint import pprint


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


def check_params():
    return True


@app.route('/search', methods=['POST'])
def do_search():
    if not check_params():
        rv = {'ERROR_CODE': 10002, 'ERROR_MESSAGE': 'Request parameter error', 'textqa_results': [], 'cqa_results': []}
        return jsonify(rv)

    query = request.json['query']
    category = request.json['category']
    rv = {'ERROR_CODE': 10000, 'ERROR_MESSAGE': '', 'textqa_results': [], 'cqa_results': []}

    # QA Recall and Ranking
    # Call qa pair recall
    # Call qa pair ranking
    res = requests.post('http://10.60.1.124:8000/ques_search', data={'query': query, "topk": 2, 'category':category })
    res = res.json()
    if res['ERROR_CODE'] != 10000:
        logger.error('wuchen service fail!')
    retrieved_qas = res['candidates']
    for idx in range(len(retrieved_qas)):
        retrieved_qas[idx]['content'] = retrieved_qas[idx]['question']
        retrieved_qas[idx]['id'] = retrieved_qas[idx]['q_id']
    print(retrieved_qas)
    res = requests.post('http://10.60.1.79:9191/path', json={'query': query, 'candidates': retrieved_qas})
    res = res.json()
    if res['ERROR'] != 10000:
        logger.error('wangzi service fail!')
    sorted_qids = res['response']
    qid2index = {qid:idx for idx, qid in enumerate(sorted_qids)}
    retrieved_qas.sort(key=lambda x: qid2index[x['id']])
    cqa_results = []
    for qa in retrieved_qas:
        cqa_results.append({'q_id': qa['id'], 'doc_id': qa['doc_id'], 'para_id': qa['para_id'], 'question': qa['content'], 'answer': qa['answer']})
    rv['cqa_results'] = cqa_results

    # Doc retrieval & rerank & split paragraph & rank Sentence & Extract answer
    # Call paragraph recall
    # Call sentence ranking
    res = requests.post('http://10.60.1.124:8000/docs_search', data={'query': query, "doc_top_num": 2, 'para_top_num': 1, "category": category})
    res = res.json()
    if res['ERROR_CODE'] != 10000:
        logger.error('wuchen service fail!')
    context = res['paras'][0]
    #res = requests.post('http://10.60.1.124:8627/sentence_ranking', data={'query': query, 'passage': context})
    #res = res.json()
    #if res['ERROR_CODE'] != 10000:
    #    logger.info('Jixiang service fail!')
    #answers = res['answer']
    #answer_sentence = answers[0]['sentence']

    res = requests.post('http://10.60.1.71:9999/en_rc', json={'question': query, 'contexts': [context['content']]})
    res = res.json()
    if res['ERROR_CODE'] != 10000:
        logger.error('wuchen service fail!')
    answer_spans = res['answers']
    answer_span = answer_spans[0]
    textqa_result = {'answer_span': answer_span, 'answer_sentence': context['content'], 'answer_start': context['content'].find(answer_span), 'doc_id': context['doc_id'], 'para_id': context['para_id']}
    rv['textqa_results'] = [textqa_result]
    return jsonify(rv)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8992)
