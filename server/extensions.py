from flask_admin import Admin
from flask_cors import CORS
from flask_login import LoginManager
from flask_mail import Mail

from .admin import CustomAdminIndexView
from .models import User

login_manager = LoginManager()
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


mail = Mail()

admin = Admin(template_mode='bootstrap3', index_view=CustomAdminIndexView())

cors = CORS()

def init_app_extensions(app):
    login_manager.init_app(app)
    mail.init_app(app)
    cors.init_app(app, resources={r'/*': {'origins': '*'}})