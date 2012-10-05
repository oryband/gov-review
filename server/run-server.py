#!/usr/bin/env python
# encoding: utf8

from flask import Flask, app, render_template
#from wtforms import Form, TextField, TextArea
import redis
import os
from json import loads
from random import randrange


app.host = '0.0.0.0'
DEBUG = True

ROOT = os.path.abspath(os.path.dirname(__file__))
DB_HOST = 'localhost'
DB_PORT = 6379
DB_KEY = 'gov-review'
DB_FILE = '%s/db/dump.rdb' % ROOT

app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def index():
    #r = redis.StrictRedis(host=DB_HOST, port=DB_PORT, db=0)
    #reports = r.hgetall(DB_KEY)
    #for k in reports.keys():  # Convert JSON to dict.
        #reports[k] = loads(reports[k])

    f = open('data.json', 'rb')
    data = loads(f.read())
    chapters = data['chapters']
    f.close()

    # Loads random defects.
    defects = []
    l = len(chapters)
    for x in range(4):
        c = randrange(l)
        ll = len(chapters[c]['sub-chapters'])
        sc = randrange(ll)
        sub_chapters = chapters[c]['sub-chapters']
        lll = len(sub_chapters[sc]['defects'])
        d = randrange(lll)
        ds = sub_chapters[sc]['defects'][d]

        defects.append({
            'chapter': c,
            'sub_chapter': sub_chapters[sc]['name'],
            'defect_number': d,
            'tags': ds['tags'],
            'status': ds['status'],
            'entities': sub_chapters[sc]['entities'],
            'url': ds['url'],
            'description': ds['description']
        })

    return render_template('index.html', defects=defects)


@app.route('/add')
def add():
    return render_template('add.html')


if __name__ == '__main__':
    app.run(debug=DEBUG)
