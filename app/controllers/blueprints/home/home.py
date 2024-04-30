from app.controllers.blueprints.home import home_bp
from flask_login import login_required

@home_bp.route('/')
@login_required
def index():
    return '''<h1 height="80px">Logado, sacana</h1>
            <a href="/logout/">Sair</a>
    '''