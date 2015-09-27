from unittest import TestCase

import mongomock

from app import app

class TestBase(TestCase):
    def setUp(self):
        super(TestBase, self).setUp()

        self.test_app = app.test_client()
        # Re-init the client, db and posts, so that we can mock.
        app.mongo_client = mongomock.MongoClient()
        app.db = app.mongo_client['leetnews']
        self.posts = app.posts = app.db['posts']

        self.posts.drop()

    def tearDown(self):
        pass
