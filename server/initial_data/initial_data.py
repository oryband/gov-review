#!/usr/bin/env python
# encoding: utf8
"""Populates database file with initial lorem-ipsum data, for testing
purposes.
"""

from documents import *
from run_server import DB_NAME

from mongoengine import connect

from random import choice, sample, randint
from datetime import datetime
from re import sub


def generate_initial_data():
    # Data size.
    TAG_AMOUNT = 10
    ENTITY_AMOUNT = 20

    VOLUME_AMOUNT = 2
    SECTION_AMOUNT = 2  # Per volume.
    CHAPTER_AMOUNT = 2  # Per section.
    SUB_CHAPTER_AMOUNT = 2  # Per chapter.
    DEFECT_AMOUNT = 3  # Per sub-chapter.

    RESOLUTION_AMOUNT = 15

    def generate_text(source, word_range):
        return ' '.join(sample(source, randint(1, word_range)))

    connection = connect(DB_NAME)
    connection.drop_database(DB_NAME)  # WARNING: flushes db.

    # Fetch lorem-ipsum source text.
    f = open('lorem.txt', 'rb')
    lorem = f.read()
    f.close()

    # Filter dots, commas, spaces, etc.
    lorem = sub(r'[\.\,\-]', r'', lorem)
    lorem_words = lorem.split(' ')
    lorem_words = [word.strip() for word in lorem_words if word.strip()]

    # Generate tag and monitored entities stash.
    monitored_entities = [MonitoredEntity.objects.create(
        name=generate_text(lorem_words, 10))
        for _ in range(ENTITY_AMOUNT)]
    tags = [Tags.objects.create(
        name=generate_text(lorem_words, 3)) for _ in range(TAG_AMOUNT)]

    # Generate volumes, sections, chapters, defects, etc.
    for vi in range(1, VOLUME_AMOUNT + 1):
        v = Volume.objects.create(order=vi)
        for si in range(1, SECTION_AMOUNT + 1):
            s = Section.objects.create(
                volume=v, order=si, title=generate_text(lorem_words, 4))
            for ci in range(1, CHAPTER_AMOUNT + 1):
                c = Chapter.objects.create(
                    section=s, order=ci,
                    title=generate_text(lorem_words, 5))
            for sci in range(1, SUB_CHAPTER_AMOUNT + 1):
                sc = SubChapter.objects.create(
                    chapter=c, order=sci,
                    title=generate_text(lorem_words, 21),
                    monitored_entities=sample(monitored_entities,
                                              randint(1, 4)),
                    tags=sample(tags, randint(1, 4)))
                for di, me in enumerate(
                    sample(sc.monitored_entities,
                           randint(1, len(sc.monitored_entities))), 1):
                    Defect.objects.create(
                        sub_chapter=sc, order=di,
                        description=lorem,
                        reviews=[DefectReview(monitored_entity=me,
                                              description=lorem)
                                 for _ in range(3)],
                        url='http://google.com',
                        status=choice(('fixed', 'in_progress', 'unfixed'))
                    )

    for ri in range(1, RESOLUTION_AMOUNT + 1):
        Resolution.objects.create(
            tags=sample(tags, randint(1, 4)),
            datetime=datetime(randint(1995, 2011),
                              randint(1, 12),
                              randint(1, 28)),
            description=lorem)

    connection.close()
