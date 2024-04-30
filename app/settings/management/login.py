from app.settings.extensions import lm
from app.models import Users


def init_app(app):
    lm.init_app(app)

    lm.login_view = 'auth.login_'

    @lm.user_loader
    def load_user(user_id):
        return Users.query.get(user_id)