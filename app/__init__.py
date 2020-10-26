from flask import Flask
from flask_talisman import Talisman
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
# Talisman(app)
login = LoginManager(app)
login.login_view = 'login'
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)

from app import routes, models