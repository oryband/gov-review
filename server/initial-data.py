#!/usr/bin/env python
# encoding: utf8

import redis

if __name__ == '__main__':
    r = redis.StrictRedis(host='localhost', port=6379, db=0)

    r.flushall()  # Clear db.

    # Populate db with initial example data.
    for id in range(10):
        r.hset('gov-review', str(id), {
            'cp': 'chapter ' + str(id),
            'ent': [str(x) for x in range(10)],
            'desc': 'blah blah.',
            'url': 'http://google.com',
            'res': 'res res res res res.',
            'st': '0',
            'fu': 'nothing happened.',
            'r_ent': 'big_brother',
            'r_desc': 'big brother says no.'
        })

    r.save()  # Dump to file.
