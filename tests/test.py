from utils import AbstractTestCase
import unittest


class VotingSystemTestCase(AbstractTestCase):
    def test_not_found(self):
        rv = self.app.get('/hoge', follow_redirects=True)
        assert '<title>404 Not Found</title>' in str(rv.data)

    def test_unauthorized(self):
        rv = self.app.get('/', follow_redirects=True)
        assert '<title>Login</title>' in str(rv.data)
        rv = self.app.get('/topic/new', follow_redirects=True)
        assert '<title>Login</title>' in str(rv.data)

    def test_show_home_by_user(self):
        self.login('user@example.com', 'password')
        rv = self.app.get('/', follow_redirects=True)
        assert '<title>Voting System</title>' in str(rv.data)
        assert 'voting_user' in str(rv.data)
        assert 'Add Topic' not in str(rv.data)

    def test_show_home_by_admin(self):
        self.login('admin@example.com', 'password')
        rv = self.app.get('/', follow_redirects=True)
        assert '<title>Voting System</title>' in str(rv.data)
        assert 'voting_admin' in str(rv.data)
        assert 'Add Topic' in str(rv.data)

    def test_add_topic(self):
        self.login('admin@example.com', 'password')
        rv = self.app.get('/topic/new', follow_redirects=True)
        assert 'action="/topic/new" method="post"' in str(rv.data)
        rv = self.app.post('/topic/new', data=dict(
            id='peach',
            title='Peach Project',
            description='This is a test project.'
        ), follow_redirects=True)
        assert 'href="/topic/peach"' in str(rv.data)
        assert 'Peach Project' in str(rv.data)
        assert 'This is a test project.' in str(rv.data)
        assert 'Private' in str(rv.data)

    def test_add_entry(self):
        self.test_add_topic()
        rv = self.app.post('/topic/peach/entry/new', data=dict(
            title='Sample Entry',
            category='idea',
            description='This is a test entry.'
        ), follow_redirects=True)
        assert 'Sample Entry' in str(rv.data)
        assert 'This is a test entry.' in str(rv.data)

    def test_add_comment(self):
        self.test_add_entry()
        rv = self.app.post('/topic/peach/entry/1', data=dict(
            text='This is a test comment.'
        ), follow_redirects=True)
        assert 'This is a test comment.' in str(rv.data)


if __name__ == '__main__':
    unittest.main()
