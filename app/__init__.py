from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'
# login.login_message = "Hey you can't do that!"
login.login_message_category = 'danger'

CORS(app)

from app.blueprints.api import bp as api
app.register_blueprint(api)

from . import routes, models