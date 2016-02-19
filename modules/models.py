from app import db
from sqlalchemy.orm import synonym
from werkzeug import check_password_hash, generate_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    # password = db.Column(db.Text)
    _password = db.Column('password', db.String(100))
    active = db.Column(db.Boolean, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)
    topics = db.relationship('Topic', backref='owner', lazy='dynamic')

    def get_id(self):
        return self.id

    @property
    def is_active(self):
        return self.active

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        if password:
            password = password.strip()
        self._password = generate_password_hash(password)

    password_descriptor = property(_get_password, _set_password)
    password = synonym('_password', descriptor=password_descriptor)

    def check_password(self, password):
        password = password.strip()
        if not password:
            return False
        return check_password_hash(self.password, password)

    @classmethod
    def authenticate(cls, query, email, password):
        user = query(cls).filter(cls.email == email).first()
        if user is None:
            return None, False
        return user, user.check_password(password)

    def __repr__(self):
        return '<User id={id} username={username!r}>'.format(id=self.id, username=self.username)


members = db.Table('members',
                   db.Column('project_id', db.Text, db.ForeignKey('topic.id')),
                   db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
                   )


class Topic(db.Model):
    id = db.Column(db.Text, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.Text)
    entries = db.relationship('Entry', backref='topic', lazy='dynamic')
    members = db.relationship('User', secondary=members,
                              backref=db.backref('my_projects', lazy='dynamic'))

    def __repr__(self):
        return '<Topic id={id} title={title!r}>'.format(id=self.id, title=self.title)


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Text, db.ForeignKey('topic.id'))
    title = db.Column(db.Text)
    detail = db.Column(db.Text)
    # Bug, Enhance, Idea..
    type = db.Column(db.Text)
    # New, Vote, Pending, Done, Close
    status = db.Column(db.Text)

    def __repr__(self):
        return '<Entry id={id} title={title!r}>'.format(id=self.id, title=self.title)


class Reset(db.Model):
    key = db.Column(db.Text, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
