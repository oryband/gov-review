#!/usr/bin/env python
# encoding: utf8

s = __import__("run-server")  # Because of dash `-` in file name.

import redis

from json import dumps
from random import choice, randrange
from datetime import date
from re import sub

if __name__ == '__main__':
    #r = redis.StrictRedis(host=s.DB_HOST, port=s.DB_PORT, db=0)
    #r.flushall()  # Clear db.

    f = open('lorem.txt', 'rb')
    lorem = f.read()
    f.close()

    # Filter dots, commas, spaces, etc.
    lorem = sub(r'[\.\,\-]', r'', lorem)
    lorem_split = lorem.split(' ')
    lorem_split = [word.strip() for word in lorem_split if word.strip()]

    tags = [choice(lorem_split) for x in range(10)]
    entities = [' '.join(
        [choice(lorem_split) for words in range(randrange(10))]
    ) for x in range(10)]

    # Populate db/file with initial lorem-ipsum data.
    chapters = []
    for chapter in range(1, 6):
        sub_chapters = []
        for sub_chapter in range(1, 4):
            cur_entities = sorted(set(
                [choice(entities) for x in range(randrange(1, 6))]
            ))

            defects = []
            for defect in range(3):
                defects.append({
                    'tags': sorted(set(
                        [choice(tags) for x in range(randrange(1, 11))]
                    )),
                    'url': 'http://google.com',
                    'description': lorem,
                    'status': choice(('fixed', 'in-progress', 'unfixed')),
                    'follow-up': dict.fromkeys(cur_entities, lorem),
                })

            sub_chapters.append({
                'name': ' '.join([choice(lorem_split)
                                  for word in range(randrange(1, 21))]),
                'entities': cur_entities,
                'defects': defects
            })

        chapters.append({
            'name': 'chapter-%s' % chapter,
            'sub-chapters': sub_chapters
        })

    resolutions = {}
    for resolution in range(15):
        resolutions[date(2011,
                         choice(range(1, 13)),
                         choice(range(1, 31))
                    ).isoformat()] = {
                        'tags': sorted(set(
                            [choice(tags) for x in range(randrange(1, 11))]
                        )),
                        'description': lorem
                    }

    #r.hset(s.DB_KEY, 'chapters', dumps(chapters))
    #r.hset(s.DB_KEY, 'resolutions', dumps(resolutions))
    #r.save()  # Save to db.

    d = {'chapters': chapters, 'resolutions': resolutions}
    f = open('data.json', 'wb')
    f.write(dumps(d))
    f.close()
