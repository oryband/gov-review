#!/usr/bin/env python
# encoding: utf8

from flask import Flask, app, request, render_template
from wtforms import Form, IntegerField, SelectField, TextField, TextAreaField
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
            'chapter_name': chapters[c]['name'],
            'sub_chapter': sc,
            'name': sub_chapters[sc]['name'],
            'defect': d,
            'tags': ds['tags'],
            'status': ds['status'],
            'entities': sub_chapters[sc]['entities'],
            'url': ds['url'],
            'description': ds['description'],
            'follow-up': ds['follow-up']
        })

    return render_template('index.html', defects=defects)


@app.route('/add')
def add():
    return render_template('add.html')


@app.route('/edit/<int:chapter>/<int:sub_chapter>/<int:defect>')
def edit(chapter, sub_chapter, defect):
    f = open('data.json', 'rb')
    chapters = loads(f.read())['chapters']
    f.close()

    sc = chapters[chapter]['sub-chapters'][sub_chapter]
    d = sc['defects'][defect]

    defect = {
        'chapter': chapter,
        'chapter_name': chapters[chapter]['name'],
        'sub_chapter': sub_chapter,
        'name': sc['name'],
        'defect': defect,
        'tags': d['tags'],
        'status': d['status'],
        'entities': sc['entities'],
        'url': d['url'],
        'description': d['description'],
        'follow_up': d['follow-up']
    }

    return render_template('add.html', defect=defect)


@app.route('/update/<int:chapter>/<int:sub_chapter>/<int:defect>')
def update(chapter, sub_chapter, defect):
    form = DefectForm(request.form)
    if request.method == 'POST' and form.validate():
        # TODO: EDIT DATA
        pass


class DefectForm(Form):
    chapter_number = IntegerField('chapter-number')
    chapter_name = TextField('chapter-number')
    sub_chapter = TextField('sub-chapter')
    sub_chapter_number = IntegerField('sub-chapter-number')
    defect = TextField('defect')
    tags = TextField('tags')
    status = SelectField('status', choices=[('unfixed', 'unfixed'),
                                            ('in-progress', 'in-progress'),
                                            ('fixed', 'fixed')])
    entities = TextField('entities')
    description = TextAreaField('description')
    follow_up = TextAreaField('follow-up')


if __name__ == '__main__':
    app.run(debug=DEBUG)
