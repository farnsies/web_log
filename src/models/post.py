__author__ = 'mrf'

import uuid
from datetime import datetime

from src.common.database import Database


class Post(object):
    def __init__(self, blog_id, title, content, author, date=None, _id=None):
        """Constructor"""
        self.blog_id = blog_id
        self.title = title
        self.content = content
        self.author = author
        self.created_date = datetime.utcnow() if date is None else date
        self._id = uuid.uuid4().hex if _id is None else _id

    def persist(self):
        Database.insert('posts', self.get_json())

    def get_json(self):
        return {
            '_id': self._id,
            'blog_id': self.blog_id,
            'author': self.author,
            'content': self.content,
            'title': self.title,
            'created_date': self.created_date
        }

    @classmethod
    def from_db(cls, id):
        data = Database.find_one('posts', {'id': id})
        return cls(**data)

    @staticmethod
    def from_blog(blog_id):
        return [post for post in Database.find('posts', {'blog_id': blog_id})]