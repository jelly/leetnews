#!/usr/bin/python 
from datetime import datetime

from flask import Flask, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
app.mongo_client = MongoClient()
app.db = app.mongo_client['leetnews']
app.posts = app.db['posts']

@app.route('/post/', methods=['GET', 'POST'])
def post():
    # List of posts
    if request.method == 'GET':
        # FIXME: add pagination
        cursor = app.posts.find({}, {'_id': 0}).limit(10) # 10 posts on front page
        return jsonify({'data': list(cursor), 'total': app.posts.find().count()})

    # A new post
    elif request.method == 'POST':
        fields = set(('url', 'title', 'author'))
        post = request.json
        keys = post.keys()

        if fields == keys:
            post['date'] = datetime.utcnow()
            app.posts.insert_one(post)
        elif fields < keys:
            return jsonify({'errors': 'too many dictionary keys', 'keys': ', '.join(keys - fields)}), 400
        elif set(('url', 'title', 'author')) > keys:
            return jsonify({'errors': 'missing dictionary keys', 'keys': ', '.join(fields - keys)}), 400
        else: # same number of keys, wrong keys
            return jsonify({'errors': 'missing dictionary keys', 'keys': ', '.join(fields - keys)}), 400

    return ''
