from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_restful import Api


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config["SECRET_KEY"] = "1234567"

db = SQLAlchemy(app)

from .views import *

from .models import User, Message
migrate = Migrate(app=app, db=db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

from .api import MessageApi, MessagesApi
api = Api(app)
api.add_resource(MessageApi, '/api/message')
api.add_resource(MessagesApi, '/api/messages')