import os
import unittest
from urlparse import urlparse

from werkzeug.security import generate_password_hash

os.environ['CONFIG_PATH'] = 'blog.config.TestingConfig'

from blog import app
from blog import models
from blog.database import Base, engine, session


class TestViews(unittest.TestCase):
    def setUp(self):

        """
        Test Setup.
        """

        self.client = app.test_client()

        Base.metadata.create_all(engine)

        # Create sample user
        self.user = models.User(name='Alice',
                                email='alice@example.com',
                                password=generate_password_hash('test'))

        session.add(self.user)
        session.commit()

    def tearDown(self):

        """
        Test teardown.
        """

        # Remove tables and their data from the database
        Base.metadata.drop_all(engine)

    def simulate_login(self):
        with self.client.session_transaction() as http_session:
            http_session['user_id'] = str(self.user.id)
            http_session['_fresh'] = True

    def test_add_post(self):
        self.simulate_login()

        response = self.client.post('/post/add', data={
            'title': 'Test Post',
            'content': 'Test Content'
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlparse(response.location).path, '/')
        posts = session.query(models.Post).all()
        self.assertEqual(len(posts), 1)

        post = posts[0]
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.content, '<p>Test Content</p>\n')
        self.assertEqual(post.author, self.user)

    def test_delete_post(self):
        self.simulate_login()

        response = self.client.post('/post/add', data={
            'title': 'Test Post',
            'content': 'Test Content'
        })


        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlparse(response.location).path, '/')
        posts = session.query(models.Post).all()
        self.assertEqual(len(posts), 1)

        print type(response)
        print vars(response)

        post = posts[0]

        post_url = '/post/%s' % post.id
        post_delete = '/post/%s/delete' % post.id

        self.assertEqual(self.client.get(post_url).status_code, 200)

        delete_post = self.client.get(post_delete)
        self.assertEqual(delete_post.status_code, 302)
        self.assertEqual(self.client.get(post_url).status_code, 500)

        print delete_post

    def test_view_post(self):
        self.simulate_login()

        response = self.client.post('/post/add', data={
            'title': 'Test Post',
            'content': 'Test Content'
        })

        posts = session.query(models.Post).all()

        post = posts[0]
        post_url = '/post/%s/' % post.id

        view_post = self.client.get(post_url)
        print view_post

    def test_edit_post(self):
        self.simulate_login()

        response = self.client.post('/post/add', data={
            'title': 'Test Post',
            'content': 'Test Content'
        })

        posts = session.query(models.Post).all()

        post = posts[0]
        post_url = '/post/%s/' % post.id

        view_post = self.client.get(post_url)
        print view_post


if __name__ == '__main__':
    unittest.main()