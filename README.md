# Israeli Government Review

* [Discussion](https://groups.google.com/d/forum/gov-supervisor).
* [Specs](https://docs.google.com/folder/d/0B3UwEwwe_DvDUm1JY2E2ZTdtdmM/edit).

## Set-up

This project uses [Flask](http://flask.pocoo.org/) as a web-framework.
[MongoDB](http://mongodb.org/) is the DB backend,
with [PyMongo](http://api.mongodb.org/python/current/) as its driver,
and [mongoengine](http://mongoengine.org/) as its ORM.
Also, it uses [Compass](http://compass-style.org/install) and
[Sass](http://sass-lang.com/download) for CSS.

* `brew install python ruby mongodb` - On **OS X**. On **Ubuntu** you can use `apt-get` and friends.
* `pip install -r ./requirements.txt` for Python packages.
* `gem update --system && gem install compass` - This will install [Compass](http://compass-style.org/install), which will also install [Sass](http://sass-lang.com/download) for you.

## Test Run

1. `./generate_initial_data.sh` - Populates DB with Hebrew **lorem-ipsum** data
2. Execute both of these simultaneously:
  * `./run_mongo.sh` - Runs in foreground.
  * `./run_server.py` - Flask app.

## Helpful Utilities

* `./run_tests.sh`
