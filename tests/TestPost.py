import json

from TestBase import TestBase

class TestPost(TestBase):
    def setUp(self):
        TestBase.setUp(self)

    def testCreatePost(self):
        ''' Test post creation '''

        data = {'author': 'John Doe', 'title': 'My new post', 'url': 'https://google.com' }
        response = self.test_app.post('/post/', data = json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        item = self.posts.find_one({'author': 'John Doe'})

        self.assertIsNotNone(item['date'])

        del item['date']
        del item['_id']
        self.assertEqual(item, data)

    def testCreatePostParameters(self):
        ''' Test post creation same number of parameters, wrong parameter '''

        data = {'foobar': 'John Doe', 'title': 'My new post', 'url': 'https://google.com' }
        response = self.test_app.post('/post/', data = json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # Verify error message
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data['errors'], 'missing dictionary keys')
        self.assertEqual(data['keys'], 'author')

    def testCreatePostMissingParameter(self):
        ''' Test post creation, not enough parameters'''

        data = {'title': 'My new post', 'url': 'https://google.com' }
        response = self.test_app.post('/post/', data = json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # Verify error message
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data['errors'], 'missing dictionary keys')
        self.assertEqual(data['keys'], 'author')

    def testCreatePostTooManyParameter(self):
        ''' Test post creation, too many parameters'''

        data = {'title': 'My new post', 'url': 'https://google.com', 'author': 'John doe', 'foobar': 'text', 'test': 'test' }
        response = self.test_app.post('/post/', data = json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # Verify error message
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data['errors'], 'too many dictionary keys')
        self.assertIn('foobar', data['keys'])
        self.assertIn('test', data['keys'])
