# Israeli Government Review

* [Discussion](https://groups.google.com/d/forum/gov-supervisor).
* [Specs](https://docs.google.com/folder/d/0B3UwEwwe_DvDUm1JY2E2ZTdtdmM/edit).

## Set-up

This project uses [Flask](http://flask.pocoo.org/) as a web-framework.
[MongoDB](http://mongodb.org/) is DB backend,
with [PyMongo](http://api.mongodb.org/python/current/) as a driver and
[mongoengine](http://mongoengine.org/) as an ORM.
Also, it uses [Compass](http://compass-style.org/install) and
[Sass](http://sass-lang.com/download) for CSS.

* `brew install python ruby mongodb`
* `pip install -r ./requirements.txt` for Python packages.
* `gem update --system && gem install compass` - This will install [Compass](http://compass-style.org/install), which will also install [Sass](http://sass-lang.com/download) for you.

## Test Run

- `./generate_initial_data.sh` - Populates DB with Hebrew **lorem-ipsum** data
- Execute both of these simultaneously:
  - `./run_mongo.sh` - Runs in foreground.
  - `./run_server.py` - Flask app.

## Helpful Utilities

* `./run_tests.sh`
