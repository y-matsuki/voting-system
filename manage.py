from __future__ import print_function

from app import db, app
from flask.ext.script import Manager

manager = Manager(app)


@manager.command
def init_db():
    # db.drop_all()
    db.create_all()


if __name__ == '__main__':
    manager.run()
