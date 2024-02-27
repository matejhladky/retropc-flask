from flask import Flask, send_from_directory
from .config import Config
from .extensions import init_app_extensions, migrate
from .database import db
from .admin import setup_admin
from .commands import register_commands
from .routes.auth import auth_bp
from .routes.mail import mail_bp
from .views.category import category_bp
from .views.product import product_bp


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    migrate.init_app(app, db)

    init_app_extensions(app)

    register_commands(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(mail_bp)
    app.register_blueprint(product_bp, url_prefix='/api/v1/products')
    app.register_blueprint(category_bp, url_prefix='/api/v1/categories')

    setup_admin(app)

    @app.route('/static/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    with app.app_context():
        db.create_all()

    return app