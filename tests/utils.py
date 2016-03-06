import os
import tempfile
import unittest

import app
from modules import models


class AbstractTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()
        app.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + self.db_path
        app.app.config['WTF_CSRF_ENABLED'] = False
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()
        app.db.create_all()
        admin = models.User(username='voting_admin', email='admin@example.com',
                            password='password', active=True, is_admin=True)
        user = models.User(username='voting_user', email='user@example.com',
                           password='password', active=True, is_admin=False)
        app.db.session.add(admin)
        app.db.session.add(user)
        app.db.session.commit()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def login(self, email, password):
        return self.app.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)
