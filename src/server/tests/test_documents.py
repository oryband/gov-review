#!/usr/bin/env python
# encoding: utf8

from documents import *

from random import sample, randint
import unittest


class TestDocuments(unittest.TestCase):
    def test_all(self):
        m = [MonitoredEntity.objects.create(name='entity %d' % i)
             for i in range(10)]
        t = [Tags.objects.create(name='tag %d' % i) for i in range(20)]

        v = Volume.objects.create(order=1)
        s = Section.objects.create(volume=v, order=1,
                                     title='first section')
        c = Chapter.objects.create(section=s, order=1,
                                     title='first chapter')
        sc = SubChapter.objects.create(
            chapter=c, order=1,
            title='first sub-chapter',
            monitored_entities=sample(m, randint(1, 4)),
            tags=sample(t, randint(1, 4)))

        for i, me in enumerate(sample(sc.monitored_entities,
                         randint(1, len(sc.monitored_entities))), 1):
            Defect.objects.create(
                sub_chapter=sc, order=i,
                description='defect %d' % i,
                reviews=[DefectReview(
                    monitored_entity=me,
                    description='review %d.%d' % (i, j))
                    for j in range(3)],
                url='http://google.com',
                status='fixed')

        for i in range(1, 10):
            Resolution.objects.create(
                tags=sample(t, randint(1, 4)),
                description='resolution %d' % i)
