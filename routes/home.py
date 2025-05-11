from flask import render_template
from flask_login import current_user, login_required


def setup_home_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html',
                               user=current_user,
                               is_authenticated=current_user.is_authenticated)