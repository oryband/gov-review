#!/usr/bin/env python
# encoding: utf8

import redis
from json import dumps
from random import choice

if __name__ == '__main__':
    f = open('lorem.txt', 'rb')
    lorem = f.read()
    r = redis.StrictRedis(host='localhost', port=6379, db=0)

    r.flushall()  # Clear db.

    # Populate db with initial example data.
    for id in range(10):
        r.hset('gov-review', str(id), dumps({
            'tags': [str(x) for x in range(10)],
            'chapter': 'chapter ' + str(id),
            'entities': [str(x) for x in range(20)],
            #'description': 'blah blah.',
            'description': lorem,
            'url': 'http://google.com',
            'resolution': 'res res res res res.',
            'status': choice(['fixed', 'in-progress', 'unfixed']),
            'follow-up': 'nothing happened.',
            'responding-entity': 'big_brother',
            'responding-description': 'big brother says no.'
        }))

    r.save()  # Dump to file.
