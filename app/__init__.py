from flask import Flask
from config import Config
from flask_seasurf import SeaSurf
from flask_talisman import Talisman
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
csrf = SeaSurf(app)

SELF = "'self'"
talisman = Talisman(
    app,
    content_security_policy={
        'default-src': [
            SELF,
            'https://fonts.googleapis.com/',
            'https://fonts.gstatic.com/s/syne/',
            'https://player.vimeo.com/',
        ],
        'img-src': SELF,
        'script-src': [
            SELF,
        ],
        'style-src': [
            SELF,
            'https://fonts.googleapis.com/',
            'https://fonts.gstatic.com/s/syne/',
        ],
        'base-uri': SELF,
        'object-src': "'none'",
        'frame-ancestors': "'none'",
        'form-action': SELF,
    },
    content_security_policy_nonce_in=['script-src'],
    feature_policy={
        'geolocation': '\'none\'',
    }
)

login = LoginManager(app)
login.login_view = 'login'
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)

from app import routes, models