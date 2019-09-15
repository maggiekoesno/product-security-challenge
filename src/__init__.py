import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or '76d8f44b0b6943dd5a62'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///zendesk.db'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'dummy.zendeskchallenge@gmail.com'
app.config['MAIL_PASSWORD'] = 'securitychallenge'

# Below is the code that can be used if environment variables were used for the email account
#
# import os
# app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
# app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')

database = SQLAlchemy(app)
encrypt = Bcrypt(app)
login = LoginManager(app)
mail = Mail(app)

from src import pages