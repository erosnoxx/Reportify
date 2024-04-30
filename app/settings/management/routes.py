from app.controllers.blueprints.auth.login import auth_bp
from app.controllers.blueprints.home.home import home_bp

def init_app(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)
