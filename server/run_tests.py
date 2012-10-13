#!/usr/bin/env python
# encoding: utf8

from run_server import DB_NAME
from mongoengine import connect

import unittest
from tests.test_documents import TestDocuments


if __name__ == '__main__':
    db_name = '%s_test' % DB_NAME
    c = connect(db_name)
    c.drop_database(db_name)  # flush db.
    unittest.main()
    c.close()
