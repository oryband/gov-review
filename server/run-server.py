#!/usr/bin/env python
# encoding: utf8

from flask import Flask, app, render_template
#from wtforms import Form, TextField, TextArea
import redis
import os
from json import loads


app.host = '0.0.0.0'
DEBUG = True

ROOT = os.path.abspath(os.path.dirname(__file__))
DB = '%s/db/dump.rdb' % ROOT

app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def index():
    r = redis.StrictRedis(host='localhost', port=6379, db=0)

    reports = r.hgetall('gov-review')
    for k in reports.keys():  # Convert JSON to dict.
        reports[k] = loads(reports[k])

    return render_template('index.html', reports=reports.values())


@app.route('/add/')
def add(report):
    return render_template('add.html')


#class Report(Form):
    #id = TextField(u'מס\' דו"חות')
    #cp = TextField(u'פרק')  # Chapter.
    #ent = TextField(u'גופים מבוקרים')  # Critisized entities.
    #url = TextField(u'קישור')
    #desc = TextArea(u'מעקב')  # Description.
    #res = TextArea(u'החלטת הממשלה')  # Government resolution.
    #r_ent = TextField(u'הגוף המגיב')  # Remarking entity.
    #r_desc = TextArea(u'תוכן ההערה')


#@app.route('/add', methods=['GET', 'POST'])
#def add(id):
    #if request.method == 'POST' and form.validate():
        #form = Report(request.form)
        ## TODO: get dada from form & update db.
        #return redirect(url_for('index'))
    #else:
        #return render_template('add.html', form=form)


if __name__ == '__main__':
    app.run(debug=DEBUG)
