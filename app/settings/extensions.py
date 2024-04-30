from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mailman import Mail

db = SQLAlchemy()
lm = LoginManager()
mail = Mail()


def init_app(app) -> None:
    db.init_app(app)
    Migrate(app, db)
