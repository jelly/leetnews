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

        app.posts.drop()

    def testCreatePost(self):
        ''' Test post creation '''

        data = {'author': 'John Doe', 'title': 'My new post', 'url': 'https://google.com' }
        response = self.test_app.post('/post/', data = json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        item = app.posts.find_one({'author': 'John Doe'})

        self.assertIsNotNone(item['date'])

        del item['date']
        del item['_id']
        self.assertEqual(item, data)

    def testCreatePostMissing(self):
        ''' Test post creation parameters missing '''

        data = {'foobar': 'John Doe', 'title': 'My new post', 'url': 'https://google.com' }
        response = self.test_app.post('/post/', data = json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
