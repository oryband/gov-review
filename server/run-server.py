#!/usr/bin/env python
# encoding: utf8

from flask import Flask, app, render_template, redirect, url_for, request
#from wtforms import Form, TextField, TextArea
import os


app.host = '0.0.0.0'
DEBUG = True

ROOT = os.path.abspath(os.path.dirname(__file__))
DB = '%s/db/dump.rdb' % ROOT

app = Flask(__name__)
app.config.from_object(__name__)


def init_db():
    """Load reports from db file."""
    # TODO
    pass


@app.route('/')
def index():
    return render_template('index.html')


#@app.route('/fa')
#return Response(file('static/html/index.html').read())


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
