import os
import json
from unittest import TestCase

import mongomock
from mongomock import Database
from mongomock import OperationFailure

from app import app

class TestClass(TestCase):
    def setUp(self):
        super(TestClass, self).setUp()

        self.test_app = app.test_client()
        # Re-init the client, db and posts, so that we can mock.
        app.mongo_client = mongomock.MongoClient()
        app.db = app.mongo_client['leetnews']
        app.posts = app.db['posts']

    def testCreatePost(self):
        data = json.dumps({'author': 'John Doe', 'title': 'My new post', 'url': 'https://google.com' })
        response = self.test_app.post('/post/', data = data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
