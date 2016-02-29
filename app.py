import logging
from logging import Formatter
from logging.handlers import RotatingFileHandler

import os
from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from modules.mail import Mail
from flask_gravatar import Gravatar

app = Flask(__name__)
app.config.from_object('config')

# Logging
app.debug_log_format = '%(asctime)s\t[%(levelname)s]\t%(message)s'
log_file = os.path.join(app.root_path, 'logs/app.log')
file_handler = RotatingFileHandler(log_file, backupCount=3, maxBytes=100000)
file_handler.setFormatter(Formatter('%(asctime)s\t[%(levelname)s]\t%(message)s'))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

login_manager = LoginManager()
login_manager.init_app(app)

db = SQLAlchemy(app)

gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    use_ssl=False,
                    base_url=None)

# Mail
server_root = app.config.get('SERVER_ROOT')
from_addr = app.config.get('MAIL_FROM_ADDRESS')
api_key = app.config.get('POSTMARK_API_KEY')
mail = Mail(server_root=server_root, from_addr=from_addr, api_key=api_key)

import modules.views
