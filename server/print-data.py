#!/usr/bin/env python
# encoding: utf8

import redis
from json import loads
from pprint import pprint

if __name__ == '__main__':
    r = redis.StrictRedis(host='localhost', port=6379, db=0)

    reports = r.hgetall('gov-review')
    for k in reports.keys():  # Convert JSON to dict.
        reports[k] = loads(reports[k])

    pprint(reports)
