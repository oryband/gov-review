#!/usr/bin/env python
# encoding: utf8

import redis
import pprint

if __name__ == '__main__':
    r = redis.StrictRedis(host='localhost', port=6379, db=0)

    report = r.hgetall('gov-review')
    pprint.pprint(report)
