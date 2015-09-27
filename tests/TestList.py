import json

from TestBase import TestBase

class TestList(TestBase):
    def setUp(self):
        TestBase.setUp(self)

    def testList(self):
        test_data = {'author': 'John Doe', 'title': 'My new post', 'url': 'https://google.com' }
        item = self.posts.insert_one(test_data)
        response = self.test_app.get('/post/', content_type='application/json')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data['total'], 1)
        del test_data['_id']
        self.assertEqual(data['data'][0], test_data)
