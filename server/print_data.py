#!/usr/bin/env python
# encoding: utf8

s = __import__("run-server")  # Because of dash `-` in file name.

import redis

from json import loads
from pprint import pprint

if __name__ == '__main__':
    r = redis.StrictRedis(host=s.DB_HOST, port=s.DB_PORT, db=0)

    reports = r.hgetall(s.DB_KEY)
    for k in reports.keys():  # Convert JSON to dict.
        reports[k] = loads(reports[k])

    pprint(reports)
