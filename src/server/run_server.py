#!/usr/bin/env python
# encoding: utf8

from documents import *

from flask import Flask, app, request, render_template
from mongoengine import connect

import os
from json import loads, dumps
from random import randrange
from pprint import pprint


app.host = '0.0.0.0'
DEBUG = True

DB_NAME = 'gov_review'
ROOT = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/', methods=['GET'])
def index():
    connect(DB_NAME)
    defects = Defect.objects.order_by('-time_updated').limit(5)
    # TODO: Need to inject id into each defect object,
    # this should be the unique url for each defect.
    #pprint(defects[0].id.__str__())
    return render_template('index.html', defects=defects)


@app.route('/list', methods=['GET'])
def list():
    pass


@app.route('/defect/<oid>', methods=['GET'])
def defect(oid):
    connect(DB_NAME)
    defect = Defect.objects.get(oid)
    return render_template('defect.html', defect=defect)


#@app.route('/add')
#def add():
    #return render_template('add.html')


#@app.route('/edit/<<int:c>/<int:sc>/<int:d>', methods=['GET'])
#def edit(c, sc, d):
    #r = redis.StrictRedis(host=DB_HOST, port=DB_PORT, db=0)
    #chapter = loads(r.hgetall(DB_NAME)['chapters'])[c]

    #sub_chapter = chapter['sub-chapters'][sc]
    #defect = sub_chapter['defects'][d]

    #response = {
        #'chapter': c,
        #'chapter_name': chapter['name'],
        #'sub_chapter': sc,
        #'name': sub_chapter['name'],
        #'defect': d,
        #'status': defect['status'],
        #'url': defect['url'],
        #'tags': defect['tags'],
        #'entities': sub_chapter['entities'],
        #'description': defect['description'],
        #'follow_up': defect['follow-up']
    #}

    #return render_template('add.html', defect=response)


## chapter/sub-chapter/defect.
#@app.route('/update/<int:c>/<int:sc>/<int:d>', methods=['POST'])
#def update(c, sc, d):
    ##form = DefectForm(request.form)
    #form = request.form
    ##if form.validate():

    #r = redis.StrictRedis(host=DB_HOST, port=DB_PORT, db=0)
    #chapters = loads(r.hgetall(DB_NAME)['chapters'])

    #sub_chapter = chapters[c]['sub-chapters'][sc]
    #sub_chapter['entities'] = [entity.strip() for
                               #entity in form['entities'].split(',')]

    #defect = sub_chapter['defects'][d]
    #defect['status'] = form['status']
    #defect['url'] = form['url']
    #defect['tags'] = [tag.strip() for tag in form['tags'].split(',')]
    #defect['description'] = form['description']
    #defect['follow-up'] = form['follow-up']
    #print '------here------'

    #r.hset(DB_NAME, 'chapters', dumps(chapters))
    #r.save()

    #return render_template('index.html')


#@app.route('/delete/<int:chapter>/<int:sub_chapter>/<int:defect>')
#def delete(chapter, sub_chapter, defect):
    #f = open(DB_FILE, 'w+b')
    #data = loads(f.read())

    #sub_chapter = data['chapters'][chapter]['sub-chapters'][sub_chapter]
    #del(sub_chapter['defects'][defect])
    #if len(sub_chapter['defect']) == 0:
        #del(data['chapters'][chapter]['sub-chapters'])

    #f.close()


if __name__ == '__main__':
    app.run(debug=DEBUG)
