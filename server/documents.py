#!/usr/bin/env python
# encoding: utf8

from mongoengine import *

from datetime import datetime


class MonitoredEntity(Document):
    name = StringField(required=True)
    meta = {'indexes': ['name']}


class Tags(Document):
    name = StringField(required=True)
    meta = {'indexes': ['name']}


class Volume(Document):
    order = IntField(required=True, min_value=1, unique=True)
    meta = {'indexes': ['order'], 'ordering': ['+order']}


class Section(Document):
    volume = ReferenceField(Volume, required=True)
    order = IntField(required=True, min_value=1, unique_with='volume')
    title = StringField(required=True)
    meta = {'indexes': ['order'], 'ordering': ['+order']}


class Chapter(Document):
    section = ReferenceField(Section, required=True)
    order = IntField(required=True, min_value=1, unique_with='section')
    title = StringField(required=True)
    meta = {'indexes': ['order'], 'ordering': ['+order']}


class SubChapter(Document):
    chapter = ReferenceField(Chapter, required=True)
    order = IntField(min_value=1, unique_with='chapter')
    title = StringField(required=True)
    monitored_entities = ListField(ReferenceField(MonitoredEntity),
                                   required=True, default=list)
    tags = ListField(ReferenceField(Tags),
                     required=True, default=list)
    meta = {'indexes': ['order'], 'ordering': ['+order']}


class DefectReview(EmbeddedDocument):
    monitored_entity = ReferenceField(MonitoredEntity)
    description = StringField(required=True)


class Defect(Document):
    sub_chapter = ReferenceField(SubChapter, required=True)
    order = IntField(required=True, min_value=1,
                     unique_with='sub_chapter')
    description = StringField(required=True)
    reviews = ListField(EmbeddedDocumentField(DefectReview),
                        required=True, default=list)
    url = URLField()
    status = StringField(choices=('fixed', 'in_progress', 'unfixed'))
    time_updated = DateTimeField(required=True, default=datetime.now)
    meta = {'indexes': ['time_updated', 'status'], 'ordering': ['+order']}


class Resolution(Document):
    tags = ListField(ReferenceField(Tags), required=True, default=list)
    time_updated = DateTimeField(required=True, default=datetime.now)
    description = StringField(required=True)
    meta = {'indexes': ['time_updated'], 'ordering': ['-time_updated']}
