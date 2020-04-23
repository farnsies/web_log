__author__ = 'mrf'

import uuid
from datetime import datetime

from src.common.database import Database
from src.models.post import Post


class Blog(object):
    def __init__(self, author, title, description, author_id, _id=None):
        self.author = author
        self.title = title
        self.description = description
        self.author_id = author_id
        self._id = uuid.uuid4().hex if _id is None else _id

    def new_post(self, title, content, date=datetime.utcnow()):
        post = Post(_id=self._id,
                    title=title,
                    content=content,
                    author=self.author,
                    created_date=date)
        post.persist()

    def get_posts(self):
        return Post.from_blog(self._id)

    def persist(self):
        Database.insert(collection='blogs',
                        data=self.get_json())

    def get_json(self):
        return {
            'author': self.author,
            'author_id': self.author_id,
            'title': self.title,
            'description': self.description,
            '_id': self._id
        }

    @classmethod
    def load_from_db(cls, _id):
        data = Database.find_one(collection='blogs',
                                 query={'_id': _id})
        return cls(**data)

    @classmethod
    def find_by_author_id(cls, author_id):
        blogs = Database.find(collection='blogs',
                              query={'author_id': author_id})
        return [cls(**blog) for blog in blogs]