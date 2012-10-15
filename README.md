# Israeli Government Review

* [Discussion](https://groups.google.com/d/forum/gov-review).
* [Specs](https://docs.google.com/document/d/1eJPQi3uKpvPkav7YPgf8--eFGZPgjsTLvfkCA5sM_Mg/edit).

## Requirements

This project uses [Flask](http://flask.pocoo.org/) as a web-framework.
[MongoDB](http://mongodb.org/) is the DB backend,
with [PyMongo](http://api.mongodb.org/python/current/) as its driver,
and [mongoengine](http://mongoengine.org/) as its ORM.
Also, it uses [Compass](http://compass-style.org/install) and
[Sass](http://sass-lang.com/download) for CSS.
Oh, and [Twitter Bootstrap](http://twitter.github.com/bootstrap/),
with [AbduallahDiaa's RTL version](https://github.com/AbdullahDiaa/Bootstrap-RTL) of it.

## Set-up

* `git clone`, `virtualenv`, [install Homebrew](http://mxcl.github.com/homebrew/) or use `apt-get`,
  and do whatever else is necessary to set-up a generic Python project.
* `brew install python ruby mongodb` - On **Ubuntu** use `apt-get` instead of `brew`.
* `pip install -r ./requirements.txt` for Python packages.
* `gem update --system && gem install compass` - To install [Compass](http://compass-style.org/install) and [Sass](http://sass-lang.com/download).

## Test Run

1. `cd src/server`
2. `./generate_initial_data.sh` - Populates DB with Hebrew **lorem-ipsum** data
3. Execute both of these simultaneously:
  * `./run_mongo.sh` - Runs in foreground.
  * `./run_server.py` - Flask app.

## Helpful Utilities

* `src/server/run_tests.sh`
