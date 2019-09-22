import time
import json

import flask
import requests
app = flask.Flask('server');

@app.route('/', methods=["GET", "POST"])
def test ():
    _start = time.clock();
    res = requests.get('https://vk.com').text
    _end = time.clock();
    print(f'Время выполнения программы: {_end - _start}')
    return res

app.run('0.0.0.0', port=4000)